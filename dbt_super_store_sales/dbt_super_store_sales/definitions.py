from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path

from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster.components import build_component_defs

from dbt_super_store_sales.assets import dbt_super_store_sales_dbt_assets
from dbt_super_store_sales.project import dbt_super_store_sales_project
from dbt_super_store_sales.schedules import schedules



# import defs as airbyte_defs
# from dagster._core.definitions.load_assets_from_modules import load_assets_from_modules



# defs = Definitions(
#     assets=[dbt_super_store_sales_dbt_assets],
#     schedules=schedules,
#     resources={
#         "dbt": DbtCliResource(project_dir=dbt_super_store_sales_project),
#     },
# )

# Load all component definitions from defs/ folder (including Airbyte)
# defs_list = load_all(["."])

# my_assets = load_assets_from_modules([my_module])

# component_defs = build_component_defs(
#     # components_root=os.path.join(os.path.dirname(__file__), "defs")
#      components_root=Path(__file__).parent / "defs"
#     )


### test


# component_defs = build_component_defs(components_root=Path(__file__).parent / "defs")
# for asset in component_defs.assets or []:
#     if hasattr(asset, "key"):
#         print(asset.key)
#     elif hasattr(asset, "keys"):
#         print(asset.keys)


# component_defs = build_component_defs(components_root=Path(__file__).parent / "defs")
# for asset in component_defs.assets or []:
#     if hasattr(asset, "keys"):
#         for key in asset.keys:
#             print(key)


# Combine all loaded definitions with your existing assets and schedules
defs = Definitions.merge(
    # *defs_list,
    # component_defs,
    build_component_defs(components_root=Path(__file__).parent / "defs"),
    Definitions(
        assets=[dbt_super_store_sales_dbt_assets],
        schedules=schedules,
        resources={
            "dbt": DbtCliResource(project_dir=dbt_super_store_sales_project),
        },
    )
)