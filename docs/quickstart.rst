Quick Start Guide
=================

Basic Usage
-----------

Generate In-Memory Dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tempdataset

   # Generate 500 rows (default)
   data = tempdataset.create_dataset('sales')
   
   # Generate custom number of rows
   data = tempdataset.create_dataset('sales', 1000)
   
   # View the data
   data.head()

Save to Files
~~~~~~~~~~~~~

.. code-block:: python

   # Save directly to CSV
   tempdataset.create_dataset('sales.csv', 500)
   
   # Save directly to JSON
   tempdataset.create_dataset('sales.json', 500)

Read Data Back
~~~~~~~~~~~~~~

.. code-block:: python

   # Read CSV data
   csv_data = tempdataset.read_csv('sales.csv')
   
   # Read JSON data
   json_data = tempdataset.read_json('sales.json')

Working with Data
-----------------

.. code-block:: python

   data = tempdataset.create_dataset('sales', 1000)

   # Basic operations
   data.head(10)          # First 10 rows
   data.tail(5)           # Last 5 rows
   data.describe()        # Statistical summary
   data.info()            # Data info

   # Export options
   data.to_csv('output.csv')
   data.to_json('output.json')