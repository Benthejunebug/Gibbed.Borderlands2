# Mods — Runtime Level-Requirement Bypass for Borderlands 2

This folder contains **runtime mods** that eliminate level requirements in-game.
The save editor (in the parent repo) can set a weapon's level to 80, but the **game
itself** still checks `player level < item level` when you try to equip it. These
mods bypass that check.

---

## 📂 Files

| File | What it is | When to use |
|------|-----------|-------------|
| `NoLevelRequirement.blcmm` | OpenBLCMM text mod (focused subset) | You already use BLCMM / Community Patch |
| `NoLevelRequirement/__init__.py` | Python SDK mod (willow2-mod-manager v3.x) | You have the Python SDK installed |
| `install_mod.py` | Cross-platform installer script | To auto-install the Python SDK mod |
| `INSTALL_MOD.cmd` | Windows double-click wrapper | Same as above, but easier |

---

## 🚀 Quick Start — Python SDK mod (recommended)

### Step 1: Install the Python SDK
1. Go to **https://bl-sdk.github.io/willow2-mod-db/**
2. Download the latest `PythonSDK.zip` release
3. Extract it into your Borderlands 2 folder (merge with existing files)
   - Steam default: `C:\Program Files (x86)\Steam\steamapps\common\Borderlands 2`
   - You want `Binaries/Win32/ddraw.dll` and a `Mods/` folder
4. Restart Borderlands 2. You should see a **MODS** menu on the main screen.

### Step 2: Install this mod
**Option A — Double-click (Windows):**
```
mods/
  └── INSTALL_MOD.cmd   ← double-click this
```

**Option B — Command line (any OS):**
```bash
cd mods/
python install_mod.py
```

**Option C — Manual copy:**
Copy `NoLevelRequirement/` to `Borderlands 2/Binaries/Win32/Mods/NoLevelRequirement/`

### Step 3: Enable in-game
1. Restart Borderlands 2
2. From the main menu, select **MODS**
3. Find **"No Level Requirement"** and enable it
4. Done! Now any weapon you patched to level 80 in the save editor will actually equip.

---

## 🧪 Quick Start — BLCMM text mod

If you already use OpenBLCMM and the Community Patch:

1. Open `NoLevelRequirement.blcmm` in OpenBLCMM
2. Export / merge into your existing patch
3. Launch the game with your patch active

This covers artifacts, class mods, shields, grenades, Krieg's buzzaxe, and a
selection of unique weapons. For **complete** coverage of every weapon variant,
download the full mod from Nexus Mods #94.

---

## 🔗 Links

| Resource | URL |
|----------|-----|
| Python SDK download | https://bl-sdk.github.io/willow2-mod-db/ |
| Python SDK install guide | https://borderlandsmodding.com/sdk-mods/ |
| Full "No Level Requirement" mod (Nexus #94) | https://www.nexusmods.com/borderlands2/mods/94 |
| OpenBLCMM mod manager | https://borderlandsmodding.com/ |
| Save editor fork (this repo) | https://github.com/Benthejunebug/Gibbed.Borderlands2 |

---

## ⚠️ Important

- **You need BOTH the save editor AND a runtime mod.** The save editor changes the
  level stored in `.sav`; the runtime mod changes the game's equip check. Neither
  alone is enough.
- The Python SDK mod (`__init__.py`) is written for **willow2-mod-manager v3.x**
  (the current SDK as of mid-2026). The old `PythonSDK` (archived Jan 2025) used a
  different API and will NOT work.
- The BLCMM mod is a **focused subset** (artifacts, class mods, shields, grenades,
  some weapons). If your specific weapon isn't covered, use the Python SDK mod or
  the full Nexus mod.
