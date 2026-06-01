{% macro insert_employees() %}
    INSERT INTO {{ target.schema }}.employees (employee, region_key, is_manager)
    SELECT employee, region_key, is_manager
    FROM {{ target.schema }}.stg_employees
    WHERE employee NOT IN (SELECT employee FROM {{ target.schema }}.employees);
{% endmacro %}