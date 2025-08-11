Quick Start Guide
=================

Getting Help
------------

First, explore what's available:

.. code-block:: python

   import tempdataset

   # Get comprehensive help and examples
   tempdataset.help()
   
   # Quick overview of all datasets
   tempdataset.list_datasets()

Basic Usage
-----------

Generate In-Memory Datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate any of the 40 available datasets across 6 categories
   
   # Core Business datasets
   sales_data = tempdataset.create_dataset('sales', 1000)
   customers = tempdataset.create_dataset('customers', 500)
   crm = tempdataset.create_dataset('crm', 300)
   
   # Financial datasets
   banking = tempdataset.create_dataset('banking', 800)
   stocks = tempdataset.create_dataset('stocks', 1200)
   
   # IoT Sensors datasets
   weather = tempdataset.create_dataset('weather', 2000)
   energy = tempdataset.create_dataset('energy', 1500)
   
   # Healthcare datasets
   patients = tempdataset.create_dataset('patients', 400)
   lab_results = tempdataset.create_dataset('lab_results', 1000)
   
   # Technology datasets
   web_analytics = tempdataset.create_dataset('web_analytics', 5000)
   api_calls = tempdataset.create_dataset('api_calls', 10000)
   
   # Social Media datasets
   social_media = tempdataset.create_dataset('social_media', 2000)
   
   # View the data
   print(f"Generated {len(sales_data)} sales records")
   sales_data.head()

Save Directly to Files
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Save any dataset to CSV
   tempdataset.create_dataset('sales_data.csv', 1000)
   tempdataset.create_dataset('customer_profiles.csv', 500)
   
   # Save any dataset to JSON
   tempdataset.create_dataset('ecommerce_transactions.json', 800)
   tempdataset.create_dataset('employee_records.json', 300)

Read Data Back
~~~~~~~~~~~~~~

.. code-block:: python

   # Read CSV data
   sales_data = tempdataset.read_csv('sales_data.csv')
   customers = tempdataset.read_csv('customer_profiles.csv')
   
   # Read JSON data
   ecommerce = tempdataset.read_json('ecommerce_transactions.json')
   employees = tempdataset.read_json('employee_records.json')

Explore Dataset Structure
-------------------------

.. code-block:: python

   # Generate a small sample to explore structure
   sample = tempdataset.create_dataset('sales', 10)
   
   print(f"Dataset shape: {sample.shape}")
   print(f"Columns: {list(sample.columns)}")
   print(f"Data types: {sample.dtypes}")

Working with Data
-----------------

.. code-block:: python

   data = tempdataset.create_dataset('customers', 1000)

   # Basic operations
   data.head(10)          # First 10 rows
   data.tail(5)           # Last 5 rows
   data.describe()        # Statistical summary
   data.info()            # Data information
   data.memory_usage()    # Memory usage details

   # Data filtering and selection
   vip_customers = data.filter(lambda row: row['loyalty_member'] and row['total_spent'] > 5000)
   contact_info = data.select(['full_name', 'email', 'phone_number'])

   # Export options
   data.to_csv('customers.csv')
   data.to_json('customers.json')
   dict_data = data.to_dict()

Dataset-Specific Examples
-------------------------

Sales Analysis
~~~~~~~~~~~~~~

.. code-block:: python

   sales = tempdataset.create_dataset('sales', 2000)
   
   # High-value transactions
   premium_sales = sales.filter(lambda row: row['final_price'] > 500)
   
   # Regional analysis
   west_region = sales.filter(lambda row: row['region'] == 'West')
   
   # Product category performance
   electronics = sales.filter(lambda row: row['category'] == 'Electronics')

Customer Segmentation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   customers = tempdataset.create_dataset('customers', 1000)
   
   # Loyalty program members
   loyalty_members = customers.filter(lambda row: row['loyalty_member'])
   
   # High-value customers
   big_spenders = customers.filter(lambda row: row['total_spent'] > 10000)
   
   # Active customers
   active_customers = customers.filter(lambda row: row['account_status'] == 'Active')

E-commerce Analytics
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   ecommerce = tempdataset.create_dataset('ecommerce', 1500)
   
   # High-rated products
   top_rated = ecommerce.filter(lambda row: row['customer_rating'] >= 4.5)
   
   # Mobile transactions
   mobile_sales = ecommerce.filter(lambda row: row['device_type'] == 'Mobile')

Performance Monitoring
----------------------

.. code-block:: python

   import tempdataset

   # Generate large dataset
   data = tempdataset.create_dataset('retail', 50000)

   # Check performance stats
   stats = tempdataset.get_performance_stats()
   print(f"Generation time: {stats['generation_time']:.2f}s")
   print(f"Memory usage: {stats['memory_usage']:.2f}MB")

   # Reset stats for next operation
   tempdataset.reset_performance_stats()

All Available Datasets
-----------------------

.. code-block:: python

   # All 40 datasets organized by category
   datasets_by_category = {
       'Core Business': ['crm', 'customers', 'ecommerce', 'employees', 'inventory', 
                        'marketing', 'retail', 'reviews', 'sales', 'suppliers'],
       'Financial': ['stocks', 'banking', 'cryptocurrency', 'insurance', 'loans', 
                    'investments', 'accounting', 'payments'],
       'IoT Sensors': ['weather', 'energy', 'traffic', 'environmental', 'industrial', 'smarthome'],
       'Healthcare': ['patients', 'appointments', 'lab_results', 'prescriptions', 
                     'medical_history', 'clinical_trials'],
       'Social Media': ['social_media', 'user_profiles'],
       'Technology': ['web_analytics', 'app_usage', 'system_logs', 'api_calls', 
                     'server_metrics', 'user_sessions', 'error_logs', 'performance']
   }
   
   # Generate sample of each dataset by category
   for category, dataset_list in datasets_by_category.items():
       print(f"\n{category} Datasets:")
       for dataset_name in dataset_list:
           data = tempdataset.create_dataset(dataset_name, 10)
           print(f"  {dataset_name}: {data.shape[1]} columns")
       
   # Or use the helper function to see all datasets with descriptions
   tempdataset.list_datasets()

Dataset Categories Quick Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Quick examples from each category
   
   # Core Business (10 datasets)
   sales = tempdataset.create_dataset('sales', 100)
   customers = tempdataset.create_dataset('customers', 100)
   
   # Financial (8 datasets) 
   banking = tempdataset.create_dataset('banking', 100)
   stocks = tempdataset.create_dataset('stocks', 100)
   
   # IoT Sensors (6 datasets)
   weather = tempdataset.create_dataset('weather', 100)
   energy = tempdataset.create_dataset('energy', 100)
   
   # Healthcare (6 datasets)
   patients = tempdataset.create_dataset('patients', 100)
   lab_results = tempdataset.create_dataset('lab_results', 100)
   
   # Social Media (2 datasets)
   social_media = tempdataset.create_dataset('social_media', 100)
   
   # Technology (8 datasets)
   web_analytics = tempdataset.create_dataset('web_analytics', 100)
   api_calls = tempdataset.create_dataset('api_calls', 100)