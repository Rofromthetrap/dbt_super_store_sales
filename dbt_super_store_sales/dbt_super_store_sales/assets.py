from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator
from dagster import AssetKey
from .project import dbt_super_store_sales_project

import dagster as dg


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props.get("resource_type")
        name = dbt_resource_props.get("name")

        if resource_type == "source":
            # manifest source identifiers include the full source identifier names
            mapping = {
                "airbyte_super_store_orders": AssetKey(["airbytecloud_super_store_orders"]),
                "airbyte_superstore_people": AssetKey(["airbytecloud_super_store_people"]),
                "airbyte_superstore_returns": AssetKey(["airbytecloud_superstore_returns"]),
            }
            if name in mapping:
                return mapping[name]

        # Ensure the base models have simple asset keys so the source -> base lineage displays
        if resource_type == "model":
            model_mapping = {
                "base_orders": AssetKey(["base_orders"]),
                "base_people": AssetKey(["base_people"]),
                "base_returns": AssetKey(["base_returns"]),
            }
            if name in model_mapping:
                return model_mapping[name]

        return super().get_asset_key(dbt_resource_props)

    

        # mapping = {
        #     "base_orders": AssetKey(["airbytecloud_super_store_orders"]),
        #     "base_people": AssetKey(["airbytecloud_super_store_people"]),
        #     "base_returns": AssetKey(["airbytecloud_superstore_returns"]),
        # }

        # model_name = dbt_resource_props.get("name")
        # if model_name in mapping:
        #     return upstream | {mapping[model_name]}
        
        # return upstream
    

@dbt_assets(
        manifest=dbt_super_store_sales_project.manifest_path,
        dagster_dbt_translator=CustomDagsterDbtTranslator(),
        )
def dbt_super_store_sales_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    

