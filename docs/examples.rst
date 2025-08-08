Examples
========

Sales Dataset Examples
----------------------

Basic Sales Data Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate sales data
   sales = tempdataset.create_dataset('sales', 1000)
   
   # View structure
   print(f"Shape: {sales.shape}")
   print(f"Columns: {sales.columns}")
   
   # View sample data
   print(sales.head())

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate large dataset
   data = tempdataset.create_dataset('sales', 50000)

   # Check performance stats
   stats = tempdataset.get_performance_stats()
   print(f"Generation time: {stats['generation_time']:.2f}s")
   print(f"Memory usage: {stats['memory_usage']:.2f}MB")

Data Analysis Example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate sales data
   data = tempdataset.create_dataset('sales', 5000)

   # Filter high-value transactions
   high_value = data.filter(lambda row: row['amount'] > 1000)
   
   # Select specific columns
   summary = data.select(['customer_name', 'amount', 'date'])
   
   # Export for analysis
   summary.to_csv('sales_summary.csv')