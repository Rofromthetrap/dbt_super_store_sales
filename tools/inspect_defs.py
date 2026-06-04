"""
Inspect the `defs` object in `dbt_super_store_sales.definitions` and print asset keys.
Run this from the repo root with the virtualenv activated:
    python tools/inspect_defs.py
"""
from importlib import import_module


def main():
    m = import_module('dbt_super_store_sales.definitions')
    print('module defs attr exists:', hasattr(m, 'defs'))
    if not hasattr(m, 'defs'):
        return 1

    defs = m.defs
    assets = list(defs.assets or [])
    print('num assets in defs:', len(assets))
    for a in assets:
        # Handle single-asset and multi-asset definitions
        if hasattr(a, 'keys') and a.keys:
            print('multi-asset keys:', [k.to_string() for k in a.keys])
        elif hasattr(a, 'key'):
            try:
                print('asset key:', a.key.to_string())
            except Exception:
                print('asset key: (unprintable)')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
