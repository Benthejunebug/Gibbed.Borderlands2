# NoLevelRequirement: Python SDK mod for Borderlands 2
# Eliminates level requirements for ALL gear at runtime via dynamic patching.
#
# INSTALL:
#   1. Install Python SDK (see https://borderlandsmodding.com/sdk-mods/)
#   2. Copy this folder to: Binaries/Win32/Mods/NoLevelRequirement/
#   3. Restart game. Look for "NoLevelRequirement" in the Mods menu.
#
# HOW IT WORKS:
#   Instead of listing 1766 individual item definitions like the BLCMM text mod,
#   this hooks into the game's object system and patches bUsesPlayerLevelRequirement
#   on EVERY WillowInventoryDefinition as it loads. Covers weapons, shields,
#   grenades, class mods, artifacts, and any modded/DLC items automatically.
#
# STATUS: Skeleton / experimental. The exact unrealsdk API varies by SDK version.
#   The BLCMM text mod (NoLevelRequirement.blcmm) is the proven approach.
#   This Python mod is provided as a cleaner future path once the SDK API is verified.
#
# AUTHOR: Fork of Gibbed.Borderlands2 tooling
# LICENSE: Same as Gibbed.Borderlands2 (zlib-style, see upstream)

try:
    import unrealsdk
    HAS_SDK = True
except ImportError:
    HAS_SDK = False

if HAS_SDK:
    class NoLevelRequirement(unrealsdk.BL2SDK.MOD):
        Name = "NoLevelRequirement"
        Version = "1.0.0"
        Author = "Ben (forked from community research)"
        Description = "Removes level requirements from ALL gear dynamically."

        _patched = set()

        def Enable(self):
            unrealsdk.Log("[NoLevelRequirement] Enabling...")
            self.PatchAllDefinitions()
            self.RegisterHook("WillowGame.WillowPlayerController", "PlayerTick", self.OnPlayerTick)
            unrealsdk.Log("[NoLevelRequirement] Enabled.")

        def Disable(self):
            unrealsdk.Log("[NoLevelRequirement] Disabled.")

        def OnPlayerTick(self, caller, function, params):
            self.PatchAllDefinitions()
            return True

        def PatchAllDefinitions(self):
            try:
                objs = unrealsdk.FindAll("WillowInventoryDefinition")
            except Exception:
                try:
                    cls = unrealsdk.FindClass("WillowInventoryDefinition")
                    if cls is None:
                        return
                    objs = unrealsdk.UObjectIterator(cls)
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
                        pass
            if patched_this_frame > 0:
                unrealsdk.Log(f"[NoLevelRequirement] Patched {patched_this_frame} definitions.")

    unrealsdk.RegisterMod(NoLevelRequirement())
else:
    # Standalone: this file is meant to run inside the game's Python SDK.
    # If you see this message, you're running it outside the game.
    print("[NoLevelRequirement] This mod must run inside Borderlands 2 via the Python SDK.")
    print("[NoLevelRequirement] Install the SDK, copy this folder to Binaries/Win32/Mods/NoLevelRequirement/")
