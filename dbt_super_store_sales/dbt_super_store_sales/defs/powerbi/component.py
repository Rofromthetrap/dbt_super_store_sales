import dataclasses
from dagster import AssetKey, Definitions
from dagster.components import ComponentLoadContext
from dagster_powerbi import (
    PowerBIWorkspaceComponent,
    PowerBIWorkspace,
    build_semantic_model_refresh_asset_definition,
    load_powerbi_asset_specs,
)


@dataclasses.dataclass
class CustomPowerBIWorkspaceComponent(PowerBIWorkspaceComponent):

    def build_defs(self, context: ComponentLoadContext) -> Definitions:
        workspace: PowerBIWorkspace = self.workspace

        upstream_deps = [
            AssetKey("dim_customers"),
            AssetKey("dim_product"),
            AssetKey("dim_subregion"),
            AssetKey("dim_region"),
            AssetKey("fct_orders"),
            AssetKey("dim_shipping_status"),
        ]

        specs = load_powerbi_asset_specs(
            workspace,
            use_workspace_scan=False,  # your critical flag
        )

        result = []
        for spec in specs:
            if spec.key == AssetKey(["semantic_model", "Super_Store_Sales"]):
                spec = spec.replace_attributes(
                    group_name="powerbi",
                    deps=upstream_deps
                )
            else:
                spec = spec.replace_attributes(group_name="powerbi")

            if spec.tags.get("dagster-powerbi/asset_type") == "semantic_model":
                result.append(
                    build_semantic_model_refresh_asset_definition(
                        resource_key="power_bi",
                        spec=spec,
                    )
                )
            else:
                result.append(spec)

        return Definitions(
            assets=result,
            resources={"power_bi": workspace},
        )