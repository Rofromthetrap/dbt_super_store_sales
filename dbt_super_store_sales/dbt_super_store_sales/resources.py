import dagster as dg
from pathlib import Path
from dagster import AssetKey

from dotenv import load_dotenv
import os


from dagster_powerbi import (
    PowerBIServicePrincipal,
    #PowerBIToken,
    PowerBIWorkspace,
    build_semantic_model_refresh_asset_definition,
    load_powerbi_asset_specs,
)

load_dotenv()


##### Power BI ######


power_bi_workspace = PowerBIWorkspace(
    credentials=PowerBIServicePrincipal(
        client_id=os.environ["POWER_BI_CLIENT_ID"],
        client_secret=os.environ["POWER_BI_CLIENT_SECRET"],
        tenant_id=os.environ["POWER_BI_TENANT_ID"],
    ),
    workspace_id=os.environ["POWER_BI_WORKSPACE_ID"],
)


def get_powerbi_specs():
    specs = load_powerbi_asset_specs(
        power_bi_workspace,
        use_workspace_scan=False,
    )

    upstream_deps = [
        AssetKey("dim_customers"),
        AssetKey("dim_product"),
        AssetKey("dim_subregion"),
        AssetKey("dim_region"),
        AssetKey("fct_orders"),
        AssetKey("dim_shipping_status"),
    ]


    result = []
    for spec in specs:
        if spec.key == AssetKey(["semantic_model", "Super_Store_Sales"]):
            spec = spec.replace_attributes(group_name="powerbi", deps=upstream_deps)
        else:
            spec = spec.replace_attributes(group_name="powerbi")

        # wrap semantic models in a refresh asset definition
        if spec.tags.get("dagster-powerbi/asset_type") == "semantic_model":
            result.append(build_semantic_model_refresh_asset_definition(
                resource_key="power_bi", spec=spec
            ))
        else:
            result.append(spec)

    return result