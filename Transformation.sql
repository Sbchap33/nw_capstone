--merge data from historical GSheets and S3 tables and new data from Cloud Function table into a newly created table each time data is loaded into Cloud Function table)

merge into KREMMLING.CFS using GOOGLE_CLOUD_FUNCTION.UPPER_C
    on KREMMLING.CFS.TIME_S = GOOGLE_CLOUD_FUNCTION.UPPER_C.TIME
    when not matched 
        then insert (SITE_NAME, CFS, _FIVETRAN_SYNCED, TIME_S) values(GOOGLE_CLOUD_FUNCTION.UPPER_C.SITE_NAME, GOOGLE_CLOUD_FUNCTION.UPPER_C.CFS, GOOGLE_CLOUD_FUNCTION.UPPER_C._FIVETRAN_SYNCED,
                                                                    GOOGLE_CLOUD_FUNCTION.UPPER_C.TIME);
