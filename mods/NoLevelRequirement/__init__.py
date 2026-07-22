# NoLevelRequirement Debug Build — Two-Pass Workflow
# ====================================================
#
# PASS 1 (THIS BUILD): DIAGNOSTIC / INFORMATION GATHERING
#   Goal: Figure out what actually works inside Borderlands 2's Python SDK.
#   The mod probes the object system, tries multiple discovery methods,
#   and reports back EXACTLY what it found.
#
# PASS 2 (AFTER YOUR REPORT): FIXED / PRODUCTION BUILD
#   Goal: Based on what Pass 1 discovered, we write the real mod.
#   Maybe the property is named differently. Maybe find_all() doesn't exist.
#   Maybe we need to hook a different function. We won't know until Pass 1 runs.
#
# HOW TO RUN PASS 1:
#   1. Install Python SDK (willow2-mod-manager v3.x):
#      https://bl-sdk.github.io/willow2-mod-db/
#   2. Copy this folder to: Borderlands 2/Binaries/Win32/Mods/NoLevelRequirement/
#   3. Start Borderlands 2
#   4. From main menu, select MODS → enable "No Level Requirement (DEBUG)"
#   5. Load a save or start a new game (the mod needs PlayerTick to fire)
#   6. Open the in-game console (default key: ~ or F6)
#   7. Look for output prefixed with [NOLVL-DEBUG]
#   8. Copy ALL the console output and send it to me
#
# CONSOLE COMMANDS (type these in the in-game console):
#   nolvl.probe   — Runs the probe immediately
#   nolvl.dump    — Shows the last collected findings
#   nolvl.patch   — Force patch pass
#
# WHAT TO LOOK FOR:
#   - Does it find any WillowInventoryDefinition objects?
#   - Does the property bUsesPlayerLevelRequirement exist?
#   - Can it READ the property? Can it WRITE the property?
#   - What errors show up?
#   - What classes are the objects? (maybe it's a subclass)
#
# FILES:
#   __init__.py         — The mod (loads into game)
#   probe_console.py    — Standalone script (test SDK from normal Python)
#   NoLevelRequirement.sdkmod  — Pre-packaged mod (drop into sdk_mods/)
#
# INSTALL OPTIONS:
#   A) Manual: Copy this folder to Binaries/Win32/Mods/NoLevelRequirement/
#   B) .sdkmod: Drop NoLevelRequirement.sdkmod into Binaries/Win32/sdk_mods/
#   C) Installer: Run ../install_mod.py (or double-click ../INSTALL_MOD.cmd)

from __future__ import annotations

import unrealsdk
from mods_base import Game, Mod, command, hook, register_mod
from unrealsdk.hooks import Type


class NoLevelRequirementDebug(Mod):
    """Diagnostic probe for level-requirement removal."""

    name = "No Level Requirement (DEBUG)"
    author = "Ben"
    description = "Diagnostic build — probes the object system and reports findings."
    version = "1.0.0-debug"
    supported_games = Game.Willow2
    auto_enable = True

    def __post_init__(self) -> None:
        super().__post_init__()
        self._probed = False
        self._patch_count = 0
        self._error_count = 0
        self._findings = {
            "total_objects": 0,
            "has_property": 0,
            "property_readable": 0,
            "property_writable": 0,
            "property_already_false": 0,
            "property_true_count": 0,
            "errors": [],
            "classes_seen": set(),
            "sample_objects": [],
            "sample_errors": [],
        }

    def _log(self, msg: str) -> None:
        unrealsdk.logging.info(f"[NOLVL-DEBUG] {msg}")

    def _dump_findings(self) -> None:
        f = self._findings
        self._log("=" * 60)
        self._log("NOLVL DIAGNOSTIC SUMMARY")
        self._log("=" * 60)
        self._log(f"Total objects scanned: {f['total_objects']}")
        self._log(f"Has bUsesPlayerLevelRequirement: {f['has_property']}")
        self._log(f"  - Readable: {f['property_readable']}")
        self._log(f"  - Writable: {f['property_writable']}")
        self._log(f"  - Already False: {f['property_already_false']}")
        self._log(f"  - Was True (patched): {f['property_true_count']}")
        self._log(f"Errors: {self._error_count}")
        self._log(f"Unique classes: {len(f['classes_seen'])}")
        if f['sample_objects']:
            self._log("")
            self._log("Sample patched objects:")
            for s in f['sample_objects'][:15]:
                self._log(f"  {s}")
        if f['sample_errors']:
            self._log("")
            self._log("Sample errors:")
            for s in f['sample_errors'][:10]:
                self._log(f"  {s}")
        self._log("=" * 60)
        self._log("END SUMMARY")
        self._log("=" * 60)

    def probe_and_patch(self) -> None:
        self._findings = {
            "total_objects": 0, "has_property": 0, "property_readable": 0,
            "property_writable": 0, "property_already_false": 0,
            "property_true_count": 0, "errors": [],
            "classes_seen": set(), "sample_objects": [], "sample_errors": [],
        }
        self._patch_count = 0
        self._error_count = 0

        objs = []
        methods_tried = []

        # Method 1: find_all
        try:
            objs = list(unrealsdk.find_all("WillowInventoryDefinition"))
            methods_tried.append("find_all")
        except Exception as e:
            self._log(f"find_all() failed: {e}")
            self._findings["sample_errors"].append(f"find_all: {e}")

        # Method 2: UObjectIterator
        if not objs:
            try:
                cls = unrealsdk.find_class("WillowInventoryDefinition")
                if cls is not None:
                    objs = list(unrealsdk.UObjectIterator(cls))
                    methods_tried.append("UObjectIterator")
            except Exception as e:
                self._log(f"UObjectIterator failed: {e}")
                self._findings["sample_errors"].append(f"UObjectIterator: {e}")

        # Method 3: all_objects
        if not objs:
            try:
                objs = list(unrealsdk.all_objects())
                methods_tried.append("all_objects")
            except Exception as e:
                self._log(f"all_objects() failed: {e}")
                self._findings["sample_errors"].append(f"all_objects: {e}")

        self._log(f"Discovery methods tried: {methods_tried}")
        self._log(f"Total objects found: {len(objs)}")
        self._findings["total_objects"] = len(objs)

        for obj in objs:
            if obj is None:
                continue
            try:
                cls_name = str(obj.Class.Name)
                self._findings["classes_seen"].add(cls_name)
            except Exception:
                cls_name = "unknown"

            has_prop = hasattr(obj, "bUsesPlayerLevelRequirement")
            if not has_prop:
                continue

            self._findings["has_property"] += 1

            try:
                current = obj.bUsesPlayerLevelRequirement
                self._findings["property_readable"] += 1
            except Exception as e:
                self._error_count += 1
                err = f"Read {cls_name}: {e}"
                self._findings["errors"].append(err)
                if len(self._findings["sample_errors"]) < 20:
                    self._findings["sample_errors"].append(err)
                continue

            if current is False:
                self._findings["property_already_false"] += 1
                continue

            self._findings["property_true_count"] += 1

            try:
                obj.bUsesPlayerLevelRequirement = False
                self._findings["property_writable"] += 1
                self._patch_count += 1
                if len(self._findings["sample_objects"]) < 20:
                    obj_name = str(obj.Name)
                    self._findings["sample_objects"].append(
                        f"{obj_name} ({cls_name}) = False"
                    )
            except Exception as e:
                self._error_count += 1
                err = f"Write {cls_name}: {e}"
                self._findings["errors"].append(err)
                if len(self._findings["sample_errors"]) < 20:
                    self._findings["sample_errors"].append(err)

        self._log(
            f"Probe done: {self._patch_count} patched, "
            f"{self._error_count} errors, "
            f"{self._findings['property_already_false']} already False"
        )

    def on_enable(self) -> None:
        self._log("=" * 60)
        self._log("NoLevelRequirement DEBUG mod enabled")
        self._log("Run 'nolvl.probe' in console to start diagnostic")
        self._log("=" * 60)

    def on_disable(self) -> None:
        self._log("NoLevelRequirement DEBUG mod disabled")

    @hook("WillowGame.WillowPlayerController.PlayerTick", Type.POST)
    def on_player_tick(self, obj, args, ret, func) -> None:
        if not self._probed:
            self._probed = True
            self._log("Auto-probing on first PlayerTick...")
            self.probe_and_patch()
            self._dump_findings()
        return None


# Console commands
@command("nolvl.probe")
def cmd_probe(args: str) -> None:
    unrealsdk.logging.info("[NOLVL-DEBUG] Console command: probe")
    if mod is not None:
        mod.probe_and_patch()
        mod._dump_findings()


@command("nolvl.dump")
def cmd_dump(args: str) -> None:
    unrealsdk.logging.info("[NOLVL-DEBUG] Console command: dump")
    if mod is not None:
        mod._dump_findings()


@command("nolvl.patch")
def cmd_patch(args: str) -> None:
    unrealsdk.logging.info("[NOLVL-DEBUG] Console command: patch")
    if mod is not None:
        mod.probe_and_patch()
        mod._dump_findings()


# Register
mod = NoLevelRequirementDebug()
register_mod(mod)
