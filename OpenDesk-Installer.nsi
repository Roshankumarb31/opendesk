; OpenDesk Installer Script
; Created for OpenDesk - A Developer App Launcher
; Author: Roshankumarb31

[Setup]
; Basic app information
AppName=OpenDesk
AppVersion=1.0.0
AppPublisher=Roshankumarb31
AppPublisherURL=https://github.com/Roshankumarb31/opendesk
AppSupportURL=https://github.com/Roshankumarb31/opendesk/issues
AppUpdatesURL=https://github.com/Roshankumarb31/opendesk/releases
AppId={{B31D4E8F-1234-5678-9ABC-DEF012345678}

; Installation settings
DefaultDirName={autopf}\OpenDesk
DefaultGroupName=OpenDesk
AllowNoIcons=yes
DisableProgramGroupPage=yes
LicenseFile=LICENSE.txt
InfoBeforeFile=README.md
OutputDir=installer_output
OutputBaseFilename=OpenDesk-Setup-v1.0.0
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\OpenDesk.exe
Compression=lzma2
SolidCompression=yes

; Modern wizard style
WizardStyle=modern
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

; Minimum Windows version
MinVersion=10.0

; Privileges
PrivilegesRequired=admin

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "associate"; Description: "Associate OpenDesk with .opendesk files"; GroupDescription: "File associations:"
Name: "startmenu"; Description: "Add to Start Menu"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checked

[Files]
; Main application files
Source: "OpenDesk.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; Configuration files (if they exist)
Source: "launcher_config.json"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

; Documentation
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists('docs')

[Icons]
; Start Menu icons
Name: "{group}\OpenDesk"; Filename: "{app}\OpenDesk.exe"; IconFilename: "{app}\icon.ico"; Tasks: startmenu
Name: "{group}\OpenDesk Documentation"; Filename: "{app}\README.md"; Tasks: startmenu
Name: "{group}\{cm:UninstallProgram,OpenDesk}"; Filename: "{uninstallexe}"; Tasks: startmenu

; Desktop icon
Name: "{autodesktop}\OpenDesk"; Filename: "{app}\OpenDesk.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

; Quick Launch icon (for older Windows)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\OpenDesk"; Filename: "{app}\OpenDesk.exe"; IconFilename: "{app}\icon.ico"; Tasks: quicklaunchicon

; Start Menu tile (Windows 10/11)
Name: "{autoprograms}\OpenDesk"; Filename: "{app}\OpenDesk.exe"; IconFilename: "{app}\icon.ico"

[Registry]
; Application settings
Root: HKCU; Subkey: "Software\OpenDesk"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\OpenDesk"; ValueType: string; ValueName: "Version"; ValueData: "1.0.0"
Root: HKCU; Subkey: "Software\OpenDesk"; ValueType: dword; ValueName: "FirstRun"; ValueData: 1

; File association (optional)
Root: HKCR; Subkey: ".opendesk"; ValueType: string; ValueName: ""; ValueData: "OpenDeskConfigFile"; Flags: uninsdeletevalue; Tasks: associate
Root: HKCR; Subkey: "OpenDeskConfigFile"; ValueType: string; ValueName: ""; ValueData: "OpenDesk Configuration"; Flags: uninsdeletekey; Tasks: associate
Root: HKCR; Subkey: "OpenDeskConfigFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\icon.ico"; Tasks: associate
Root: HKCR; Subkey: "OpenDeskConfigFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\OpenDesk.exe"" ""%1"""; Tasks: associate

; Add to Windows Programs list
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{{B31D4E8F-1234-5678-9ABC-DEF012345678}_is1"; ValueType: string; ValueName: "DisplayName"; ValueData: "OpenDesk"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{{B31D4E8F-1234-5678-9ABC-DEF012345678}_is1"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "1.0.0"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{{B31D4E8F-1234-5678-9ABC-DEF012345678}_is1"; ValueType: string; ValueName: "Publisher"; ValueData: "Roshankumarb31"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{{B31D4E8F-1234-5678-9ABC-DEF012345678}_is1"; ValueType: string; ValueName: "URLInfoAbout"; ValueData: "https://github.com/Roshankumarb31/opendesk"

[Run]
; Option to run OpenDesk after installation
Filename: "{app}\OpenDesk.exe"; Description: "{cm:LaunchProgram,OpenDesk}"; Flags: nowait postinstall skipifsilent

; Open README after installation (optional)
Filename: "notepad.exe"; Parameters: """{app}\README.md"""; Description: "View README file"; Flags: nowait postinstall skipifsilent unchecked

[UninstallRun]
; Clean up processes before uninstall
Filename: "taskkill"; Parameters: "/f /im OpenDesk.exe"; Flags: runhidden

[UninstallDelete]
; Clean up user configuration files
Type: files; Name: "{userappdata}\OpenDesk\*"
Type: dirifempty; Name: "{userappdata}\OpenDesk"

[Code]
// Custom Pascal code for advanced functionality

function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
  Result := 0;
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;

function InitializeSetup(): Boolean;
begin
  // Check if OpenDesk is currently running
  if CheckForMutexes('OpenDeskMutex') then
  begin
    if MsgBox('OpenDesk is currently running. Please close it before continuing with the installation.', mbError, MB_OKCANCEL) = IDCANCEL then
    begin
      Result := False;
    end
    else
    begin
      Result := True;
    end;
  end
  else
  begin
    Result := True;
  end;
end;

// Check if directory exists
function DirExists(const Name: string): Boolean;
begin
  Result := DirExists(ExpandConstant(Name));
end;

[Messages]
; Custom messages
WelcomeLabel2=This will install [name/ver] on your computer.%n%nOpenDesk is a developer app launcher that helps you quickly open and manage your development tools.%n%nIt is recommended that you close all other applications before continuing.
ClickNext=Click Next to continue, or Cancel to exit Setup.
BeveledLabel=OpenDesk - Developer App Launcher by Roshankumarb31
