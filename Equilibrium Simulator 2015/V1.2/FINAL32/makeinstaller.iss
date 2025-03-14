; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{3DFC3137-EBB2-4090-B2D8-CD23FB422C90}
AppName=Equilibrium Simulator 2015
AppVersion=1.2
;AppVerName=Equilibrium Simulator 2015 1.2
AppPublisher=James Curran
AppPublisherURL=https://github.com/fredtargaryen/eqmsim2015
AppSupportURL=https://github.com/fredtargaryen/eqmsim2015
AppUpdatesURL=https://github.com/fredtargaryen/eqmsim2015
DefaultDirName=C:\Equilibrium Simulator 2015
DefaultGroupName=Equilibrium Simulator 2015
AllowNoIcons=yes
OutputBaseFilename=Equilibrium Simulator Setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\imageformats\*"; DestDir: "{app}\imageformats"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\PyQt4.QtCore.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\PyQt4.QtGui.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\python32.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\QtCore4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\QtGui4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\sip.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\user\Desktop\FINAL32\exe.win32-3.2\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Equilibrium Simulator 2015"; Filename: "{app}\main.exe"
Name: "{group}\{cm:ProgramOnTheWeb,Equilibrium Simulator 2015}"; Filename: "https://github.com/fredtargaryen/eqmsim2015"
Name: "{group}\{cm:UninstallProgram,Equilibrium Simulator 2015}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Equilibrium Simulator 2015"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,Equilibrium Simulator 2015}"; Flags: nowait postinstall skipifsilent

