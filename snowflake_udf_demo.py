# Creating snowpark python UDF

# Create or replace stage demo_db.public.udf_stage;

from snowflake.snowpark.types import IntegerType, StringType
from generic_code import code_library
from snowflake.snowpark.functions import udf, col
import pandas as pd

connection_parameters = {"account":"ijvunnh-ny22848", \
"user":"pradeep", \
"password": "AbcdAbcdAbcd067$", \
"role":"ACCOUNTADMIN", \
"warehouse":"COMPUTE_WH", \
"database":"DEMO_DB", \
"schema":"PUBLIC" \
}

# Create connection with snowflake and return the session
session_new = code_library.snowconnection(connection_parameters)

# Run this in Snowfalke
# create or replace stage demo_db.public.udf_stage;

@udf(session = session_new,name='a_plus_b', input_types=[IntegerType(), IntegerType()], return_type=IntegerType(), stage_location='@udf_stage',is_permanent=True, replace=True)
def a_plus_b(a: int, b: int) -> int:
    return a+b

df = session_new.create_dataframe(pd.DataFrame([(1, 2, 3, 4)], columns=["a", "b", "c", "d"]))
df.show()
df.withColumn('A_PLUS_B', a_plus_b(col('"a"'), col('"b"'))).show()

# Create table customer test in snowflake before executing below code.
# create table
# DEMO_DB.PUBLIC.CUSTOMER_TEST
# as
# select * from SNOWFLAKE_SAMPLE_DATA.TPCH_SF10.CUSTOMER

df = session_new.table("DEMO_DB.PUBLIC.CUSTOMER_TEST")
dk = df.withColumn('A_PLUS_B', a_plus_b(col('C_CUSTOMER_SK'))).show()

###### Using python packages #######

session_new.add_packages("email_validator")

@udf(session = session_new,name='email_validate', input_types=[StringType()], return_type=StringType(), stage_location='@udf_stage',is_permanent=True, replace=True)
def email_validate(email: str) -> str:
    from email_validator import validate_email, EmailNotValidError
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        return "VALID"
    except EmailNotValidError as e:
        return "NOTVALID"
    

##### Vectorised UDF #####
### If you get certificate error. Just close the terminal or restart the kernel and run again.
from snowflake.snowpark.functions import udf
from snowflake.snowpark.types import IntegerType, PandasSeriesType, PandasDataFrameType

@udf(session = session_new,name='a_plus_b_vector', max_batch_size=200,input_types=[PandasDataFrameType([IntegerType(), IntegerType()])], return_type=PandasSeriesType(IntegerType()), stage_location='@udf_stage',is_permanent=True, replace=True)
def a_plus_b_vector(df):
    return df[0]+df[1]


######### Snowflake external packages ###########
from snowflake.snowpark.functions import udf

session_new.add_packages("numpy", "pandas","catalogue","faker","phonenumbers","dateparser","nltk","textblob")

#session.add_import("@DEMO_DB.PUBLIC.UDF_STAGE/scrubadub/scrubadub.zip")
session_new.add_import('/workspaces/Snowpark_pipeline/python_packages/scrub/scrubadubw/scrubadub')
session_new.add_import('/workspaces/Snowpark_pipeline/python_packages/python-stdnum-1.18/stdnum')
session_new.add_import('/workspaces/Snowpark_pipeline/python_packages/textblob-0.17.1/textblob')
session_new.add_import('/workspaces/Snowpark_pipeline/python_packages/xlrd-2.0.1/xlrd')

@udf(session=session_new ,name="external_scrub_text", is_permanent=True, stage_location="@UDF_STAGE", replace=True)
def scrub_text(x: str) -> str:
    import scrubadub as sc
    txt = sc.clean(x)
    return txt