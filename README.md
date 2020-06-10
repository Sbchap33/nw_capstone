# nw_capstone - Sam Chapman
## Northwestern University School of Professional Studies - Masters in Data Science - Data Engineering 

This project leverages Fivetran's connectors to build an ELT pipeline from the United States Geological Survey (USGS) API to a Snowflake destination warehouse. A cloud function is built and deployed in Google Cloud Platform (GCP) to call the API, and then Fivetran handles the connections between the cloud function and Snowflake. Fivetran provides significant benefits by handling some of the more technical aspects of database connections (e.g. JDBC/ODBC drivers) as well as deduplication, type-inference, and pagination logic. Additionally, their UI provides lots of added features to help automate different parts of the pipeline. 

## Step 1 - Build Cloud Function

A cloud function is built and deployed in GCP to call the USGS website to pull river data on a stretch of the Colorado River near Kremmling Colorado (commonly referred to as "Upper Colorado"). Specifically, the key piece of information is Cubic Feet per Second, or CFS, which provides information on the volume of water currently flowing (a popular metric used by rafters and anglers alike). 

The code to be deployed in GCP (any cloud function service can be used) is: ```usgs_api_pull_funct.py```
