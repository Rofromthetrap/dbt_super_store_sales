
/*joining returned orders to fact table*/
with source_data as (
    select * from {{ref('base_orders')}}
),

added_returned_orders as (
select
    s.*,
    returned is_returned
from
    source_data s
left join
    {{ ref('base_returns') }} r
on 
    s.ORDER_ID = r.ORDER_ID
),

rearrange_columns as (
select 
    ORDER_ID ORDER_ID_KEY,
    CASE
        WHEN SHIP_MODE= 'Same Day'  THEN 100
        WHEN SHIP_MODE = 'Standard Class'  THEN 110
        WHEN SHIP_MODE = 'First Class'  THEN 120
        WHEN SHIP_MODE = 'Second Class'  THEN 130
    END SHIP_STATUS_KEY,
    CUSTOMER_ID CUSTOMER_KEY,
    --{{ dbt_utils.generate_surrogate_key(['product_name']) }} as PRODUCT_KEY,
    PRODUCT_ID PRODUCT_KEY,
    POSTAL_CODE POSTAL_CODE_KEY,
    {{ dbt_utils.generate_surrogate_key(['postal_code','city']) }} as SUBREGION_KEY,
    ORDER_DATE,
    SHIP_DATE,
    IS_RETURNED,
    SALES,
    QUANTITY,
    DISCOUNT,
    PROFIT
 from 
    added_returned_orders
)
select * from rearrange_columns