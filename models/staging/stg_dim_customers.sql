with source as (
    select * from {{ref('base_orders')}}
),
distinct_columns as(
select distinct
    customer_id customer_key,
    customer_name,
    segment
from
    source
)
select * from distinct_columns