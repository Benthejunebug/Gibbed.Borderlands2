# Gibbed.Borderlands2 — Autosave + Level-80 Patch (fork)

A fork of [gibbed/Gibbed.Borderlands2](https://github.com/gibbed/Gibbed.Borderlands2)
with two additions:

1. **Autosave backups** — before every save, a timestamped copy of the `.sav` is
   written into a `Backups/` folder next to it. The editor has an **Auto-backup**
   toggle (on by default) and a **Backup Now** button, so you always have a
   recoverable copy even if you overwrite the wrong slot.
2. **Level-80 weapons on a level-1 character** — the "Sync Levels" button used to
   force a weapon's `GameStage` down to your character level. It now uses
   `Math.Max(existing, syncLevel)`, so gear *above* your level is **preserved**
   instead of being wiped. A level-80 weapon on a level-1 character now survives
   a sync (and already saved fine — there was never a character-level gate on the
   weapon level itself).

> ⚠️ This is a UI/behavior fork, not an offline-enable or cheat-everything fork.
> The save format and validation are unchanged.

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

```
bash build.sh
```

WPF only *runs* on Windows, so on Linux/macOS the script builds the **headless
CLI patcher** instead (see below). It still compiles the GUI assembly if you
just want the binary.

---

## 💻 Headless CLI patcher (no Windows needed)

If you just want to bump a weapon's level from the command line (e.g. set a
level-80 weapon on a save), build the CLI patcher:

```
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
| `build.sh` / `build.cmd` | cross-platform build scripts |

---

## 📋 Notes & caveats

- The **GUI editor is WPF** and only *runs* on Windows. It now *builds* from the
  command line thanks to the reference-assemblies package, but you still need
  Windows to actually launch it.
- The headless CLI patcher runs anywhere .NET 8 runs (Linux, macOS, Windows).
- Upstream `gibbed/Gibbed.Borderlands2` is **not** modified by this fork's push;
  all changes live here on `Benthejunebug/Gibbed.Borderlands2`.

---

## 🙏 Credits

Forked from [Rick (gibbed) — Gibbed.Borderlands2](https://github.com/gibbed/Gibbed.Borderlands2).
Save format, decoding, and GameInfo data are all his original work; this fork
only adds the autosave + level-preservation behavior described above.
