/*extracting returns data*/
with source_data as (
    --select * from raw.super_store_sales.airbyte_superstore_returns
    select * from {{ source('superstore', 'airbyte_superstore_returns') }}
)
select
    RETURNED,
    --$2 as ORDER_ID
    {{ clean_bom('"﻿ORDER ID"') }} as order_id
from
    source_data