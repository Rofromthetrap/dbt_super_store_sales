
with source_data as (
select * from {{ref('stg_dim_shipping_status')}}
)
select
    SHIPPING_KEY as SHIP_STATUS_KEY,
    SHIP_MODE
from 
    source_data