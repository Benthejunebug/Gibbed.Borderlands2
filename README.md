# Gibbed.Borderlands2 — Autosave + Level-80 Patch (fork)

A fork of [gibbed/Gibbed.Borderlands2](https://github.com/gibbed/Gibbed.Borderlands2)
with three additions:

1. **Autosave backups** — before every save, a timestamped copy of the `.sav` is
   written into a `Backups/` folder next to it. The editor has an **Auto-backup**
   toggle (on by default) and a **Backup Now** button, so you always have a
   recoverable copy even if you overwrite the wrong slot.
2. **Level-80 weapons on a level-1 character (save editor)** — the "Sync Levels"
   button used to force a weapon's `GameStage` down to your character level. It now
   uses `Math.Max(existing, syncLevel)`, so gear *above* your level is **preserved**
   instead of being wiped. A level-80 weapon on a level-1 character now survives
   a sync.
3. **Runtime level-requirement bypass** — because the *save* can hold a level-80
   weapon for a level-1 character, but the *game* still refuses to let you equip it.
   We've bundled two approaches:
   - A **BLCMM text mod** (`mods/NoLevelRequirement.blcmm`) listing the most
     common item definitions with `bUsesPlayerLevelRequirement=False`
   - A **Python SDK mod** (`mods/NoLevelRequirement/__init__.py`) that hooks the
     game's object system and patches ALL inventory definitions dynamically

> ⚠️ **The save editor alone CANNOT make a level-80 item equippable.**
> You need BOTH the save editor (to set the level in `.sav`) AND a runtime mod
> (to bypass the in-game level check). See "How to use" below.

---

## 🎮 How to use (complete workflow)

### Step 1 — Patch your save (save editor)
**Windows (GUI):**
1. Download the release from the link below.
2. Open your `.sav` in `Gibbed.Borderlands2.SaveEdit.exe`.
3. Find the weapon, set **Game Stage** to `80`.
4. Save. Autosave backup fires automatically.

**Any OS (CLI):**
```bash
dotnet projects/Borderlands2.CliPatcher/bin/Release/net8.0/bl2-clipatcher.dll save.sav --level 80 --all
```
Writes `save.sav.patched.sav` with all backpack weapons bumped to level 80.

### Step 2 — Bypass level requirement in-game (runtime mod)
**Option A — BLCMM text mod (easiest, no Python SDK):**
1. Install [OpenBLCMM](https://borderlandsmodding.com/) and hex-edit your BL2 exe.
2. Open `mods/NoLevelRequirement.blcmm` in BLCMM.
3. Export / merge into your patch. Launch game.

**Option B — Python SDK mod (cleaner, covers everything):**
1. Install [Python SDK](https://borderlandsmodding.com/sdk-mods/)
2. Copy `mods/NoLevelRequirement/` to `Binaries/Win32/Mods/`
3. Restart game. Enable "NoLevelRequirement" in the Mods menu.

Both approaches achieve the same thing: you can now equip that level-80 weapon.

---

## 📦 Download (prebuilt Windows .exe)

No build needed — grab the release zip and run it:

**→ https://github.com/Benthejunebug/Gibbed.Borderlands2/releases/tag/v1.0.0-autosave**

Unzip and launch **`Gibbed.Borderlands2.SaveEdit.exe`** on Windows
(.NET Framework 4 is required — every Windows box already has it).

The zip contains the compiled editor plus all its dependency DLLs. No installer,
no Visual Studio.

---

## 🛠️ Build it yourself

You don't need Visual Studio. The repo includes build scripts that install the
.NET SDK for you (user-local, no admin) and compile the project.

### Windows
Double-click **`build.cmd`** (or run it in `cmd`):

```
build.cmd
```

It builds the WPF GUI editor. If the Windows Desktop workload isn't present it
falls back to building the headless CLI patcher. Output:

```
projects\Gibbed.Borderlands2.SaveEdit\bin\Release\Gibbed.Borderlands2.SaveEdit.exe
```

### Linux / macOS
Run **`build.sh`**:

```bash
bash build.sh
```

WPF only *runs* on Windows, so on Linux/macOS the script builds the **headless
CLI patcher** instead (see below). It still compiles the GUI assembly if you
just want the binary.

---

## 💻 Headless CLI patcher (no Windows needed)

If you just want to bump a weapon's level from the command line (e.g. set a
level-80 weapon on a save), build the CLI patcher:

```bash
dotnet build projects/Borderlands2.CliPatcher/Borderlands2.CliPatcher.csproj -c Release
dotnet projects/Borderlands2.CliPatcher/bin/Release/net8.0/bl2-clipatcher.dll <save.sav> --level 80
```

Flags:

| Flag         | Meaning                                         |
|--------------|-------------------------------------------------|
| `--level N`  | target weapon `GameStage` (default `80`)        |
| `--all`      | patch every backpack weapon slot               |
| `--slot IDX` | patch only one slot (0-based)                  |

It writes a patched copy as `<save.sav>.patched.sav` and leaves your original
untouched. **A level-1 character with a level-80 weapon round-trips correctly** —
the character stays level 1, the weapon stays 80.

---

## 🎮 Runtime mods (level requirement bypass)

### BLCMM text mod (`mods/NoLevelRequirement.blcmm`)
A focused subset of the full community mod covering:
- All artifacts/relics (base + DLC)
- All class mods (all 6 characters + DLC variants)
- Base-game shields and grenade mods
- Krieg's buzzaxe
- A selection of unique weapons

Load this in OpenBLCMM, export to your patch, and the game will allow equipping
these item types at any level.

### Python SDK mod (`mods/NoLevelRequirement/__init__.py`)
A dynamic hook that iterates all `WillowInventoryDefinition` objects in memory
and flips `bUsesPlayerLevelRequirement` to `False`. Covers **every item in the
game** including DLCs and future content, without needing a 1766-line list.

Requires the [Python SDK](https://borderlandsmodding.com/sdk-mods/) installed.
Copy the `NoLevelRequirement/` folder to `Binaries/Win32/Mods/` and enable it
in the in-game Mods menu.

**Why two approaches?**
- BLCMM works if you already use text mods / Community Patch.
- Python SDK is cleaner, automatic, and doesn't need per-item enumeration.

---

## 🔧 What changed (source)

| File | Change |
|------|--------|
| `projects/Gibbed.Borderlands2.SaveEdit/SaveLoad.cs` | `BackupFile()` — timestamped backup into `Backups/` before overwrite |
| `projects/Gibbed.Borderlands2.SaveEdit/ShellView.xaml` | toolbar: **Auto-backup** checkbox + **Backup Now** button |
| `projects/Gibbed.Borderlands2.SaveEdit/ShellViewModel.cs` | `AutoBackup` property (default `true`), backup before save, `BackupNow()` |
| `projects/Gibbed.Borderlands2.SaveEdit/Tabs/BackpackViewModel.cs` | 4 Sync blocks use `Math.Max` (never lower `GameStage`) |
| `projects/Gibbed.Borderlands2.SaveEdit/Tabs/BankViewModel.cs` | 2 Sync blocks use `Math.Max` |
| `projects/Gibbed.Borderlands2.SaveEdit/Gibbed.Borderlands2.SaveEdit.csproj` | added `Microsoft.NETFramework.ReferenceAssemblies` so `dotnet build` can compile net40 WPF without VS |
| `projects/Borderlands2.CliPatcher/` | headless level-patcher (Linux/macOS/Windows) |
| `projects/Borderlands2.MakeSave/` | synthetic test-save generator (for testing) |
| `projects/Borderlands2.Probe/` | dumps valid asset-library paths (debugging) |
| `mods/NoLevelRequirement.blcmm` | BLCMM text mod for runtime level-requirement bypass |
| `mods/NoLevelRequirement/__init__.py` | Python SDK mod for runtime level-requirement bypass |
| `build.sh` / `build.cmd` | cross-platform build scripts |

---

## 📋 Notes & caveats

- The **GUI editor is WPF** and only *runs* on Windows. It now *builds* from the
  command line thanks to the reference-assemblies package, but you still need
  Windows to actually launch it.
- The headless CLI patcher runs anywhere .NET 8 runs (Linux, macOS, Windows).
- The runtime mods (BLCMM + Python SDK) are **game-side** modifications and only
  affect the running game, not the save file itself.
- Upstream `gibbed/Gibbed.Borderlands2` is **not** modified by this fork's push;
  all changes live here on `Benthejunebug/Gibbed.Borderlands2`.

---

## 🙏 Credits

Forked from [Rick (gibbed) — Gibbed.Borderlands2](https://github.com/gibbed/Gibbed.Borderlands2).
Save format, decoding, and GameInfo data are all his original work; this fork
adds the autosave + level-preservation behavior + runtime mod tooling described
above.

Level-requirement bypass research based on the community mod
"No Level Requirement For Gear" by OurLordAndSaviorGabeNewell (Nexus Mods #94).
