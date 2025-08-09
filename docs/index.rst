TempDataset Documentation
========================

A lightweight Python library for generating realistic temporary datasets for testing and development.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   datasets
   api
   examples
   contributing
   changelog

Features
--------

* **7 Comprehensive Datasets**: Sales, Customers, E-commerce, Employees, Marketing, Retail, and Suppliers
* **Lightweight**: Zero dependencies for core functionality
* **Multiple Formats**: Generate CSV, JSON, or in-memory datasets
* **Realistic Data**: Built-in datasets with realistic patterns and relationships
* **Extensible**: Easy to add custom dataset types
* **Memory Efficient**: Optimized for large dataset generation
* **Built-in Help**: Interactive help system with `tempdataset.help()`
* **Python 3.7+**: Compatible with modern Python versions

Quick Example
-------------

.. code-block:: python

   import tempdataset

   # Get comprehensive help
   tempdataset.help()
   
   # Generate any of the 7 available datasets
   sales_data = tempdataset.create_dataset('sales', 1000)
   customers = tempdataset.create_dataset('customers', 500)
   ecommerce = tempdataset.create_dataset('ecommerce', 800)

   # Save directly to files
   tempdataset.create_dataset('employees.csv', 300)
   tempdataset.create_dataset('marketing.json', 600)

Available Datasets
------------------

* **Sales** (27 columns): Transaction data with order details, customer info, and financial metrics
* **Customers** (31 columns): Customer profiles with demographics and purchase history  
* **E-commerce** (35+ columns): Advanced transaction data with reviews and digital metrics
* **Employees** (30+ columns): HR data with performance metrics and benefits
* **Marketing** (32+ columns): Campaign data with ROI analysis and channel performance
* **Retail** (28+ columns): In-store operations with inventory and staff data
* **Suppliers** (22+ columns): Vendor management with quality ratings and contracts

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`