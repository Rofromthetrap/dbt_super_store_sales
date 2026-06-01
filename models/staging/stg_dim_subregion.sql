with source_data as (
    select * from {{ref('base_orders')}}
),
denormalised as (
SELECT DISTINCT
   {{ dbt_utils.generate_surrogate_key(['postal_code','city']) }} as SUBREGION_KEY,
    POSTAL_CODE POSTAL_CODE_KEY,
    COUNTRY_REGION,
    CITY,
    STATE_PROVINCE,
    CASE
        WHEN REGION= 'West'  THEN 1
        WHEN REGION = 'East'  THEN 2
        WHEN REGION = 'Central'  THEN 3
        WHEN REGION = 'South'  THEN 4
    END REGION_KEY
FROM
source_data
)
select * from denormalised