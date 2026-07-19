@echo off
REM build.cmd - Build Gibbed.Borderlands2 on Windows (double-click or run in cmd).
REM No Visual Studio required, but you DO need Windows (the GUI is WPF).
REM If the GUI build fails, this falls back to building the headless CLI patcher.
setlocal

set "DOTNET_DIR=%LOCALAPPDATA%\dotnet"
set "DOTNET=%DOTNET_DIR%\dotnet.exe"

REM 1. Install the .NET SDK (user-local, no admin) if missing.
if not exist "%DOTNET%" (
  echo == .NET SDK not found, installing to %DOTNET_DIR% ==
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "Invoke-WebRequest https://dot.net/v1/dotnet-install.ps1 -OutFile %TEMP%\dotnet-install.ps1; & %TEMP%\dotnet-install.ps1 -Channel 8.0 -InstallDir '%DOTNET_DIR%'"
)

set "PATH=%DOTNET_DIR%;%PATH%"
set "DOTNET_CLI_TELEMETRY_OPTOUT=1"
set "DOTNET_NOLOGO=1"

cd /d "%~dp0"

REM 2. Try to build the GUI editor (WPF / net40).
echo == building GUI editor (SaveEdit) ==
dotnet build projects\Gibbed.Borderlands2.SaveEdit\Gibbed.Borderlands2.SaveEdit.csproj -c Release
if %ERRORLEVEL%==0 (
  echo.
  echo "== GUI build complete =="
  echo "Output: projects\Gibbed.Borderlands2.SaveEdit\bin\Release\Gibbed.Borderlands2.SaveEdit.exe (run on Windows)"
  goto :done
)

REM 3. Fallback: build the headless CLI patcher (works without Windows desktop workload).
echo.
echo == GUI build failed (likely missing the Windows Desktop workload). ==
echo == Falling back to the headless CLI patcher, which still works. ==
dotnet build projects\Borderlands2.CliPatcher\Borderlands2.CliPatcher.csproj -c Release
if %ERRORLEVEL%==0 (
  echo.
  echo == CLI patcher build complete ==
  echo Run: dotnet projects\Borderlands2.CliPatcher\bin\Release\net8.0\bl2-clipatcher.dll ^<save.sav^> --level 80
  goto :done
)

echo.
echo == Build failed. Your buddy may need the .NET Framework dev pack or Windows SDK. ==
exit /b 1

:done
echo.
echo == Done. ==
endlocal
