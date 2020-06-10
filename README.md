# nw_capstone - Sam Chapman
## Northwestern University School of Professional Studies - Masters in Data Science - Data Engineering 

This project leverages Fivetran's connectors to build an ELT pipeline from the United States Geological Survey (USGS) API to a Snowflake destination warehouse. A cloud function is built and deployed in Google Cloud Platform (GCP) to call the API, and then Fivetran handles the connections between the cloud function and Snowflake. Fivetran provides significant benefits by handling some of the more technical aspects of database connections (e.g. JDBC/ODBC drivers) as well as deduplication, type-inference, and pagination logic. Additionally, their UI provides lots of added features to help automate different parts of the pipeline. 

This project will walk through a "normal" pipeline creation to aggregate data from a cloud function as well as historical data from a AWS S3 bucket and GSheets to simulate the process to prepare data for analytics. 

## Step 1 - Build Cloud Function

A cloud function is built and deployed in GCP to call the USGS website to pull river data on a stretch of the Colorado River near Kremmling Colorado (commonly referred to as "Upper Colorado"). Specifically, the key piece of information is Cubic Feet per Second, or CFS, which provides information on the volume of water currently flowing (a popular metric used by rafters and anglers alike). Note that Fivetran requires the request be sent in a certain structure with a few key variables (https://fivetran.com/docs/functions). State (pagination/cursor to let Fivetran know where we left off to avoid pulling duplicate data) and Insert (data to be inserted). 

The code to be deployed in GCP (any cloud function service can be used) is: ```usgs_api_pull_funct.py```
This code will send the most recent CFS value, date, and location (always the same) for the Upper Colorado water meter from the USGS. 

## Step 2 - Set up connector in Fivetran between Snowflake (destination warehouse) and Cloud Function. 

Setting up the connectors is the easiest part of the entire project! Fivetran makes it insanely easy to set up the source and destination connectors, especially with Snowflake which one can link through their "Partner Connect" tunnel. 

Connect Google Cloud Function to Fivetran: https://fivetran.com/docs/functions/google-cloud-functions/setup-guide
Connect to Snowflake Warehouse: https://fivetran.com/docs/destinations/snowflake

Once these are configured, data will now begin flowing from the function to the destination warehouse. The user changes the frequency of API calls in Fivetran's UI. The end result in Snowflake is the below table (note the automatically added Fivetran columns). 

![image](https://user-images.githubusercontent.com/60025118/84286043-679bd300-aafb-11ea-8ac0-0716295abf33.png)

## Step 3 - Feed historical data into Snowflake warehouse

Now that the cloud function is pushing new data to Snowflake, I wanted to pull historical data into Snowflake to have a longer time-series for analysis. I could have done this through the API using the State variable for Fivetran to know where it left off, but again I wanted to simulate a "normal" ETL/ELT project which normally combines a few data sources. I pull historical data from the USGS into an AWS S3 bucket and a GSheets to highlight two common one-off upload methods through Fivetran. I then connect two new connectors to each source and the data is uploaded into unique databases in my Snowflake warehouse.

Fivetran S3 connector: https://fivetran.com/docs/files/aws-s3
Fivetran GSheets connector: https://fivetran.com/docs/files/google-sheets/changelog

## Step 4 - Create transformation in Fivetran's UI to create new combined historical/new database

Now that I have new data being pushed into a database in Snowflake as well as two databases with historical data (different time period in each), I need to combine them into one master database which has all of the years combined. Fivetran makes this very easy to do through its transformation function in the UI. I deploy SQL code in Fivetran's transformation function that is triggered to run every time new data is written into Snowflake from the cloud function. This way, I maintain my separate tables for historic and new data from the cloud function, but then I also now have a combined table with all of the data that is updated every time new data is written into the cloud function database. 

The code to deploy in Fivetran's transformation UI is ```Transformation.sql```

![Transform](https://user-images.githubusercontent.com/60025118/84287807-9b77f800-aafd-11ea-9c5d-cee9a9251b0a.png)

## Step 5 - Manipulate Fivetran connectors using REST API 

Now that our pipeline is fully operational, there are a few ways that we can intereact with Fivetran using the REST API. Fivetran makes it very easy to get connector status, create or manipulate connector details, and edit/view users in our Fivetran account. The code for this is in the API folder in this repository. Note the Requirements.yml must have the correct key to access one's account. Note the changes one must make for the requirements.yml directory and their individual Fivetran User ID and Connector ID information in the code. 

### Get USGS Details
```GET_USGS_UpperC.py```
This is not for interacting with Fivetran's API, but instead is for interacting with the USGS API. This is the raw data that is coming from the USGS API for which my cloud function is cleaning and sending off to Fivetran. I put this here just in case one wants to see the raw data coming from the USGS API. 

### Retrieve User Details

https://fivetran.com/docs/rest-api/users#retrieveuserdetails

```GET_User_Info.py```

Returns user information from Fivetran

### List Connectors within a Group

https://fivetran.com/docs/rest-api/groups#listallconnectorswithinagroup

```GET_Group_Details.py```

### Retrieve Connector Details

https://fivetran.com/docs/rest-api/connectors#retrieveconnectordetails

```GET_Connector_Details.py```

### Retrieve Connector Schema Config

https://fivetran.com/docs/rest-api/connectors#retrieveaconnectorschemaconfigbeta

```GET_Schema.py```

### Run Connector (initiate sync)

https://fivetran.com/docs/rest-api/connectors#syncconnectordatabeta

```POST_Sync_GCloud.py```



