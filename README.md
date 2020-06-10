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
