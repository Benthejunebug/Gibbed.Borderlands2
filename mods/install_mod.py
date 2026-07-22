#!/usr/bin/env python3
"""
NoLevelRequirement Mod Installer
================================
Installs the NoLevelRequirement Python SDK mod for Borderlands 2.

Usage:
    python install_mod.py          # Auto-detects BL2 path
    python install_mod.py --path "C:\\Steam\\...\\Borderlands 2"
    python install_mod.py --check  # Just check if SDK is installed
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Where this script lives (repo root / mods/ )
SCRIPT_DIR = Path(__file__).parent.resolve()
MOD_SOURCE = SCRIPT_DIR / "NoLevelRequirement"

# Default Steam install paths (Windows)
DEFAULT_STEAM_PATHS = [
    Path.home() / "Steam" / "steamapps" / "common" / "Borderlands 2",
    Path("C:/Program Files (x86)/Steam/steamapps/common/Borderlands 2"),
    Path("C:/Program Files/Steam/steamapps/common/Borderlands 2"),
    Path("D:/Steam/steamapps/common/Borderlands 2"),
    Path("E:/Steam/steamapps/common/Borderlands 2"),
]

# Default Epic paths
DEFAULT_EPIC_PATHS = [
    Path("C:/Program Files/Epic Games/Borderlands2"),
    Path("C:/Program Files/Epic Games/Borderlands 2"),
]


def find_bl2_install() -> Path | None:
    """Try to locate the Borderlands 2 install directory."""
    for path in DEFAULT_STEAM_PATHS + DEFAULT_EPIC_PATHS:
        if path.exists() and (path / "Borderlands2.exe").exists():
            return path
    # Check Windows registry for Steam install path
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\WOW6432Node\Valve\Steam") as key:
            steam_path = Path(winreg.QueryValueEx(key, "InstallPath")[0])
            bl2 = steam_path / "steamapps" / "common" / "Borderlands 2"
            if bl2.exists() and (bl2 / "Borderlands2.exe").exists():
                return bl2
    except Exception:
        pass
    return None


def check_sdk_installed(bl2_path: Path) -> bool:
    """Check if the Python SDK (willow2-mod-manager) is installed."""
    win32 = bl2_path / "Binaries" / "Win32"
    if not win32.exists():
        return False
    # Look for SDK indicators
    sdk_markers = ["ddraw.dll", "Mods", "sdk_mods"]
    return any((win32 / marker).exists() for marker in sdk_markers)


def install_mod(bl2_path: Path, force: bool = False) -> bool:
    """Copy the mod to Binaries/Win32/Mods/NoLevelRequirement/."""
    mods_dir = bl2_path / "Binaries" / "Win32" / "Mods" / "NoLevelRequirement"

    if mods_dir.exists() and not force:
        print(f"⚠️  Mod already installed at: {mods_dir}")
        print("   Use --force to overwrite.")
        return False

    if not MOD_SOURCE.exists():
        print(f"❌ Mod source not found: {MOD_SOURCE}")
        print("   Make sure this script is in the same folder as the NoLevelRequirement/ directory.")
        return False

    # Remove existing if force
    if mods_dir.exists() and force:
        shutil.rmtree(mods_dir)

    shutil.copytree(MOD_SOURCE, mods_dir)
    print(f"✅ Installed to: {mods_dir}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Install NoLevelRequirement Python SDK mod")
    parser.add_argument("--path", type=Path, help="Manual Borderlands 2 install path")
    parser.add_argument("--check", action="store_true", help="Only check SDK status, don't install")
    parser.add_argument("--force", action="store_true", help="Overwrite existing mod")
    args = parser.parse_args()

    print("=" * 60)
    print(" NoLevelRequirement Mod Installer")
    print("=" * 60)

    # Find BL2
    bl2_path = args.path
    if bl2_path is None:
        print("\n🔍 Searching for Borderlands 2 install...")
        bl2_path = find_bl2_install()

    if bl2_path is None:
        print("\n❌ Could not find Borderlands 2 automatically.")
        print("   Please provide the path manually:")
        print("   python install_mod.py --path \"C:\\\\Path\\\\To\\\\Borderlands 2\"")
        return 1

    print(f"\n📁 Found Borderlands 2 at: {bl2_path}")

    # Check SDK
    sdk_ok = check_sdk_installed(bl2_path)
    if sdk_ok:
        print("✅ Python SDK (willow2-mod-manager) appears installed.")
    else:
        print("❌ Python SDK NOT detected.")
        print("\n   🌐 Download from: https://bl-sdk.github.io/willow2-mod-db/")
        print("   📖 Install guide: https://borderlandsmodding.com/sdk-mods/")
        print("\n   Quick steps:")
        print("   1. Download PythonSDK.zip from the GitHub releases")
        print("   2. Extract to Binaries/Win32/ (should create Mods/ folder)")
        print("   3. Restart Borderlands 2 — you'll see a MODS menu on main screen")
        print("\n   After installing the SDK, run this script again.")
        return 1

    if args.check:
        print("\n✅ SDK check complete. Ready to install mod.")
        return 0

    # Install
    print("\n📦 Installing NoLevelRequirement mod...")
    if install_mod(bl2_path, force=args.force):
        print("\n🎉 Done! Next steps:")
        print("   1. Restart Borderlands 2 (if it's running)")
        print("   2. Open the MODS menu from the main screen")
        print("   3. Enable 'No Level Requirement'")
        print("   4. Equip that level-80 weapon on your level-1 character!")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
