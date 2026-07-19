#!/usr/bin/env bash
# build.sh — builds the headless Borderlands 2 CLI patcher (no Windows required).
# Installs the .NET SDK locally if missing, then builds Borderlands2.CliPatcher.
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

# 2. Build the CLI patcher (net8.0 — runs on Linux/macOS/Windows).
echo "== building Borderlands2.CliPatcher =="
dotnet build projects/Borderlands2.CliPatcher/Borderlands2.CliPatcher.csproj -c Release

# 3. Show usage.
echo ""
echo "== build complete =="
echo "Run a patch, e.g.:"
echo "  dotnet projects/Borderlands2.CliPatcher/bin/Release/net8.0/bl2-clipatcher.dll <save.sav> --level 80"
echo ""
echo "Flags:"
echo "  --level N    set target weapon GameStage (default 80)"
echo "  --all        patch every weapon slot"
echo "  --slot IDX   patch only one backpack slot (0-based)"
