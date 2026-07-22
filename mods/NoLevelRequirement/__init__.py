# NoLevelRequirement: Python SDK mod for Borderlands 2 / TPS / AoDK
# Eliminates level requirements for ALL gear at runtime via dynamic patching.
#
# INSTALL:
#   1. Install Python SDK (willow2-mod-manager) from https://bl-sdk.github.io/
#   2. Copy this folder to: Binaries/Win32/Mods/NoLevelRequirement/
#   3. Restart game. Look for "NoLevelRequirement" in the Mods menu.
#
# HOW IT WORKS:
#   Instead of listing 1766 individual item definitions like the BLCMM text mod,
#   this hooks into the game's object system and patches bUsesPlayerLevelRequirement
#   on EVERY WillowInventoryDefinition as it loads. Covers weapons, shields,
#   grenades, class mods, artifacts, and any modded/DLC items automatically.
#
# COMPATIBILITY:
#   Requires willow2-mod-manager v3.x (the current Python SDK for BL2/TPS/AoDK).
#   The old PythonSDK (archived Jan 2025) used a different API.
#
# AUTHOR: Fork of Gibbed.Borderlands2 tooling
# LICENSE: Same as Gibbed.Borderlands2 (zlib-style, see upstream)

from __future__ import annotations

import unrealsdk
from mods_base import Game, Mod, hook, register_mod
from unrealsdk.hooks import Type


class NoLevelRequirement(Mod):
    """Removes level requirements from all gear dynamically."""

    name = "No Level Requirement"
    author = "Ben (forked from community research)"
    description = "Removes level requirements from ALL gear dynamically at runtime."
    version = "1.0.0"
    supported_games = Game.Willow2  # BL2 | TPS | AoDK
    auto_enable = True

    def __post_init__(self) -> None:
        super().__post_init__()
        # Instance-level cache (each mod instance gets its own)
        self._patched: set[int] = set()

    def on_enable(self) -> None:
        """Called when the mod is enabled."""
        unrealsdk.logging.info("[NoLevelRequirement] Enabling...")
        self.patch_all_definitions()
        unrealsdk.logging.info("[NoLevelRequirement] Enabled.")

    def on_disable(self) -> None:
        """Called when the mod is disabled. We can't easily undo property changes,
        but we stop the continuous patching."""
        unrealsdk.logging.info("[NoLevelRequirement] Disabled.")

    @hook("WillowGame.WillowPlayerController.PlayerTick", Type.POST)
    def on_player_tick(self, obj, args, ret, func) -> None:
        """Periodic re-scan in case new definitions load mid-session (e.g. DLC)."""
        self.patch_all_definitions()
        return None  # Don't block the original tick

    def patch_all_definitions(self) -> None:
        """Find every WillowInventoryDefinition in memory and flip the flag."""
        try:
            objs = unrealsdk.find_all("WillowInventoryDefinition")
        except Exception:
            return

        patched_this_frame = 0
        for obj in objs:
            if obj is None:
                continue
            obj_id = id(obj)
            if obj_id in self._patched:
                continue

            if hasattr(obj, "bUsesPlayerLevelRequirement"):
                try:
                    obj.bUsesPlayerLevelRequirement = False
                    self._patched.add(obj_id)
                    patched_this_frame += 1
                except Exception:
                    pass  # Some objects may be read-only; skip silently

        if patched_this_frame > 0:
            unrealsdk.logging.info(
                f"[NoLevelRequirement] Patched {patched_this_frame} definitions."
            )


# Register the mod with the mod manager
mod = NoLevelRequirement()
register_mod(mod)
