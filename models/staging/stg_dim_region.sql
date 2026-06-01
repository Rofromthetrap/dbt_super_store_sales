with source_data as (
    select * from {{ref('base_people')}}
),
denormalised as (
    SELECT
    --*
    CASE
        WHEN REGION = 'West'  THEN 1
        WHEN REGION = 'East'  THEN 2
        WHEN REGION = 'Central'  THEN 3
        WHEN REGION = 'South'  THEN 4
    END REGION_KEY,
   REGIONAL_MANAGER EMPLOYEE,
    CASE
        WHEN REGIONAL_MANAGER IS NOT NULL THEN TRUE
        ELSE FALSE
    END IS_MANAGER
FROM
    source_data
)
select * from denormalised