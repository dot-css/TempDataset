"""
Core data generation engine.

Coordinates dataset generation and manages the dataset registry.
"""

import os
import warnings
from typing import Dict, Type, Union, Optional, Iterator, List, Any
from .datasets.base import BaseDataset
from .utils.data_frame import TempDataFrame
from .utils.performance import (
    MemoryMonitor, ProgressTracker, BatchProcessor, 
    DataStructureOptimizer, optimize_for_large_datasets, PerformanceProfiler
)
from .exceptions import (
    DatasetNotFoundError, DataGenerationError, ValidationError,
    MemoryError as TempDatasetMemoryError, DependencyWarning, PerformanceWarning
)


class DataGenerator:
    """
    Main data generation engine that coordinates dataset creation.
    
    Manages dataset registration and provides the main generation interface.
    """
    
    def __init__(self):
        """Initialize the data generator with empty registry."""
        self.datasets: Dict[str, Type[BaseDataset]] = {}
        self.faker_available = self._check_faker()
        self.memory_monitor = MemoryMonitor()
        self.profiler = PerformanceProfiler()
    
    def register_dataset(self, name: str, dataset_class: Type[BaseDataset]) -> None:
        """
        Register a new dataset type.
        
        Args:
            name: Name of the dataset type
            dataset_class: Class that implements BaseDataset
            
        Raises:
            ValidationError: If parameters are invalid
        """
        # Validate input parameters
        if not isinstance(name, str):
            raise ValidationError("name", name, "string")
        
        if not name.strip():
            raise ValidationError("name", name, "non-empty string")
        
        if not isinstance(dataset_class, type):
            raise ValidationError("dataset_class", dataset_class, "class type")
        
        # Check if class implements BaseDataset
        if not issubclass(dataset_class, BaseDataset):
            raise ValidationError(
                "dataset_class", 
                dataset_class, 
                "subclass of BaseDataset",
                "The class must inherit from BaseDataset and implement required methods."
            )
        
        self.datasets[name] = dataset_class
    
    def generate(self, dataset_type: str, rows: int = 500) -> Union[TempDataFrame, None]:
        """
        Generate dataset using registered generators.
        
        Args:
            dataset_type: Dataset type ('sales') or filename ('sales.csv', 'sales.json')
            rows: Number of rows to generate
            
        Returns:
            TempDataFrame for dataset types, None for file outputs
            
        Raises:
            ValidationError: If parameters are invalid
            DatasetNotFoundError: If dataset type is not registered
            DataGenerationError: If data generation fails
            TempDatasetMemoryError: If memory limits are exceeded
        """
        # Validate input parameters
        if not isinstance(dataset_type, str):
            raise ValidationError("dataset_type", dataset_type, "string")
        
        if not dataset_type.strip():
            raise ValidationError("dataset_type", dataset_type, "non-empty string")
        
        if not isinstance(rows, int):
            raise ValidationError("rows", rows, "integer")
        
        if rows < 0:
            raise ValidationError("rows", rows, "non-negative integer")
        
        # Check memory requirements for large datasets
        self._check_memory_requirements(rows)
        
        # Check if it's a file output request
        if dataset_type.endswith('.csv') or dataset_type.endswith('.json'):
            return self._generate_to_file(dataset_type, rows)
        
        # Generate dataset in memory
        if dataset_type not in self.datasets:
            available = list(self.datasets.keys())
            raise DatasetNotFoundError(dataset_type, available)
        
        try:
            # Get optimization settings based on dataset size
            optimization_settings = optimize_for_large_datasets(rows)
            
            # Start performance profiling
            self.profiler.start_operation("data_generation")
            
            # Use optimized generation for large datasets
            if optimization_settings["use_batching"]:
                data = self._generate_with_batching(dataset_type, rows, optimization_settings)
            else:
                data = self._generate_standard(dataset_type, rows, optimization_settings)
            
            # End performance profiling
            generation_time = self.profiler.end_operation("data_generation")
            
            # Log performance info for large datasets
            if optimization_settings["show_progress"]:
                print(f"\nGeneration completed in {generation_time:.2f}s ({rows/generation_time:.0f} rows/sec)")
            
            # Get schema from dataset class
            dataset_class = self.datasets[dataset_type]
            temp_dataset = dataset_class(1)  # Create temporary instance for schema
            schema = temp_dataset.get_schema()
            columns = list(schema.keys())
            
            return TempDataFrame(data, columns)
            
        except Exception as e:
            # Wrap any unexpected errors in DataGenerationError
            if isinstance(e, (ValidationError, DatasetNotFoundError, TempDatasetMemoryError)):
                raise  # Re-raise our custom exceptions as-is
            
            raise DataGenerationError(
                f"Unexpected error during data generation: {str(e)}", 
                dataset_type, 
                rows
            ) from e
    
    def _generate_to_file(self, filename: str, rows: int) -> None:
        """
        Generate dataset and save to file.
        
        Args:
            filename: Output filename with extension
            rows: Number of rows to generate
            
        Raises:
            ValidationError: If filename format is invalid
            DataGenerationError: If file generation fails
        """
        # Validate filename
        if not filename or not isinstance(filename, str):
            raise ValidationError("filename", filename, "non-empty string")
        
        # Extract dataset type from filename
        base_name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1].lower()
        
        # Validate file extension
        supported_extensions = ['.csv', '.json']
        if extension not in supported_extensions:
            raise ValidationError(
                "filename", 
                filename, 
                f"filename with extension in {supported_extensions}",
                f"Got extension: {extension}"
            )
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                raise DataGenerationError(
                    f"Failed to create directory '{directory}': {str(e)}", 
                    rows=rows
                ) from e
        
        # For now, assume 'sales' dataset - will be expanded later
        dataset_type = 'sales'
        
        try:
            # Get optimization settings
            optimization_settings = optimize_for_large_datasets(rows)
            
            # Use streaming for very large datasets to avoid memory issues
            if optimization_settings["use_streaming"]:
                self._generate_streaming_to_file(dataset_type, rows, filename)
            else:
                # Generate the data in memory first
                temp_df = self.generate(dataset_type, rows)
                
                # Save to appropriate format
                if extension == '.csv':
                    temp_df.to_csv(filename)
                elif extension == '.json':
                    temp_df.to_json(filename)
                
        except Exception as e:
            if isinstance(e, (ValidationError, DatasetNotFoundError, TempDatasetMemoryError)):
                raise  # Re-raise our custom exceptions as-is
            
            raise DataGenerationError(
                f"Failed to generate file '{filename}': {str(e)}", 
                dataset_type, 
                rows
            ) from e
    
    def _check_memory_requirements(self, rows: int) -> None:
        """
        Check if the requested number of rows might exceed memory limits.
        
        Args:
            rows: Number of rows to generate
            
        Raises:
            TempDatasetMemoryError: If estimated memory usage is too high
        """
        # Estimate memory usage (rough calculation)
        # Assume ~1KB per row for sales data (27 columns with mixed types)
        estimated_memory_mb = (rows * 1024) / (1024 * 1024)  # Convert to MB
        
        # Set reasonable limits
        warning_threshold_mb = 100  # Warn at 100MB
        error_threshold_mb = 500    # Error at 500MB
        
        if estimated_memory_mb > error_threshold_mb:
            raise TempDatasetMemoryError(rows, estimated_memory_mb)
        elif estimated_memory_mb > warning_threshold_mb:
            warnings.warn(
                f"Large dataset requested ({rows:,} rows, ~{estimated_memory_mb:.1f} MB). "
                f"Consider using file output for better memory efficiency.",
                category=UserWarning,
                stacklevel=3
            )
    
    def _generate_standard(self, dataset_type: str, rows: int, optimization_settings: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate dataset using standard method.
        
        Args:
            dataset_type: Type of dataset to generate
            rows: Number of rows to generate
            optimization_settings: Optimization settings
            
        Returns:
            List of dictionaries representing the data
        """
        dataset_class = self.datasets[dataset_type]
        dataset = dataset_class(rows)
        
        # Monitor memory usage if enabled
        if optimization_settings["memory_monitoring"]:
            self.memory_monitor.check_memory_usage("standard generation")
        
        # Generate data
        data = dataset.generate()
        
        # Optimize data structure if needed
        if rows > 5000:
            data = DataStructureOptimizer.optimize_dict_list(data)
        
        return data
    
    def _generate_with_batching(self, dataset_type: str, rows: int, optimization_settings: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate dataset using batch processing for memory efficiency.
        
        Args:
            dataset_type: Type of dataset to generate
            rows: Number of rows to generate
            optimization_settings: Optimization settings
            
        Returns:
            List of dictionaries representing the data
        """
        batch_size = optimization_settings["batch_size"]
        batch_processor = BatchProcessor(batch_size)
        
        def batch_generator(start_idx: int, batch_size: int) -> Iterator[Dict[str, Any]]:
            """Generate a batch of data."""
            dataset_class = self.datasets[dataset_type]
            dataset = dataset_class(batch_size)
            batch_data = dataset.generate()
            return iter(batch_data)
        
        # Process in batches and collect results
        all_data = []
        progress_desc = f"Generating {dataset_type} data"
        
        for item in batch_processor.process_in_batches(
            rows, 
            batch_generator, 
            progress_description=progress_desc
        ):
            all_data.append(item)
        
        # Optimize final data structure
        all_data = DataStructureOptimizer.optimize_dict_list(all_data)
        
        return all_data
    
    def _generate_streaming_to_file(self, dataset_type: str, rows: int, filename: str) -> None:
        """
        Generate dataset directly to file using streaming for very large datasets.
        
        Args:
            dataset_type: Type of dataset to generate
            rows: Number of rows to generate
            filename: Output filename
        """
        optimization_settings = optimize_for_large_datasets(rows)
        batch_size = optimization_settings["batch_size"]
        
        # Determine file format
        extension = os.path.splitext(filename)[1].lower()
        
        # Get schema from dataset class
        dataset_class = self.datasets[dataset_type]
        temp_dataset = dataset_class(1)
        schema = temp_dataset.get_schema()
        columns = list(schema.keys())
        
        def batch_generator(start_idx: int, batch_size: int) -> Iterator[Dict[str, Any]]:
            """Generate a batch of data."""
            dataset = dataset_class(batch_size)
            batch_data = dataset.generate()
            return iter(batch_data)
        
        # Stream directly to file
        if extension == '.csv':
            from .io.csv_handler import write_csv_streaming
            
            def data_generator():
                batch_processor = BatchProcessor(batch_size)
                for item in batch_processor.process_in_batches(
                    rows, 
                    batch_generator, 
                    progress_description=f"Streaming {dataset_type} to CSV"
                ):
                    yield item
            
            write_csv_streaming(data_generator(), filename, columns)
            
        elif extension == '.json':
            from .io.json_handler import write_json_streaming
            
            def data_generator():
                batch_processor = BatchProcessor(batch_size)
                for item in batch_processor.process_in_batches(
                    rows, 
                    batch_generator, 
                    progress_description=f"Streaming {dataset_type} to JSON"
                ):
                    yield item
            
            write_json_streaming(data_generator(), filename, lines=True)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics from recent operations.
        
        Returns:
            Dictionary with performance statistics
        """
        return {
            "profiler_summary": self.profiler.get_summary(),
            "peak_memory_mb": self.memory_monitor.peak_memory,
            "current_memory_mb": self.memory_monitor.current_memory
        }
    
    def _check_faker(self) -> bool:
        """
        Check if Faker library is available.
        
        Returns:
            True if Faker is available, False otherwise
        """
        try:
            import faker
            return True
        except ImportError:
            return False
    
    def _warn_faker_missing(self) -> None:
        """
        Show warning about missing Faker library when actually needed.
        """
        warnings.warn(
            "Faker library not found. Using basic random data generation. "
            "Install faker for more realistic data: pip install faker",
            category=DependencyWarning,
            stacklevel=3
        )