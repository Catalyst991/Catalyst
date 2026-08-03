; Inno Setup script for Catalyst.
; Build the app first (from the repo root):
;   pyinstaller --noconfirm --clean --name Catalyst --windowed --onedir ^
;     --icon src\catalyst\ui\icon.ico --paths src ^
;     --add-data "src\catalyst\tools\daily_report\assets\template.pptx;catalyst\tools\daily_report\assets" ^
;     --add-data "src\catalyst\ui\icon.ico;catalyst\ui" ^
;     run.py
; Then compile this script (from the installer\ folder):
;   ISCC Catalyst.iss
; The finished installer lands in installer\output\CatalystSetup.exe

#define MyAppName "Catalyst"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Catalyst"
#define MyAppExeName "Catalyst.exe"

[Setup]
AppId={{55645A18-D159-43E1-9F83-D8FC92CAA08C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=output
OutputBaseFilename=CatalystSetup
SetupIconFile=..\src\catalyst\ui\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "..\dist\Catalyst\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
