import os
from dagster import Definitions
from dagster_airbyte import AirbyteWorkspaceComponent

airbyte_component = AirbyteWorkspaceComponent(
    workspace={
        "workspace_id": os.environ.get("AIRBYTE_WORKSPACE"),
        "client_id": os.environ.get("AIRBYTE_CLIENT_ID"),
        "client_secret": os.environ.get("AIRBYTE_CLIENT_SECRET"),
    },
    connection_selector={"by_name": ["gcs_sss_to_sno_sss"]},
    translation={
        "group_name": "airbyte_data",
        "description": "Loads data from Airbyte connection {{ props.connection_name }}",
    },
)

defs = Definitions(components=[airbyte_component])

