with source_data as (
    --select * from raw.super_store_sales.airbyte_superstore_people
    select * from {{ source('superstore', 'airbyte_superstore_people') }}
)
select
    REGION,
    {{ clean_bom('"﻿REGIONAL MANAGER"') }} as REGIONAL_MANAGER
from
    source_data