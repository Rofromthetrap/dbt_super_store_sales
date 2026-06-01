{% macro clean_bom(column_name) %}
    regexp_replace({{ column_name }}, '^\uFEFF', '')
{% endmacro %}