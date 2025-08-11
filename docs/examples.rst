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

   # List all 40 available datasets by category
   tempdataset.list_datasets()

Core Business Dataset Examples
------------------------------

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

CRM Dataset Examples
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate CRM data with lead tracking
   crm = tempdataset.create_dataset('crm', 800)
   
   # Analyze sales pipeline
   hot_leads = crm.filter(lambda row: row['lead_score'] > 80)
   closed_deals = crm.filter(lambda row: row['deal_status'] == 'Closed Won')

Financial Dataset Examples
--------------------------

Banking Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate banking transaction data
   banking = tempdataset.create_dataset('banking', 2000)
   
   # Fraud detection analysis
   suspicious = banking.filter(lambda row: row['fraud_score'] > 0.7)
   high_value = banking.filter(lambda row: row['transaction_amount'] > 10000)

Stocks Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate stock market data
   stocks = tempdataset.create_dataset('stocks', 1500)
   
   # Market analysis
   high_volume = stocks.filter(lambda row: row['volume'] > 1000000)
   tech_stocks = stocks.filter(lambda row: row['sector'] == 'Technology')

Cryptocurrency Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate crypto trading data
   crypto = tempdataset.create_dataset('cryptocurrency', 1000)
   
   # Trading analysis
   bitcoin_trades = crypto.filter(lambda row: row['symbol'] == 'BTC')
   large_trades = crypto.filter(lambda row: row['trade_value'] > 50000)

IoT Sensors Dataset Examples
----------------------------

Weather Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate weather sensor data
   weather = tempdataset.create_dataset('weather', 2000)
   
   # Climate analysis
   extreme_temps = weather.filter(lambda row: row['temperature'] > 35 or row['temperature'] < -10)
   high_humidity = weather.filter(lambda row: row['humidity'] > 80)

Energy Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate smart meter energy data
   energy = tempdataset.create_dataset('energy', 1500)
   
   # Energy consumption analysis
   peak_usage = energy.filter(lambda row: row['consumption_kwh'] > 50)
   renewable_gen = energy.filter(lambda row: row['solar_generation'] > 0)

Healthcare Dataset Examples
---------------------------

Patients Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate patient medical records
   patients = tempdataset.create_dataset('patients', 500)
   
   # Medical analysis
   high_risk = patients.filter(lambda row: row['risk_score'] > 7)
   chronic_conditions = patients.filter(lambda row: len(row['conditions']) > 2)

Lab Results Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate laboratory test results
   lab_results = tempdataset.create_dataset('lab_results', 1000)
   
   # Clinical analysis
   abnormal_results = lab_results.filter(lambda row: row['result_flag'] == 'Abnormal')
   urgent_tests = lab_results.filter(lambda row: row['priority'] == 'STAT')

Technology Dataset Examples
---------------------------

Web Analytics Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate web analytics data
   web_analytics = tempdataset.create_dataset('web_analytics', 5000)
   
   # Traffic analysis
   mobile_users = web_analytics.filter(lambda row: row['device_type'] == 'Mobile')
   high_engagement = web_analytics.filter(lambda row: row['session_duration'] > 300)

API Calls Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate API performance data
   api_calls = tempdataset.create_dataset('api_calls', 10000)
   
   # Performance analysis
   slow_requests = api_calls.filter(lambda row: row['response_time'] > 1000)
   error_requests = api_calls.filter(lambda row: row['status_code'] >= 400)

Social Media Dataset Examples
-----------------------------

Social Media Dataset Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate social media posts data
   social_media = tempdataset.create_dataset('social_media', 3000)
   
   # Engagement analysis
   viral_posts = social_media.filter(lambda row: row['likes'] > 1000)
   trending_hashtags = social_media.filter(lambda row: '#trending' in row['hashtags'])

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
Co
mplete Dataset Category Examples
----------------------------------

All Core Business Datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate all core business datasets
   crm = tempdataset.create_dataset('crm', 500)
   customers = tempdataset.create_dataset('customers', 1000)
   ecommerce = tempdataset.create_dataset('ecommerce', 2000)
   employees = tempdataset.create_dataset('employees', 300)
   inventory = tempdataset.create_dataset('inventory', 800)
   marketing = tempdataset.create_dataset('marketing', 600)
   retail = tempdataset.create_dataset('retail', 1500)
   reviews = tempdataset.create_dataset('reviews', 1200)
   sales = tempdataset.create_dataset('sales', 2500)
   suppliers = tempdataset.create_dataset('suppliers', 150)

All Financial Datasets
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate all financial datasets
   stocks = tempdataset.create_dataset('stocks', 2000)
   banking = tempdataset.create_dataset('banking', 3000)
   cryptocurrency = tempdataset.create_dataset('cryptocurrency', 1500)
   insurance = tempdataset.create_dataset('insurance', 800)
   loans = tempdataset.create_dataset('loans', 1000)
   investments = tempdataset.create_dataset('investments', 600)
   accounting = tempdataset.create_dataset('accounting', 2000)
   payments = tempdataset.create_dataset('payments', 5000)

All IoT Sensors Datasets
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate all IoT sensor datasets
   weather = tempdataset.create_dataset('weather', 10000)
   energy = tempdataset.create_dataset('energy', 8000)
   traffic = tempdataset.create_dataset('traffic', 15000)
   environmental = tempdataset.create_dataset('environmental', 5000)
   industrial = tempdataset.create_dataset('industrial', 12000)
   smarthome = tempdataset.create_dataset('smarthome', 6000)

All Healthcare Datasets
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate all healthcare datasets
   patients = tempdataset.create_dataset('patients', 1000)
   appointments = tempdataset.create_dataset('appointments', 2000)
   lab_results = tempdataset.create_dataset('lab_results', 3000)
   prescriptions = tempdataset.create_dataset('prescriptions', 2500)
   medical_history = tempdataset.create_dataset('medical_history', 1500)
   clinical_trials = tempdataset.create_dataset('clinical_trials', 500)

All Technology Datasets
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate all technology datasets
   web_analytics = tempdataset.create_dataset('web_analytics', 20000)
   app_usage = tempdataset.create_dataset('app_usage', 15000)
   system_logs = tempdataset.create_dataset('system_logs', 50000)
   api_calls = tempdataset.create_dataset('api_calls', 100000)
   server_metrics = tempdataset.create_dataset('server_metrics', 25000)
   user_sessions = tempdataset.create_dataset('user_sessions', 30000)
   error_logs = tempdataset.create_dataset('error_logs', 10000)
   performance = tempdataset.create_dataset('performance', 40000)

Real-World Use Cases
--------------------

E-commerce Analytics Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate comprehensive e-commerce data
   customers = tempdataset.create_dataset('customers', 5000)
   sales = tempdataset.create_dataset('sales', 25000)
   reviews = tempdataset.create_dataset('reviews', 8000)
   web_analytics = tempdataset.create_dataset('web_analytics', 100000)
   
   # Customer segmentation analysis
   premium_customers = customers.filter(lambda row: row['total_spent'] > 2000)
   
   # Sales performance analysis
   high_value_orders = sales.filter(lambda row: row['final_price'] > 500)
   
   # Review sentiment analysis
   positive_reviews = reviews.filter(lambda row: row['rating'] >= 4)
   
   # Web traffic analysis
   converting_sessions = web_analytics.filter(lambda row: row['conversion'] == True)

Financial Risk Assessment
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate financial risk data
   banking = tempdataset.create_dataset('banking', 10000)
   loans = tempdataset.create_dataset('loans', 3000)
   insurance = tempdataset.create_dataset('insurance', 5000)
   
   # Risk analysis
   high_risk_transactions = banking.filter(lambda row: row['fraud_score'] > 0.8)
   defaulted_loans = loans.filter(lambda row: row['loan_status'] == 'Default')
   high_claims = insurance.filter(lambda row: row['claim_amount'] > 50000)

Healthcare Data Analysis
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate healthcare analytics data
   patients = tempdataset.create_dataset('patients', 2000)
   appointments = tempdataset.create_dataset('appointments', 8000)
   lab_results = tempdataset.create_dataset('lab_results', 15000)
   
   # Clinical analysis
   high_risk_patients = patients.filter(lambda row: row['risk_score'] > 8)
   missed_appointments = appointments.filter(lambda row: row['status'] == 'No Show')
   critical_results = lab_results.filter(lambda row: row['result_flag'] == 'Critical')

IoT Monitoring Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate IoT sensor data
   weather = tempdataset.create_dataset('weather', 50000)
   energy = tempdataset.create_dataset('energy', 30000)
   traffic = tempdataset.create_dataset('traffic', 100000)
   
   # Environmental monitoring
   extreme_weather = weather.filter(lambda row: 
       row['temperature'] > 40 or row['temperature'] < -20)
   
   # Energy efficiency analysis
   peak_consumption = energy.filter(lambda row: row['consumption_kwh'] > 100)
   
   # Traffic optimization
   congested_areas = traffic.filter(lambda row: row['avg_speed'] < 20)

Performance Testing Datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate large datasets for performance testing
   large_sales = tempdataset.create_dataset('sales', 100000)
   large_logs = tempdataset.create_dataset('system_logs', 500000)
   large_api = tempdataset.create_dataset('api_calls', 1000000)
   
   # Monitor performance
   stats = tempdataset.get_performance_stats()
   print(f"Total generation time: {stats['generation_time']:.2f}s")
   print(f"Peak memory usage: {stats['memory_usage']:.2f}MB")

Batch File Generation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate multiple datasets and save to files
   datasets_config = [
       ('sales_q1.csv', 'sales', 10000),
       ('customers_active.csv', 'customers', 5000),
       ('web_traffic.json', 'web_analytics', 50000),
       ('financial_data.csv', 'banking', 20000),
       ('iot_sensors.json', 'weather', 25000)
   ]
   
   for filename, dataset_type, rows in datasets_config:
       print(f"Generating {filename}...")
       tempdataset.create_dataset(filename, rows)
       print(f"✓ Generated {filename} with {rows} rows")

Dataset Comparison and Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate datasets for comparison
   datasets_to_compare = ['sales', 'ecommerce', 'retail']
   
   for dataset_name in datasets_to_compare:
       data = tempdataset.create_dataset(dataset_name, 100)
       print(f"\n{dataset_name.upper()} Dataset Analysis:")
       print(f"Columns: {len(data.columns)}")
       print(f"Sample columns: {list(data.columns)[:5]}")
       print(f"Data types: {[type(data.data[0][col]).__name__ for col in list(data.columns)[:3]]}")

Custom Analysis Workflows
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Multi-step analysis workflow
   def analyze_business_performance():
       # Step 1: Generate core business data
       sales = tempdataset.create_dataset('sales', 5000)
       customers = tempdataset.create_dataset('customers', 2000)
       marketing = tempdataset.create_dataset('marketing', 500)
       
       # Step 2: Performance metrics
       total_revenue = sum(row['final_price'] for row in sales.data)
       avg_order_value = total_revenue / len(sales.data)
       
       # Step 3: Customer insights
       loyal_customers = customers.filter(lambda row: row['loyalty_member'])
       high_value_customers = customers.filter(lambda row: row['total_spent'] > 1000)
       
       # Step 4: Marketing effectiveness
       successful_campaigns = marketing.filter(lambda row: row['roi'] > 2.0)
       
       # Step 5: Export results
       sales.to_csv('business_analysis_sales.csv')
       loyal_customers.to_csv('loyal_customers.csv')
       successful_campaigns.to_csv('top_campaigns.csv')
       
       return {
           'total_revenue': total_revenue,
           'avg_order_value': avg_order_value,
           'loyal_customer_count': len(loyal_customers.data),
           'successful_campaign_count': len(successful_campaigns.data)
       }
   
   # Run the analysis
   results = analyze_business_performance()
   print("Business Performance Analysis Results:")
   for key, value in results.items():
       print(f"{key}: {value}")