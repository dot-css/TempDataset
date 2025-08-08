Installation
============

Requirements
------------

* Python 3.7 or higher
* No additional dependencies required for core functionality

Install from PyPI
-----------------

.. code-block:: bash

   pip install tempdataset

Install from Source
------------------

.. code-block:: bash

   pip install git+https://github.com/dot-css/TempDataset

Development Installation
-----------------------

.. code-block:: bash

   git clone https://github.com/dot-css/TempDataset.git
   cd TempDataset
   pip install -e .[dev]

Verify Installation
------------------

.. code-block:: python

   import tempdataset
   print(tempdataset.__version__)