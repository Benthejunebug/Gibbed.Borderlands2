#!/usr/bin/env python3
"""
Standalone probe for NoLevelRequirement mod.
Run this BEFORE installing the mod to check if the SDK is available.

Usage:
    python probe_console.py          # Check SDK availability
    python probe_console.py --game   # Check game objects (requires running BL2 with SDK)
"""

from __future__ import annotations

import argparse
import sys


def check_sdk_import() -> dict:
    """Try to import the SDK modules and report what's available."""
    results = {
        "unrealsdk": None,
        "mods_base": None,
        "find_all": None,
        "find_class": None,
        "UObjectIterator": None,
        "all_objects": None,
        "hook": None,
        "register_mod": None,
        "command": None,
    }

    # Try unrealsdk
    try:
        import unrealsdk
        results["unrealsdk"] = True
        results["find_all"] = hasattr(unrealsdk, "find_all")
        results["find_class"] = hasattr(unrealsdk, "find_class")
        results["UObjectIterator"] = hasattr(unrealsdk, "UObjectIterator")
        results["all_objects"] = hasattr(unrealsdk, "all_objects")
    except ImportError as e:
        results["unrealsdk"] = f"ImportError: {e}"

    # Try mods_base
    try:
        import mods_base
        results["mods_base"] = True
        results["hook"] = hasattr(mods_base, "hook")
        results["register_mod"] = hasattr(mods_base, "register_mod")
        results["command"] = hasattr(mods_base, "command")
    except ImportError as e:
        results["mods_base"] = f"ImportError: {e}"

    return results


def check_game_objects() -> dict:
    """Try to find WillowInventoryDefinition objects in a running game."""
    results = {"status": "unknown", "objects_found": 0, "errors": []}

    try:
        import unrealsdk
        objs = list(unrealsdk.find_all("WillowInventoryDefinition"))
        results["status"] = "ok"
        results["objects_found"] = len(objs)

        # Probe first few objects
        sample = objs[:5]
        results["samples"] = []
        for obj in sample:
            if obj is None:
                continue
            info = {"name": str(obj.Name), "class": str(obj.Class.Name)}
            try:
                info["has_bUsesPlayerLevelRequirement"] = hasattr(
                    obj, "bUsesPlayerLevelRequirement"
                )
                if info["has_bUsesPlayerLevelRequirement"]:
                    info["value"] = bool(obj.bUsesPlayerLevelRequirement)
            except Exception as e:
                info["read_error"] = str(e)
            results["samples"].append(info)

    except Exception as e:
        results["status"] = "error"
        results["errors"].append(str(e))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe SDK availability")
    parser.add_argument("--game", action="store_true", help="Also probe running game objects")
    args = parser.parse_args()

    print("=" * 60)
    print(" NoLevelRequirement SDK Probe")
    print("=" * 60)

    print("\n📦 SDK Module Availability:")
    sdk_results = check_sdk_import()
    for name, result in sdk_results.items():
        if result is True:
            print(f"  ✅ {name}")
        elif result is False:
            print(f"  ❌ {name} (module loaded but attribute missing)")
        else:
            print(f"  ❌ {name}: {result}")

    if sdk_results["unrealsdk"] is not True:
        print("\n⚠️  unrealsdk is NOT available.")
        print("   This script must run INSIDE the Borderlands 2 Python SDK environment.")
        print("   If you're running this from a normal Python install, that's expected.")
        print("   The mod will only work when loaded by the SDK inside the game.")
        return 1

    if sdk_results["mods_base"] is not True:
        print("\n⚠️  mods_base is NOT available.")
        print("   The willow2-mod-manager v3.x must be installed.")
        print("   Old PythonSDK (archived Jan 2025) uses a different API.")
        return 1

    print("\n✅ SDK modules are available. The mod should load correctly.")

    if args.game:
        print("\n🎮 Probing game objects...")
        game_results = check_game_objects()
        if game_results["status"] == "ok":
            print(f"  Found {game_results['objects_found']} WillowInventoryDefinition objects")
            if game_results.get("samples"):
                print("  Sample objects:")
                for s in game_results["samples"]:
                    print(f"    - {s['name']} ({s['class']})")
                    if "value" in s:
                        print(f"      bUsesPlayerLevelRequirement = {s['value']}")
                    elif "read_error" in s:
                        print(f"      ERROR reading property: {s['read_error']}")
        else:
            print(f"  ❌ Game probe failed: {game_results['errors']}")

    print("\n" + "=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
