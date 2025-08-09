Examples
========

Getting Started
---------------

Help and Dataset Discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Get comprehensive help
   tempdataset.help()

   # List available datasets
   tempdataset.list_datasets()

All Available Datasets
-----------------------

Sales Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate sales transaction data (27 columns)
   sales = tempdataset.create_dataset('sales', 1000)
   
   # View structure
   print(f"Shape: {sales.shape}")
   print(f"Columns: {sales.columns}")
   
   # View sample data
   print(sales.head())

   # Filter high-value transactions
   high_value = sales.filter(lambda row: row['final_price'] > 500)

Customers Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate customer profiles (31 columns)
   customers = tempdataset.create_dataset('customers', 500)
   
   # Analyze customer segments
   vip_customers = customers.filter(lambda row: row['loyalty_member'] and row['total_spent'] > 5000)
   
   # Export customer data
   customers.to_csv('customer_profiles.csv')

E-commerce Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate e-commerce data (35+ columns)
   ecommerce = tempdataset.create_dataset('ecommerce', 2000)
   
   # Analyze reviews and returns
   high_rated = ecommerce.filter(lambda row: row['customer_rating'] >= 4.5)
   returned_items = ecommerce.filter(lambda row: row['return_status'] == 'Returned')

Employees Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate employee records (30+ columns)
   employees = tempdataset.create_dataset('employees', 300)
   
   # HR analytics
   high_performers = employees.filter(lambda row: row['performance_rating'] >= 4.0)
   it_department = employees.filter(lambda row: 'IT' in row['department'])

Marketing Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate marketing campaign data (32+ columns)
   marketing = tempdataset.create_dataset('marketing', 1000)
   
   # Campaign analysis
   high_roi = marketing.filter(lambda row: row['roi'] > 3.0)
   social_campaigns = marketing.filter(lambda row: 'Social' in row['channel'])

Retail Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate retail operations data (28+ columns)
   retail = tempdataset.create_dataset('retail', 1500)
   
   # Store performance
   weekend_sales = retail.filter(lambda row: row['day_of_week'] in ['Saturday', 'Sunday'])
   low_inventory = retail.filter(lambda row: row['inventory_level'] < 10)

Suppliers Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate supplier data (22+ columns)
   suppliers = tempdataset.create_dataset('suppliers', 200)
   
   # Supplier analysis
   top_suppliers = suppliers.filter(lambda row: row['quality_rating'] >= 4.5)
   reliable_delivery = suppliers.filter(lambda row: row['delivery_performance'] >= 95)

File Operations
---------------

Direct File Generation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate and save to CSV
   tempdataset.create_dataset('sales_data.csv', 1000)
   tempdataset.create_dataset('customer_data.csv', 500)
   
   # Generate and save to JSON
   tempdataset.create_dataset('ecommerce_data.json', 800)
   tempdataset.create_dataset('marketing_data.json', 600)

   # Read data back
   sales_data = tempdataset.read_csv('sales_data.csv')
   marketing_data = tempdataset.read_json('marketing_data.json')

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate large dataset
   data = tempdataset.create_dataset('ecommerce', 50000)

   # Check performance stats
   stats = tempdataset.get_performance_stats()
   print(f"Generation time: {stats['generation_time']:.2f}s")
   print(f"Memory usage: {stats['memory_usage']:.2f}MB")

   # Reset stats for next operation
   tempdataset.reset_performance_stats()

Advanced Data Analysis
----------------------

Multi-Dataset Analysis
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate related datasets
   customers = tempdataset.create_dataset('customers', 1000)
   sales = tempdataset.create_dataset('sales', 5000)
   marketing = tempdataset.create_dataset('marketing', 500)

   # Cross-dataset analysis
   vip_customers = customers.filter(lambda row: row['loyalty_member'])
   high_value_sales = sales.filter(lambda row: row['final_price'] > 1000)
   successful_campaigns = marketing.filter(lambda row: row['conversion_rate'] > 0.05)

Data Export and Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate and export multiple formats
   data = tempdataset.create_dataset('retail', 2000)
   
   # Export options
   data.to_csv('retail_analysis.csv')
   data.to_json('retail_data.json')
   
   # Convert to dictionary for further processing
   dict_data = data.to_dict()
   
   # Select specific columns for reports
   summary = data.select(['store_id', 'total_sales', 'date', 'staff_id'])
   summary.to_csv('daily_summary.csv')

Dataset Schema Exploration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Explore dataset structure
   for dataset_name in ['sales', 'customers', 'ecommerce', 'employees']:
       data = tempdataset.create_dataset(dataset_name, 10)  # Small sample
       print(f"\n{dataset_name.upper()} Dataset:")
       print(f"Columns ({len(data.columns)}): {list(data.columns)}")
       print(f"Sample data:\n{data.head(3)}")