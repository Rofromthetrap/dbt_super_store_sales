from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path

from dagster import Definitions, EnvVar, asset, AssetKey
from dagster_dbt import DbtCliResource
from dagster.components import build_component_defs
from dagster_powerbi import PowerBIWorkspace, PowerBIServicePrincipal

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
# Attempt to load component defs from the `defs/` folder. If that fails (for example
# because external credentials or environment variables required by YAML are not
# present), fall back to loading only the Python-defined assets/schedules so the
# module can still be imported (useful for local development and `dg dev`).
# Component YAML loading commented out per user request. If you want to
# enable loading component definitions from `defs/` again, uncomment the
# lines below and ensure required environment variables are set.
#
# Note: ensure no stale `component_defs` variable remains in module scope
# (Dagster forbids multiple `Definitions` objects at module scope). Remove
# it if present before creating the single `defs` object.
try:
    del component_defs  # remove any leftover Definitions object
except NameError:
    pass

# Attempt to load YAML component definitions (Power BI, etc.) from defs/
# If loading fails (missing env vars/credentials), continue with Python-only defs.
component_defs_loaded = None
try:
    component_defs_loaded = build_component_defs(components_root=Path(__file__).parent / "defs")
except Exception as e:
    # keep import-time safe; YAML components may require credentials not present locally
    component_defs_loaded = None
# Extract assets/resources from loaded component defs and then remove the Definitions
component_assets = []
component_resources = {}
if component_defs_loaded:
    component_assets = component_defs_loaded.assets or []
    if getattr(component_defs_loaded, "resources", None):
        component_resources = dict(component_defs_loaded.resources)
    # prevent leaving a Definitions object at module scope (Dagster invariant)
    try:
        del component_defs_loaded
    except Exception:
        component_defs_loaded = None

@asset(key=AssetKey("airbytecloud_super_store_orders"), group_name="aibyte", description="Airbyte source: super_store_orders")
def airbytecloud_super_store_orders():
    # materialization placeholder for external Airbyte source
    return None


@asset(key=AssetKey("airbytecloud_super_store_people"), group_name="aibyte", description="Airbyte source: super_store_people")
def airbytecloud_super_store_people():
    return None


@asset(key=AssetKey("airbytecloud_superstore_returns"), group_name="aibyte", description="Airbyte source: superstore_returns")
def airbytecloud_superstore_returns():
    return None


def _asset_key_tuples(asset):
    keys = []
    if hasattr(asset, "keys"):
        for k in asset.keys:
            try:
                keys.append(tuple(k.path))
            except Exception:
                try:
                    keys.append(tuple(k))
                except Exception:
                    pass
    elif hasattr(asset, "key"):
        try:
            keys.append(tuple(asset.key.path))
        except Exception:
            try:
                keys.append(tuple(asset.key))
            except Exception:
                pass
    return keys

# Build final assets list with deduplication. Prefer component assets, then dbt assets, then placeholders.
final_assets = []
seen_keys = set()
# add component assets first (if any)
for a in (component_assets or []):
    final_assets.append(a)
    for k in _asset_key_tuples(a):
        seen_keys.add(k)

# add dbt multi-asset if it doesn't duplicate existing keys
dbt_asset = dbt_super_store_sales_dbt_assets
dbt_keys = _asset_key_tuples(dbt_asset)
if not any(k in seen_keys for k in dbt_keys):
    final_assets.append(dbt_asset)
    for k in dbt_keys:
        seen_keys.add(k)

# add airbyte placeholders only if their keys are not already present
for a in [airbytecloud_super_store_orders, airbytecloud_super_store_people, airbytecloud_superstore_returns]:
    keys = _asset_key_tuples(a)
    if not any(k in seen_keys for k in keys):
        final_assets.append(a)
        for k in keys:
            seen_keys.add(k)

assets_list = final_assets

resources_merged = {"dbt": DbtCliResource(project_dir=dbt_super_store_sales_project)}
if component_resources:
    resources_merged.update(component_resources)

defs = Definitions(
    assets=assets_list,
    schedules=schedules,
    resources=resources_merged,
)