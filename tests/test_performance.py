"""
Performance and memory usage tests for TempDataset library.

Tests performance requirements and memory usage patterns for various dataset sizes.
"""

import pytest
import time
import gc
import os
import tempfile
from typing import Dict, Any

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    from memory_profiler import profile, memory_usage
    MEMORY_PROFILER_AVAILABLE = True
except ImportError:
    MEMORY_PROFILER_AVAILABLE = False

import tempdataset


class PerformanceMonitor:
    """Helper class to monitor performance metrics."""
    
    def __init__(self):
        self.process = psutil.Process() if PSUTIL_AVAILABLE else None
        self.start_time = None
        self.start_memory = None
        
    def start(self):
        """Start monitoring."""
        self.start_time = time.time()
        if self.process:
            self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        gc.collect()  # Clean up before measurement
        
    def stop(self) -> Dict[str, Any]:
        """Stop monitoring and return metrics."""
        end_time = time.time()
        duration = end_time - self.start_time if self.start_time else 0
        
        metrics = {
            'duration': duration,
            'memory_start_mb': self.start_memory if self.start_memory else 0,
            'memory_end_mb': 0,
            'memory_peak_mb': 0,
            'memory_used_mb': 0,
        }
        
        if self.process:
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            metrics.update({
                'memory_end_mb': end_memory,
                'memory_used_mb': end_memory - (self.start_memory or 0),
            })
            
        return metrics


@pytest.fixture
def performance_monitor():
    """Fixture providing performance monitoring."""
    return PerformanceMonitor()


@pytest.fixture
def temp_dir():
    """Fixture providing temporary directory for file tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestDatasetGenerationPerformance:
    """Test performance of dataset generation."""
    
    @pytest.mark.parametrize("rows", [1000, 10000, 100000])
    def test_sales_generation_performance(self, rows, performance_monitor):
        """Test sales dataset generation performance for different sizes."""
        monitor = performance_monitor
        monitor.start()
        
        # Generate dataset
        data = tempdataset.create_dataset('sales', rows=rows)
        
        metrics = monitor.stop()
        
        # Verify data was generated correctly
        assert data is not None
        assert data.shape[0] == rows
        assert data.shape[1] == 30  # Sales dataset has 30 columns
        
        # Performance assertions
        print(f"\nPerformance metrics for {rows} rows:")
        print(f"  Duration: {metrics['duration']:.2f} seconds")
        print(f"  Memory used: {metrics['memory_used_mb']:.2f} MB")
        
        # Performance requirements from spec: 10K+ rows in <30 seconds
        if rows >= 10000:
            assert metrics['duration'] < 30.0, f"Generation of {rows} rows took {metrics['duration']:.2f}s, should be <30s"
        
        # Memory usage should be reasonable (rough estimate: <10MB per 10K rows)
        expected_memory_mb = (rows / 10000) * 10
        if PSUTIL_AVAILABLE and metrics['memory_used_mb'] > 0:
            assert metrics['memory_used_mb'] < expected_memory_mb * 2, f"Memory usage {metrics['memory_used_mb']:.2f}MB too high for {rows} rows"
    
    def test_performance_scaling(self, performance_monitor):
        """Test that performance scales reasonably with dataset size."""
        sizes = [1000, 5000, 10000]
        results = []
        
        for size in sizes:
            monitor = performance_monitor
            monitor.start()
            
            data = tempdataset.create_dataset('sales', rows=size)
            metrics = monitor.stop()
            
            results.append({
                'size': size,
                'duration': metrics['duration'],
                'memory_mb': metrics['memory_used_mb']
            })
            
            # Clean up
            del data
            gc.collect()
        
        # Check that performance scales reasonably (not exponentially)
        for i in range(1, len(results)):
            prev = results[i-1]
            curr = results[i]
            
            size_ratio = curr['size'] / prev['size']
            time_ratio = curr['duration'] / prev['duration'] if prev['duration'] > 0 else 1
            
            print(f"\nScaling from {prev['size']} to {curr['size']} rows:")
            print(f"  Size ratio: {size_ratio:.1f}x")
            print(f"  Time ratio: {time_ratio:.1f}x")
            
            # Time should scale roughly linearly (allow up to 2x for overhead)
            assert time_ratio < size_ratio * 2, f"Performance scaling too poor: {time_ratio:.1f}x time for {size_ratio:.1f}x data"


class TestFileIOPerformance:
    """Test performance of file I/O operations."""
    
    @pytest.mark.parametrize("rows", [1000, 10000, 50000])
    @pytest.mark.parametrize("file_format", ["csv", "json"])
    def test_file_write_performance(self, rows, file_format, temp_dir, performance_monitor):
        """Test file writing performance for different sizes and formats."""
        filename = os.path.join(temp_dir, f"test_data.{file_format}")
        
        monitor = performance_monitor
        monitor.start()
        
        # Generate and save to file
        tempdataset.create_dataset(filename, rows=rows)
        
        metrics = monitor.stop()
        
        # Verify file was created and has content
        assert os.path.exists(filename)
        assert os.path.getsize(filename) > 0
        
        print(f"\nFile write performance for {rows} rows ({file_format}):")
        print(f"  Duration: {metrics['duration']:.2f} seconds")
        print(f"  File size: {os.path.getsize(filename) / 1024 / 1024:.2f} MB")
        print(f"  Memory used: {metrics['memory_used_mb']:.2f} MB")
        
        # File I/O should be reasonably fast
        max_time = 60.0 if rows >= 50000 else 30.0
        assert metrics['duration'] < max_time, f"File write took {metrics['duration']:.2f}s, should be <{max_time}s"
    
    @pytest.mark.parametrize("rows", [1000, 10000, 50000])
    @pytest.mark.parametrize("file_format", ["csv", "json"])
    def test_file_read_performance(self, rows, file_format, temp_dir, performance_monitor):
        """Test file reading performance for different sizes and formats."""
        filename = os.path.join(temp_dir, f"test_data.{file_format}")
        
        # First create the file
        tempdataset.create_dataset(filename, rows=rows)
        
        # Now test reading performance
        monitor = performance_monitor
        monitor.start()
        
        if file_format == "csv":
            data = tempdataset.read_csv(filename)
        else:
            data = tempdataset.read_json(filename)
        
        metrics = monitor.stop()
        
        # Verify data was read correctly
        assert data is not None
        assert data.shape[0] == rows
        
        print(f"\nFile read performance for {rows} rows ({file_format}):")
        print(f"  Duration: {metrics['duration']:.2f} seconds")
        print(f"  Memory used: {metrics['memory_used_mb']:.2f} MB")
        
        # File reading should be reasonably fast
        max_time = 30.0 if rows >= 50000 else 15.0
        assert metrics['duration'] < max_time, f"File read took {metrics['duration']:.2f}s, should be <{max_time}s"


class TestMemoryUsagePatterns:
    """Test memory usage patterns for large datasets."""
    
    @pytest.mark.skipif(not PSUTIL_AVAILABLE, reason="psutil not available")
    def test_memory_usage_large_dataset(self, performance_monitor):
        """Test memory usage for large dataset generation."""
        rows = 100000
        
        # Get baseline memory
        baseline_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        monitor = performance_monitor
        monitor.start()
        
        # Generate large dataset
        data = tempdataset.create_dataset('sales', rows=rows)
        
        metrics = monitor.stop()
        
        # Verify data
        assert data.shape[0] == rows
        
        print(f"\nMemory usage for {rows} rows:")
        print(f"  Baseline: {baseline_memory:.2f} MB")
        print(f"  Peak usage: {metrics['memory_end_mb']:.2f} MB")
        print(f"  Memory increase: {metrics['memory_used_mb']:.2f} MB")
        
        # Memory usage should be reasonable (estimate: ~1-2MB per 1000 rows)
        expected_memory_mb = (rows / 1000) * 2
        assert metrics['memory_used_mb'] < expected_memory_mb * 2, f"Memory usage too high: {metrics['memory_used_mb']:.2f}MB"
        
        # Clean up and verify memory is released
        del data
        gc.collect()
        
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_released = metrics['memory_end_mb'] - final_memory
        
        print(f"  Memory after cleanup: {final_memory:.2f} MB")
        print(f"  Memory released: {memory_released:.2f} MB")
        
        # Should release most of the memory (allow 20% overhead)
        assert memory_released > metrics['memory_used_mb'] * 0.8, "Memory not properly released after cleanup"
    
    def test_memory_usage_streaming_files(self, temp_dir, performance_monitor):
        """Test memory usage when working with large files."""
        rows = 50000
        filename = os.path.join(temp_dir, "large_test.csv")
        
        # Generate large file
        tempdataset.create_dataset(filename, rows=rows)
        
        # Test reading with memory monitoring
        monitor = performance_monitor
        monitor.start()
        
        data = tempdataset.read_csv(filename)
        
        metrics = monitor.stop()
        
        print(f"\nMemory usage reading {rows} rows from file:")
        print(f"  Duration: {metrics['duration']:.2f} seconds")
        print(f"  Memory used: {metrics['memory_used_mb']:.2f} MB")
        print(f"  File size: {os.path.getsize(filename) / 1024 / 1024:.2f} MB")
        
        # Memory usage should be reasonable for file operations
        file_size_mb = os.path.getsize(filename) / 1024 / 1024
        if PSUTIL_AVAILABLE and metrics['memory_used_mb'] > 0:
            # Memory usage should not be more than 3x file size
            assert metrics['memory_used_mb'] < file_size_mb * 3, f"Memory usage {metrics['memory_used_mb']:.2f}MB too high for {file_size_mb:.2f}MB file"


class TestPerformanceRegression:
    """Test for performance regressions."""
    
    def test_performance_baseline(self, performance_monitor):
        """Establish performance baseline for regression testing."""
        test_cases = [
            {'rows': 1000, 'max_time': 5.0},
            {'rows': 10000, 'max_time': 25.0},
        ]
        
        results = []
        
        for case in test_cases:
            monitor = performance_monitor
            monitor.start()
            
            data = tempdataset.create_dataset('sales', rows=case['rows'])
            
            metrics = monitor.stop()
            
            results.append({
                'rows': case['rows'],
                'duration': metrics['duration'],
                'memory_mb': metrics['memory_used_mb']
            })
            
            # Performance regression check
            assert metrics['duration'] < case['max_time'], f"Performance regression: {case['rows']} rows took {metrics['duration']:.2f}s (max: {case['max_time']}s)"
            
            print(f"\nBaseline for {case['rows']} rows:")
            print(f"  Duration: {metrics['duration']:.2f}s (max: {case['max_time']}s)")
            print(f"  Memory: {metrics['memory_used_mb']:.2f}MB")
            
            # Clean up
            del data
            gc.collect()
        
        # Store results for future comparison
        return results


@pytest.mark.benchmark
class TestBenchmarks:
    """Benchmark tests using pytest-benchmark if available."""
    
    def test_benchmark_small_dataset(self, benchmark):
        """Benchmark small dataset generation."""
        result = benchmark(tempdataset.create_dataset, 'sales', 1000)
        assert result.shape[0] == 1000
    
    def test_benchmark_medium_dataset(self, benchmark):
        """Benchmark medium dataset generation."""
        result = benchmark(tempdataset.create_dataset, 'sales', 10000)
        assert result.shape[0] == 10000
    
    def test_benchmark_csv_write(self, benchmark, temp_dir):
        """Benchmark CSV file writing."""
        filename = os.path.join(temp_dir, "benchmark.csv")
        benchmark(tempdataset.create_dataset, filename, 5000)
        assert os.path.exists(filename)
    
    def test_benchmark_csv_read(self, benchmark, temp_dir):
        """Benchmark CSV file reading."""
        filename = os.path.join(temp_dir, "benchmark.csv")
        tempdataset.create_dataset(filename, 5000)  # Create file first
        
        result = benchmark(tempdataset.read_csv, filename)
        assert result.shape[0] == 5000


if __name__ == "__main__":
    # Run basic performance tests when executed directly
    print("Running basic performance tests...")
    
    monitor = PerformanceMonitor()
    
    # Test 10K rows generation
    print("\nTesting 10K rows generation...")
    monitor.start()
    data = tempdataset.create_dataset('sales', 10000)
    metrics = monitor.stop()
    
    print(f"Duration: {metrics['duration']:.2f} seconds")
    print(f"Memory used: {metrics['memory_used_mb']:.2f} MB")
    print(f"Rows generated: {data.shape[0]}")
    print(f"Columns: {data.shape[1]}")
    
    # Verify performance requirement
    if metrics['duration'] < 30.0:
        print("✓ Performance requirement met (10K+ rows in <30 seconds)")
    else:
        print("✗ Performance requirement failed")
    
    print("\nPerformance tests completed.")