"""
print_lineage.py

Quick helper to read `target/manifest.json` and print source->model edges
based on `meta.dagster.asset_key` on sources and model dependencies.

Usage: run from repo root where `target/manifest.json` exists:
    python print_lineage.py
"""
import json
from pathlib import Path


def main():
    p = Path("target/manifest.json")
    if not p.exists():
        print("manifest not found at", p)
        return 1

    d = json.loads(p.read_text())

    # gather source asset keys
    sources = d.get("sources", {})
    source_asset_keys = {}
    for sid, s in sources.items():
        ak = s.get("meta", {}).get("dagster", {}).get("asset_key")
        if ak:
            if isinstance(ak, list) and len(ak) > 0:
                source_asset_keys[sid] = ak[0]
            else:
                source_asset_keys[sid] = ak

    # models/nodes
    nodes = d.get("nodes", {})
    edges = set()
    for nid, node in nodes.items():
        if not node.get("resource_type") == "model":
            continue
        model_name = node.get("alias") or node.get("name")
        deps = node.get("depends_on", {}).get("nodes", []) or []
        for dep in deps:
            if dep.startswith("source."):
                src_asset = source_asset_keys.get(dep)
                if src_asset:
                    edges.add((src_asset, model_name))

    if not edges:
        print("No edges found")
        return 0

    for a, b in sorted(edges):
        print(f"{a} -> {b}")


if __name__ == "__main__":
    raise SystemExit(main())
import json
from pathlib import Path
p = Path('target/manifest.json')
if not p.exists():
    print('manifest not found at', p)
    raise SystemExit(1)

d = json.loads(p.read_text())
# gather source asset keys
sources = d.get('sources', {})
source_asset_keys = {}
for sid, s in sources.items():
    ak = s.get('meta', {}).get('dagster', {}).get('asset_key')
    if ak:
        # ak may be list
        if isinstance(ak, list) and len(ak) > 0:
            source_asset_keys[sid] = ak[0]
        else:
            source_asset_keys[sid] = ak

# models/nodes
nodes = d.get('nodes', {})
edges = set()
for nid, node in nodes.items():
    # only consider models
    if not node.get('resource_type') == 'model':
        continue
    model_name = node.get('alias') or node.get('name')
    deps = node.get('depends_on', {}).get('nodes', []) or []
    for dep in deps:
        if dep.startswith('source.'):
            src_asset = source_asset_keys.get(dep)
            if src_asset:
                edges.add((src_asset, model_name))

# print edges
if not edges:
    print('No edges found')
else:
    for a,b in sorted(edges):
        print(f"{a} -> {b}")
