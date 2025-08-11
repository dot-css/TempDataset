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

* **40 Comprehensive Datasets**: Business, Financial, Technology, Healthcare, IoT Sensors, and Social Media  
* **Technology Focus**: New datasets for DevOps monitoring, web analytics, and system performance
* **Lightweight**: Zero dependencies for core functionality
* **Multiple Formats**: Generate CSV, JSON, or in-memory datasets
* **Realistic Data**: Built-in datasets with realistic patterns and relationships
* **Extensible**: Easy to add custom dataset types
* **Memory Efficient**: Optimized for large dataset generation
* **Built-in Help**: Interactive help system with `tempdataset.help()` and `tempdataset.list_datasets()`
* **Python 3.7+**: Compatible with modern Python versions

Quick Example
-------------

.. code-block:: python

   import tempdataset

   # Get comprehensive help
   tempdataset.help()
   
   # Generate any of the 40 available datasets
   sales_data = tempdataset.create_dataset('sales', 1000)
   customers = tempdataset.create_dataset('customers', 500)
   banking = tempdataset.create_dataset('banking', 800)
   weather = tempdataset.create_dataset('weather', 1200)

   # Save directly to files
   tempdataset.create_dataset('employees.csv', 300)
   tempdataset.create_dataset('web_analytics.json', 600)

Dataset Categories
------------------

**Core Business (10 datasets)**
* **CRM**: Customer relationship management data
* **Customers**: Customer profiles and demographics  
* **E-commerce**: E-commerce transactions and reviews
* **Employees**: HR data with performance metrics
* **Inventory**: Warehouse and inventory management
* **Marketing**: Campaign data with ROI analysis
* **Retail**: In-store operations and POS data
* **Reviews**: Product and service reviews
* **Sales**: Transaction data with order details
* **Suppliers**: Vendor management and contracts

**Financial (8 datasets)**
* **Stocks**: Stock market trading data
* **Banking**: Banking transactions and accounts
* **Cryptocurrency**: Crypto trading and wallets
* **Insurance**: Policies and claims processing
* **Loans**: Loan applications and management
* **Investments**: Investment portfolios and performance
* **Accounting**: General ledger and financial records
* **Payments**: Digital payment processing

**IoT Sensors (6 datasets)**
* **Weather**: Weather sensor monitoring
* **Energy**: Smart meter energy consumption
* **Traffic**: Traffic sensor and flow data
* **Environmental**: Air quality and pollution monitoring
* **Industrial**: Manufacturing sensor data
* **Smart Home**: IoT device monitoring

**Healthcare (6 datasets)**
* **Patients**: Patient medical records
* **Appointments**: Medical appointment scheduling
* **Lab Results**: Laboratory test results
* **Prescriptions**: Medication prescriptions
* **Medical History**: Patient medical history
* **Clinical Trials**: Clinical trial participant data

**Social Media (2 datasets)**
* **Social Media**: Posts, engagement, and metrics
* **User Profiles**: Social media user profiles

**Technology (8 datasets)**
* **Web Analytics**: Website traffic and user behavior
* **App Usage**: Mobile app usage analytics
* **System Logs**: System and application logs
* **API Calls**: API performance and usage
* **Server Metrics**: Server performance monitoring
* **User Sessions**: User session tracking
* **Error Logs**: Application error tracking
* **Performance**: Application performance monitoring

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`