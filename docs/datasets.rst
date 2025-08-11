Dataset Reference
=================

TempDataset provides 40 comprehensive datasets across 6 categories for various use cases. Each dataset is carefully designed with realistic data patterns and relationships.

Core Business Datasets (10)
----------------------------

CRM Dataset
~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('crm', rows)``

**Description:** Customer relationship management data with lead tracking, sales pipeline, and customer interactions.

**Key Features:**
- Lead and opportunity tracking
- Sales pipeline management
- Customer interaction history
- Revenue forecasting data
- Sales team performance metrics

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

Inventory Dataset
~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('inventory', rows)``

**Description:** Warehouse and inventory management data with stock levels, product information, and supply chain metrics.

**Key Features:**
- Product catalog and SKU management
- Stock levels and warehouse locations
- Supplier and vendor information
- Reorder points and lead times
- Cost and pricing data

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

Reviews Dataset
~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('reviews', rows)``

**Description:** Product and service reviews with ratings, sentiment analysis, and customer feedback data.

**Key Features:**
- Review ratings and sentiment scores
- Product and service categorization
- Customer demographics and purchase history
- Review helpfulness and verification
- Response and moderation data

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

Financial Datasets (8)
----------------------

Stocks Dataset
~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('stocks', rows)``

**Description:** Stock market trading data with prices, volumes, and market indicators.

**Key Features:**
- Stock symbols and company information
- OHLC (Open, High, Low, Close) pricing
- Trading volumes and market cap
- Technical indicators and ratios
- Sector and industry classification

Banking Dataset
~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('banking', rows)``

**Columns:** 20

**Description:** Banking transaction data with account details, transaction types, and fraud detection indicators.

**Key Features:**
- Account information and balances
- Transaction types and amounts
- Merchant and location data
- Fraud detection scores
- Currency and exchange rates

Cryptocurrency Dataset
~~~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('cryptocurrency', rows)``

**Description:** Cryptocurrency trading data with wallet addresses, transaction hashes, and market data.

**Key Features:**
- Cryptocurrency symbols and prices
- Wallet addresses and transaction IDs
- Trading volumes and market metrics
- Mining and staking information
- Exchange and platform data

Insurance Dataset
~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('insurance', rows)``

**Description:** Insurance policies and claims data with coverage details and risk assessment.

**Key Features:**
- Policy information and coverage types
- Claims processing and settlements
- Risk assessment and underwriting
- Premium calculations and payments
- Agent and broker information

Loans Dataset
~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('loans', rows)``

**Description:** Loan applications and management data with credit scores and repayment tracking.

**Key Features:**
- Loan application details
- Credit scores and risk assessment
- Repayment schedules and history
- Interest rates and terms
- Collateral and guarantor information

Investments Dataset
~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('investments', rows)``

**Description:** Investment portfolio data with asset allocation and performance tracking.

**Key Features:**
- Portfolio composition and allocation
- Asset performance and returns
- Risk metrics and volatility
- Investment strategies and goals
- Advisor and management fees

Accounting Dataset
~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('accounting', rows)``

**Description:** General ledger and accounting data with journal entries and financial statements.

**Key Features:**
- Chart of accounts and classifications
- Journal entries and transactions
- Balance sheet and income statement data
- Budget vs actual comparisons
- Audit trails and compliance

Payments Dataset
~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('payments', rows)``

**Description:** Digital payment processing data with transaction details and payment methods.

**Key Features:**
- Payment methods and processors
- Transaction amounts and fees
- Success rates and failure reasons
- Merchant and customer information
- Settlement and reconciliation data

IoT Sensors Datasets (6)
-------------------------

Weather Dataset
~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('weather', rows)``

**Description:** Weather sensor monitoring data with temperature, humidity, pressure, and atmospheric conditions.

**Key Features:**
- Temperature and humidity readings
- Atmospheric pressure and wind data
- Precipitation and weather conditions
- Air quality and visibility metrics
- Geographic coordinates and timestamps

Energy Dataset
~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('energy', rows)``

**Description:** Smart meter energy consumption data with usage patterns and billing information.

**Key Features:**
- Energy consumption readings
- Peak and off-peak usage patterns
- Billing and rate information
- Renewable energy generation
- Grid stability and load balancing

Traffic Dataset
~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('traffic', rows)``

**Description:** Traffic sensor and flow data with vehicle counts and congestion metrics.

**Key Features:**
- Vehicle counts and classifications
- Speed and congestion measurements
- Traffic light and signal data
- Incident and accident reporting
- Route optimization metrics

Environmental Dataset
~~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('environmental', rows)``

**Description:** Environmental monitoring data with air quality, pollution levels, and ecological metrics.

**Key Features:**
- Air quality indices and pollutants
- Water quality measurements
- Noise pollution levels
- Radiation and chemical sensors
- Ecological impact assessments

Industrial Dataset
~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('industrial', rows)``

**Description:** Manufacturing and industrial sensor data with equipment monitoring and production metrics.

**Key Features:**
- Equipment performance and maintenance
- Production line efficiency
- Quality control measurements
- Safety and compliance monitoring
- Energy consumption and optimization

Smart Home Dataset
~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('smarthome', rows)``

**Description:** Smart home IoT device data with automation, security, and energy management.

**Key Features:**
- Device status and automation rules
- Security system monitoring
- Energy usage optimization
- Environmental controls
- User preferences and schedules

Healthcare Datasets (6)
------------------------

Patients Dataset
~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('patients', rows)``

**Description:** Patient medical records with demographics, medical history, and treatment information.

**Key Features:**
- Patient demographics and contact info
- Medical history and conditions
- Insurance and billing information
- Emergency contacts and preferences
- Treatment plans and outcomes

Appointments Dataset
~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('appointments', rows)``

**Description:** Medical appointment scheduling data with provider information and visit details.

**Key Features:**
- Appointment scheduling and status
- Healthcare provider information
- Visit types and specialties
- Insurance verification and copays
- Follow-up and referral tracking

Lab Results Dataset
~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('lab_results', rows)``

**Description:** Laboratory test results with diagnostic information and reference ranges.

**Key Features:**
- Test types and methodologies
- Result values and reference ranges
- Quality control and validation
- Ordering physician information
- Turnaround times and priorities

Prescriptions Dataset
~~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('prescriptions', rows)``

**Description:** Medication prescriptions with dosage information and pharmacy data.

**Key Features:**
- Medication names and dosages
- Prescribing physician information
- Pharmacy and dispensing data
- Insurance coverage and copays
- Refill history and adherence

Medical History Dataset
~~~~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('medical_history', rows)``

**Description:** Patient medical history with chronic conditions, surgeries, and family history.

**Key Features:**
- Chronic conditions and diagnoses
- Surgical history and procedures
- Family medical history
- Allergies and adverse reactions
- Lifestyle and risk factors

Clinical Trials Dataset
~~~~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('clinical_trials', rows)``

**Description:** Clinical trial participant data with study protocols and outcome measures.

**Key Features:**
- Study protocols and phases
- Participant demographics and eligibility
- Treatment arms and randomization
- Outcome measures and endpoints
- Adverse events and safety monitoring

Social Media Datasets (2)
--------------------------

Social Media Dataset
~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('social_media', rows)``

**Description:** Social media posts and engagement data with metrics and user interactions.

**Key Features:**
- Post content and metadata
- Engagement metrics (likes, shares, comments)
- User demographics and behavior
- Platform-specific features
- Trending topics and hashtags

User Profiles Dataset
~~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('user_profiles', rows)``

**Description:** Social media user profiles with demographics, interests, and activity patterns.

**Key Features:**
- User demographics and location
- Interests and preferences
- Activity patterns and engagement
- Network connections and followers
- Privacy settings and preferences

Technology Datasets (8)
------------------------

Web Analytics Dataset
~~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('web_analytics', rows)``

**Description:** Website traffic and user behavior data with page views, sessions, and conversion metrics.

**Key Features:**
- Page views and session data
- User behavior and navigation paths
- Conversion tracking and goals
- Traffic sources and campaigns
- Device and browser information

App Usage Dataset
~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('app_usage', rows)``

**Description:** Mobile app usage analytics with user sessions, feature usage, and performance metrics.

**Key Features:**
- User sessions and screen time
- Feature usage and interactions
- App performance and crashes
- User retention and churn
- In-app purchases and monetization

System Logs Dataset
~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('system_logs', rows)``

**Description:** System and application logs with error tracking and performance monitoring.

**Key Features:**
- Log levels and message types
- System components and services
- Error codes and stack traces
- Performance metrics and timing
- User actions and system events

API Calls Dataset
~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('api_calls', rows)``

**Description:** API performance and usage data with request/response metrics and error tracking.

**Key Features:**
- API endpoints and methods
- Request/response times and sizes
- Status codes and error rates
- Authentication and rate limiting
- Client information and usage patterns

Server Metrics Dataset
~~~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('server_metrics', rows)``

**Description:** Server performance monitoring data with CPU, memory, disk, and network metrics.

**Key Features:**
- CPU and memory utilization
- Disk I/O and storage metrics
- Network traffic and bandwidth
- Load balancing and scaling
- Health checks and alerts

User Sessions Dataset
~~~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('user_sessions', rows)``

**Description:** User session tracking data with login/logout events and activity monitoring.

**Key Features:**
- Session start/end times and duration
- User authentication and authorization
- Activity tracking and page views
- Device and location information
- Security events and anomalies

Error Logs Dataset
~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('error_logs', rows)``

**Description:** Application error tracking data with exception details and debugging information.

**Key Features:**
- Error types and severity levels
- Stack traces and debugging info
- User context and session data
- Error frequency and patterns
- Resolution status and fixes

Performance Dataset
~~~~~~~~~~~~~~~~~~~

**Usage:** ``tempdataset.create_dataset('performance', rows)``

**Description:** Application performance monitoring data with response times, throughput, and resource usage.

**Key Features:**
- Response times and latency metrics
- Throughput and transaction rates
- Resource utilization and bottlenecks
- Performance trends and baselines
- SLA compliance and alerts

Getting Help
------------

Use the built-in help functions to explore datasets:

.. code-block:: python

   import tempdataset
   
   # Comprehensive help with examples
   tempdataset.help()
   
   # Quick dataset overview with categories
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

Usage Examples
--------------

.. code-block:: python

   import tempdataset
   
   # Generate different dataset categories
   
   # Business data
   sales = tempdataset.create_dataset('sales', 1000)
   customers = tempdataset.create_dataset('customers', 500)
   
   # Financial data
   banking = tempdataset.create_dataset('banking', 800)
   stocks = tempdataset.create_dataset('stocks', 1200)
   
   # IoT sensor data
   weather = tempdataset.create_dataset('weather', 2000)
   energy = tempdataset.create_dataset('energy', 1500)
   
   # Healthcare data
   patients = tempdataset.create_dataset('patients', 300)
   appointments = tempdataset.create_dataset('appointments', 600)
   
   # Technology data
   web_analytics = tempdataset.create_dataset('web_analytics', 5000)
   api_calls = tempdataset.create_dataset('api_calls', 10000)
   
   # Save to files
   tempdataset.create_dataset('financial_data.csv', 1000)  # Uses 'sales' as default
   tempdataset.create_dataset('iot_sensors.json', 2000)