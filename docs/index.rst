TempDataset Documentation
========================

A lightweight Python library for generating realistic temporary datasets for testing and development.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api
   examples
   contributing
   changelog

Features
--------

* **Lightweight**: Zero dependencies for core functionality
* **Multiple Formats**: Generate CSV, JSON, or in-memory datasets
* **Realistic Data**: Built-in datasets with realistic patterns
* **Extensible**: Easy to add custom dataset types
* **Memory Efficient**: Optimized for large dataset generation
* **Python 3.7+**: Compatible with modern Python versions

Quick Example
-------------

.. code-block:: python

   import tempdataset

   # Generate 1000 rows of sales data
   data = tempdataset.create_dataset('sales', 1000)
   print(data.head())

   # Save directly to CSV
   tempdataset.create_dataset('sales.csv', 500)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`