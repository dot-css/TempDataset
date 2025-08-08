"""
Performance monitoring and optimization utilities.

Provides tools for monitoring memory usage, progress tracking, and performance optimization.
"""

import time
import sys
import gc
import warnings
from typing import Iterator, Any, Optional, Callable, Dict
from ..exceptions import PerformanceWarning, MemoryError as TempDatasetMemoryError


class MemoryMonitor:
    """Monitor memory usage during data generation."""
    
    def __init__(self):
        self.peak_memory = 0
        self.current_memory = 0
        self.warning_threshold_mb = 100
        self.error_threshold_mb = 500
    
    def get_memory_usage_mb(self) -> float:
        """
        Get current memory usage in MB.
        
        Returns:
            Current memory usage in megabytes
        """
        # Get size of all objects in memory (rough estimation)
        total_size = 0
        for obj in gc.get_objects():
            try:
                total_size += sys.getsizeof(obj)
            except (TypeError, AttributeError):
                # Some objects don't support getsizeof
                continue
        
        return total_size / (1024 * 1024)  # Convert to MB
    
    def check_memory_usage(self, operation_name: str = "operation") -> None:
        """
        Check current memory usage and warn if thresholds are exceeded.
        
        Args:
            operation_name: Name of the operation being monitored
            
        Raises:
            TempDatasetMemoryError: If memory usage exceeds error threshold
        """
        current_mb = self.get_memory_usage_mb()
        self.current_memory = current_mb
        self.peak_memory = max(self.peak_memory, current_mb)
        
        if current_mb > self.error_threshold_mb:
            raise TempDatasetMemoryError(
                0,  # rows not applicable here
                current_mb
            )
        elif current_mb > self.warning_threshold_mb:
            warnings.warn(
                f"High memory usage detected during {operation_name}: "
                f"{current_mb:.1f} MB. Consider using batch processing or file output.",
                category=PerformanceWarning,
                stacklevel=3
            )
    
    def reset(self) -> None:
        """Reset memory monitoring counters."""
        self.peak_memory = 0
        self.current_memory = 0


class ProgressTracker:
    """Track progress of long-running operations."""
    
    def __init__(self, total_items: int, description: str = "Processing"):
        self.total_items = total_items
        self.description = description
        self.current_item = 0
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.update_interval = 1.0  # Update every second
        self.show_progress = total_items > 1000  # Only show for large operations
    
    def update(self, items_processed: int = 1) -> None:
        """
        Update progress counter.
        
        Args:
            items_processed: Number of items processed since last update
        """
        self.current_item += items_processed
        current_time = time.time()
        
        # Only update display if enough time has passed and we're showing progress
        if (self.show_progress and 
            current_time - self.last_update_time >= self.update_interval):
            self._display_progress()
            self.last_update_time = current_time
    
    def finish(self) -> None:
        """Mark operation as finished and display final progress."""
        self.current_item = self.total_items
        if self.show_progress:
            self._display_progress()
            print()  # New line after progress
    
    def _display_progress(self) -> None:
        """Display current progress to stdout."""
        if self.total_items == 0:
            return
        
        percentage = (self.current_item / self.total_items) * 100
        elapsed_time = time.time() - self.start_time
        
        if self.current_item > 0:
            estimated_total_time = elapsed_time * (self.total_items / self.current_item)
            remaining_time = estimated_total_time - elapsed_time
            
            # Format time
            if remaining_time > 60:
                time_str = f"{remaining_time/60:.1f}m remaining"
            else:
                time_str = f"{remaining_time:.0f}s remaining"
        else:
            time_str = "calculating..."
        
        # Create progress bar
        bar_width = 30
        filled_width = int(bar_width * percentage / 100)
        bar = "█" * filled_width + "░" * (bar_width - filled_width)
        
        # Display progress (overwrite previous line)
        print(f"\r{self.description}: [{bar}] {percentage:.1f}% ({self.current_item:,}/{self.total_items:,}) - {time_str}", 
              end="", flush=True)


class BatchProcessor:
    """Process large datasets in batches to manage memory usage."""
    
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
        self.memory_monitor = MemoryMonitor()
    
    def process_in_batches(
        self, 
        total_items: int, 
        generator_func: Callable[[int, int], Iterator[Any]], 
        processor_func: Optional[Callable[[Any], Any]] = None,
        progress_description: str = "Processing"
    ) -> Iterator[Any]:
        """
        Process items in batches to manage memory usage.
        
        Args:
            total_items: Total number of items to process
            generator_func: Function that generates items for a batch (start_idx, batch_size)
            processor_func: Optional function to process each item
            progress_description: Description for progress tracking
            
        Yields:
            Processed items
        """
        progress = ProgressTracker(total_items, progress_description)
        
        try:
            for start_idx in range(0, total_items, self.batch_size):
                # Calculate actual batch size (handle last batch)
                actual_batch_size = min(self.batch_size, total_items - start_idx)
                
                # Check memory before processing batch
                self.memory_monitor.check_memory_usage(f"batch {start_idx//self.batch_size + 1}")
                
                # Generate batch
                batch_items = generator_func(start_idx, actual_batch_size)
                
                # Process and yield items
                for item in batch_items:
                    if processor_func:
                        processed_item = processor_func(item)
                        yield processed_item
                    else:
                        yield item
                    
                    progress.update(1)
                
                # Force garbage collection after each batch
                gc.collect()
        
        finally:
            progress.finish()


class DataStructureOptimizer:
    """Optimize data structures for memory efficiency."""
    
    @staticmethod
    def optimize_dict_list(data: list) -> list:
        """
        Optimize a list of dictionaries for memory efficiency.
        
        Args:
            data: List of dictionaries to optimize
            
        Returns:
            Optimized list of dictionaries
        """
        if not data:
            return data
        
        # Get all unique keys
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
        
        # Convert to list for consistent ordering
        key_list = sorted(all_keys)
        
        # Create optimized dictionaries with consistent key ordering
        # This can help with memory locality and reduce overhead
        optimized_data = []
        for item in data:
            optimized_item = {key: item.get(key) for key in key_list}
            optimized_data.append(optimized_item)
        
        return optimized_data
    
    @staticmethod
    def estimate_memory_usage(data: list, sample_size: int = 100) -> Dict[str, float]:
        """
        Estimate memory usage of a data structure.
        
        Args:
            data: Data structure to analyze
            sample_size: Number of items to sample for estimation
            
        Returns:
            Dictionary with memory usage statistics
        """
        if not data:
            return {
                "total_mb": 0.0, 
                "per_item_bytes": 0.0, 
                "estimated_total_mb": 0.0,
                "sample_size": 0,
                "total_items": 0
            }
        
        # Sample items for estimation
        sample_data = data[:min(sample_size, len(data))]
        
        # Calculate memory usage of sample
        sample_memory = 0
        for item in sample_data:
            sample_memory += sys.getsizeof(item)
            if isinstance(item, dict):
                for key, value in item.items():
                    sample_memory += sys.getsizeof(key) + sys.getsizeof(value)
        
        # Calculate statistics
        per_item_bytes = sample_memory / len(sample_data) if sample_data else 0
        estimated_total_bytes = per_item_bytes * len(data)
        estimated_total_mb = estimated_total_bytes / (1024 * 1024)
        
        return {
            "total_mb": estimated_total_mb,
            "per_item_bytes": per_item_bytes,
            "estimated_total_mb": estimated_total_mb,
            "sample_size": len(sample_data),
            "total_items": len(data)
        }


def optimize_for_large_datasets(rows: int) -> Dict[str, Any]:
    """
    Determine optimal settings for large dataset generation.
    
    Args:
        rows: Number of rows to generate
        
    Returns:
        Dictionary with optimization settings
    """
    settings = {
        "use_batching": False,
        "batch_size": 1000,
        "show_progress": False,
        "use_streaming": False,
        "memory_monitoring": False
    }
    
    # Enable optimizations based on dataset size
    if rows > 1000:
        settings["show_progress"] = True
        settings["memory_monitoring"] = True
    
    if rows > 10000:
        settings["use_batching"] = True
        settings["batch_size"] = min(5000, rows // 10)  # 10 batches max
    
    if rows > 100000:
        settings["use_streaming"] = True
        settings["batch_size"] = min(10000, rows // 20)  # 20 batches max
    
    return settings


class PerformanceProfiler:
    """Profile performance of operations."""
    
    def __init__(self):
        self.operations = {}
    
    def start_operation(self, name: str) -> None:
        """Start timing an operation."""
        self.operations[name] = {
            "start_time": time.time(),
            "end_time": None,
            "duration": None
        }
    
    def end_operation(self, name: str) -> float:
        """
        End timing an operation.
        
        Args:
            name: Name of the operation
            
        Returns:
            Duration in seconds
        """
        if name not in self.operations:
            raise ValueError(f"Operation '{name}' was not started")
        
        end_time = time.time()
        self.operations[name]["end_time"] = end_time
        duration = end_time - self.operations[name]["start_time"]
        self.operations[name]["duration"] = duration
        
        return duration
    
    def get_summary(self) -> Dict[str, float]:
        """
        Get summary of all timed operations.
        
        Returns:
            Dictionary mapping operation names to durations
        """
        return {
            name: op["duration"] 
            for name, op in self.operations.items() 
            if op["duration"] is not None
        }