import json
from pathlib import Path
from dbt_super_store_sales.assets import CustomDagsterDbtTranslator

translator = CustomDagsterDbtTranslator()

def show(kind, name):
    props = {'resource_type': kind, 'name': name}
    k = translator.get_asset_key(props)
    print(f"{kind} {name} -> {k}")

# sources
for s in ['airbyte_super_store_orders','airbyte_superstore_people','airbyte_superstore_returns']:
    show('source', s)

# models
for m in ['base_orders','base_people','base_returns']:
    show('model', m)
