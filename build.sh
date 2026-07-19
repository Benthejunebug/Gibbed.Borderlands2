#!/usr/bin/env bash
# build.sh — builds Gibbed.Borderlands2 (Linux/macOS). No Visual Studio needed.
# Installs the .NET SDK locally if missing, then builds the GUI if it can
# (WPF needs Windows, so on Linux it falls back to the headless CLI patcher).
set -euo pipefail

DOTNET_DIR="$HOME/.dotnet"
DOTNET="$DOTNET_DIR/dotnet"

# 1. Install .NET SDK (user-local, no sudo) if not present.
if [ ! -x "$DOTNET" ]; then
  echo "== .NET SDK not found, installing to $DOTNET_DIR =="
  curl -sSL https://dot.net/v1/dotnet-install.sh -o /tmp/dotnet-install.sh
  bash /tmp/dotnet-install.sh --channel 8.0 --install-dir "$DOTNET_DIR"
fi

export PATH="$DOTNET_DIR:$PATH"
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

# 2. Try the GUI editor (WPF — only builds on Windows).
if dotnet build projects/Gibbed.Borderlands2.SaveEdit/Gibbed.Borderlands2.SaveEdit.csproj -c Release 2>/dev/null; then
  echo ""
  echo "== GUI build complete =="
  echo "Output: projects/Gibbed.Borderlands2.SaveEdit/bin/Release/Gibbed.Borderlands2.SaveEdit.exe (run on Windows)"
  exit 0
fi

# 3. Fallback: headless CLI patcher (works everywhere).
echo "== GUI build not possible here (WPF needs Windows); building CLI patcher instead =="
dotnet build projects/Borderlands2.CliPatcher/Borderlands2.CliPatcher.csproj -c Release

echo ""
echo "== CLI patcher build complete =="
echo "Run: dotnet projects/Borderlands2.CliPatcher/bin/Release/net8.0/bl2-clipatcher.dll <save.sav> --level 80"
echo "Flags: --level N (target GameStage, default 80) | --all | --slot IDX"
