Dataset Reference
=================

TempDataset provides 7 comprehensive datasets for various use cases. Each dataset is carefully designed with realistic data patterns and relationships.

Available Datasets
------------------

Sales Dataset
~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('sales', rows)``

**Columns:** 27

**Description:** Complete sales transaction data with order information, customer details, product data, financial calculations, and geographic information.

**Key Features:**
- Realistic transaction IDs and order tracking
- Customer demographics and segmentation  
- Product catalog with categories and brands
- Financial calculations with discounts and profit
- Geographic distribution across regions
- Shipping and delivery logistics

**Column Schema:**

.. code-block:: text

   order_id           : string   - Unique order identifier (ORD-YYYY-NNNNNN)
   customer_id        : string   - Customer identifier (CUST-NNNN)
   customer_name      : string   - Customer full name
   customer_email     : string   - Customer email address
   product_id         : string   - Product identifier (PROD-AAANNN)
   product_name       : string   - Product name
   category           : string   - Product category (Electronics, Clothing, etc.)
   subcategory        : string   - Product subcategory
   brand              : string   - Product brand
   quantity           : integer  - Quantity ordered
   unit_price         : float    - Price per unit
   total_price        : float    - Total before discount
   discount           : float    - Discount amount
   final_price        : float    - Final price after discount
   order_date         : date     - Order date
   ship_date          : date     - Shipping date
   delivery_date      : date     - Delivery date
   sales_rep          : string   - Sales representative
   region             : string   - Geographic region
   country            : string   - Country
   state/province     : string   - State or province
   city               : string   - City
   postal_code        : string   - Postal code
   customer_segment   : string   - Customer segment (Consumer, Corporate, Home Office)
   order_priority     : string   - Order priority level
   shipping_mode      : string   - Shipping method
   payment_method     : string   - Payment method
   customer_age       : integer  - Customer age
   customer_gender    : string   - Customer gender
   profit             : float    - Profit amount

**Example Usage:**

.. code-block:: python

   import tempdataset
   
   # Generate sales data
   sales = tempdataset.create_dataset('sales', 1000)
   
   # Analyze high-value transactions
   high_value = sales.filter(lambda row: row['final_price'] > 500)
   
   # Export regional data
   north_region = sales.filter(lambda row: row['region'] == 'North')
   north_region.to_csv('north_sales.csv')

Customers Dataset
~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('customers', rows)``

**Columns:** 31

**Description:** Comprehensive customer profiles with personal information, demographics, purchase history, and loyalty data.

**Key Features:**
- Complete personal and contact information
- Professional and demographic details
- Purchase history and spending patterns
- Loyalty program participation
- Account status and preferences
- Geographic distribution

**Column Schema:**

.. code-block:: text

   customer_id            : string    - Unique customer identifier
   first_name             : string    - First name
   last_name              : string    - Last name
   full_name              : string    - Full name
   email                  : string    - Email address
   phone_number           : string    - International phone number
   gender                 : string    - Gender
   date_of_birth          : date      - Birth date
   age                    : integer   - Age
   marital_status         : string    - Marital status
   occupation             : string    - Job title
   company                : string    - Company name
   annual_income          : float     - Annual income
   street_address         : string    - Street address
   city                   : string    - City
   state_province         : string    - State or province
   postal_code            : string    - Postal code
   country                : string    - Country
   region                 : string    - Geographic region
   account_created_date   : datetime  - Account creation date
   last_purchase_date     : datetime  - Last purchase date
   total_orders           : integer   - Total number of orders
   total_spent            : float     - Total amount spent
   average_order_value    : float     - Average order value
   loyalty_member         : boolean   - Loyalty program membership
   loyalty_points         : integer   - Loyalty points balance
   preferred_payment_method : string  - Preferred payment method
   preferred_shipping_mode  : string  - Preferred shipping method
   newsletter_subscribed    : boolean - Newsletter subscription status
   customer_segment         : string  - Customer segment
   account_status          : string   - Account status
   notes                   : string   - Customer notes

E-commerce Dataset
~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('ecommerce', rows)``

**Columns:** 35+

**Description:** Advanced e-commerce transaction data with customer behavior, product details, reviews, returns, and digital metrics.

**Key Features:**
- Transaction details with timestamps
- Customer behavior and device information
- Product catalog with reviews and ratings
- Return and refund processing
- Digital metrics (conversion rates, sessions)
- Seller and marketplace data

Employees Dataset
~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('employees', rows)``

**Columns:** 30+

**Description:** Complete HR and employee management data with performance metrics, benefits, and organizational structure.

**Key Features:**
- Personal and contact information
- Job details and organizational structure
- Performance ratings and reviews
- Compensation and benefits data
- Skills and certifications
- Training and development records

Marketing Dataset
~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('marketing', rows)``

**Columns:** 32+

**Description:** Marketing campaign performance data with channel metrics, ROI analysis, and audience insights.

**Key Features:**
- Campaign identification and metadata
- Multi-channel performance metrics
- ROI and conversion analysis
- Audience demographics and targeting
- Budget allocation and spending
- Attribution and touch point analysis

Retail Dataset
~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('retail', rows)``

**Columns:** 28+

**Description:** In-store retail operations data with point-of-sale transactions, inventory management, and store operations.

**Key Features:**
- Point-of-sale transaction data
- Inventory levels and stock management
- Store location and staff information
- Seasonal trends and patterns
- Customer loyalty card integration
- Shift and operational data

Suppliers Dataset
~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('suppliers', rows)``

**Columns:** 22+

**Description:** Supplier and vendor management data with performance metrics, contract information, and quality ratings.

**Key Features:**
- Supplier company profiles
- Performance and quality metrics
- Contract terms and conditions
- Delivery performance tracking
- Financial and credit information
- Geographic coverage areas

Getting Help
------------

Use the built-in help functions to explore datasets:

.. code-block:: python

   import tempdataset
   
   # Comprehensive help with examples
   tempdataset.help()
   
   # Quick dataset overview
   tempdataset.list_datasets()
   
   # Explore specific dataset structure
   data = tempdataset.create_dataset('sales', 10)
   print(data.columns)

Common Patterns
---------------

All datasets follow these common patterns:

**ID Generation:** Sequential IDs with realistic formatting
**Dates:** Proper chronological relationships between related dates  
**Geographic Data:** Consistent country, state, and city relationships
**Financial Data:** Realistic pricing with proper calculations
**Demographics:** Age-appropriate and statistically realistic distributions
**Relationships:** Logical correlations between related fields

**Data Quality:** All datasets include:
- Proper data types for each column
- Realistic value distributions  
- Consistent formatting
- Logical relationships between fields
- No missing values (except where realistic)
