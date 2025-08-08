# Contributing to TempDataset

Thank you for your interest in contributing to TempDataset! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and constructive in all interactions.

## Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/TempDataset.git
   cd TempDataset
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e .[dev]
   ```

4. **Verify Setup**
   ```bash
   pytest
   ```

## Development Workflow

### Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add type hints where appropriate
   - Update documentation as needed

3. **Add Tests**
   - Write tests for new functionality
   - Ensure existing tests still pass
   - Aim for high test coverage

4. **Run Quality Checks**
   ```bash
   # Format code
   black tempdataset tests
   
   # Lint code
   flake8 tempdataset tests
   
   # Type checking
   mypy tempdataset
   
   # Run tests
   pytest
   ```

### Testing

We use pytest for testing. Tests are organized in the `tests/` directory:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tempdataset

# Run specific test categories
pytest -m "not slow"          # Skip slow tests
pytest -m integration         # Integration tests only
pytest -m performance         # Performance tests only

# Run specific test file
pytest tests/test_core_functionality.py
```

### Performance Testing

Performance is important for TempDataset. Run benchmarks to ensure changes don't degrade performance:

```bash
# Run performance benchmarks
pytest .benchmarks/

# Run with detailed output
pytest .benchmarks/ -v --benchmark-verbose
```

## Code Style

### Python Style Guide

- Follow PEP 8
- Use Black for code formatting
- Maximum line length: 88 characters
- Use type hints for all public functions
- Write docstrings for all public functions and classes

### Example Code Style

```python
def generate_data(dataset_type: str, rows: int = 500) -> TempDataFrame:
    """
    Generate temporary dataset.
    
    Args:
        dataset_type: Type of dataset to generate
        rows: Number of rows to generate
        
    Returns:
        TempDataFrame containing generated data
        
    Raises:
        ValidationError: If parameters are invalid
        DataGenerationError: If generation fails
    """
    # Implementation here
    pass
```

### Documentation Style

- Use Google-style docstrings
- Include type information in docstrings
- Provide examples for complex functions
- Update README.md for user-facing changes

## Types of Contributions

### Bug Reports

When reporting bugs, please include:
- Python version and operating system
- TempDataset version
- Minimal code example that reproduces the issue
- Expected vs actual behavior
- Full error traceback if applicable

### Feature Requests

For new features:
- Describe the use case and motivation
- Provide examples of how the feature would be used
- Consider backward compatibility
- Discuss performance implications

### Code Contributions

We welcome:
- Bug fixes
- New dataset types
- Performance improvements
- Documentation improvements
- Test coverage improvements
- New utility functions

### Adding New Dataset Types

To add a new dataset type:

1. **Create Dataset Class**
   ```python
   # In tempdataset/core/datasets/your_dataset.py
   from ..base import BaseDataset
   
   class YourDataset(BaseDataset):
       def generate_row(self, row_index: int) -> dict:
           # Implementation
           pass
   ```

2. **Register Dataset**
   ```python
   # In tempdataset/__init__.py
   from .core.datasets.your_dataset import YourDataset
   _generator.register_dataset('your_dataset', YourDataset)
   ```

3. **Add Tests**
   ```python
   # In tests/test_your_dataset.py
   def test_your_dataset_generation():
       data = tempdataset('your_dataset', 100)
       assert len(data) == 100
       # More specific tests
   ```

4. **Update Documentation**
   - Add to README.md
   - Include usage examples
   - Document any special features

## Pull Request Process

1. **Before Submitting**
   - Ensure all tests pass
   - Run code quality checks
   - Update documentation
   - Add changelog entry if needed

2. **Pull Request Description**
   - Clear title describing the change
   - Detailed description of what changed and why
   - Link to related issues
   - Screenshots for UI changes (if applicable)

3. **Review Process**
   - Maintainers will review your PR
   - Address feedback promptly
   - Keep PR focused and atomic
   - Rebase if requested

## Release Process

Releases follow semantic versioning:
- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

## Performance Guidelines

- Profile code changes with large datasets
- Consider memory usage for large datasets
- Benchmark critical paths
- Document performance characteristics
- Avoid unnecessary dependencies

## Documentation

### API Documentation

- All public functions must have docstrings
- Include parameter types and descriptions
- Provide usage examples
- Document exceptions that may be raised

### User Documentation

- Update README.md for user-facing changes
- Add examples for new features
- Keep documentation current with code changes
- Consider adding tutorials for complex features

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Bugs**: Create an issue with detailed information
- **Features**: Discuss in issues before implementing
- **Code Review**: Tag maintainers for review

## Recognition

Contributors are recognized in:
- CHANGELOG.md for significant contributions
- README.md acknowledgments
- GitHub contributors page

Thank you for contributing to TempDataset! 🎉