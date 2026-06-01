
/*joining returned orders to fact table*/
with source_data as (
    --select * from raw.super_store_sales.airbyte_super_store_orders
    select * from {{ source('superstore', 'airbyte_super_store_orders') }}
)
select
    CITY,
    SALES,
    PROFIT,
    REGION,
    SEGMENT,
    CATEGORY,
    DISCOUNT,
    "ORDER ID" ORDER_ID,
    QUANTITY,
    "SHIP DATE" SHIP_DATE,
    "SHIP MODE" SHIP_MODE,
    "ORDER DATE" ORDER_DATE,
    "PRODUCT ID" PRODUCT_ID,
    "CUSTOMER ID" CUSTOMER_ID,
    "POSTAL CODE" POSTAL_CODE,
    "PRODUCT NAME" PRODUCT_NAME,
    "SUB-CATEGORY" SUB_CATEGORY,
    "CUSTOMER NAME" CUSTOMER_NAME,
    "COUNTRY/REGION" COUNTRY_REGION,
    "STATE/PROVINCE" STATE_PROVINCE
from
    source_data

