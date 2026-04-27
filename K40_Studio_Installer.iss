[Setup]
AppName=K40 Studio BR
AppVersion=0.71
AppPublisher=K40 Studio BR
DefaultDirName=C:\K40_Studio_BR
DefaultGroupName=K40 Studio BR
OutputDir=.\Output
OutputBaseFilename=K40_Studio_BR_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible

[Registry]
Root: HKCU; Subkey: "Software\K40 Studio BR"; ValueType: string; ValueName: "InstallDir"; ValueData: "{app}"; Flags: uninsdeletekey

[Files]
; Copia todos os arquivos do K40_Whisperer-0.71_src
Source: "K40_Whisperer-0.71_src\K40_Whisperer-0.71_src\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Copia as macros para a raiz da instalação para o usuário importar
Source: "K40StudioBridge.bas"; DestDir: "{app}"; Flags: ignoreversion
Source: "corel_macro.vba"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Atalho na Área de Trabalho usando pythonw.exe
Name: "{autodesktop}\K40 Studio BR"; Filename: "pythonw.exe"; Parameters: """{app}\k40_whisperer.py"""; WorkingDir: "{app}"; IconFilename: "{app}\scorchworks.ico"
; Atalho no Menu Iniciar
Name: "{group}\K40 Studio BR"; Filename: "pythonw.exe"; Parameters: """{app}\k40_whisperer.py"""; WorkingDir: "{app}"; IconFilename: "{app}\scorchworks.ico"
Name: "{group}\Desinstalar K40 Studio BR"; Filename: "{uninstallexe}"

[Run]
; (Opcional) Executar o K40 Studio após a instalação
Filename: "pythonw.exe"; Parameters: """{app}\k40_whisperer.py"""; Description: "Executar o K40 Studio BR"; Flags: nowait postinstall skipifsilent

[Code]
// Informações adicionais na tela de finalização sobre como instalar a macro
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Instalação concluída com sucesso!' + #13#10 + #13#10 + 'Para usar a integração com o CorelDRAW, importe o arquivo "K40StudioBridge.bas" localizado na pasta de instalação: ' + ExpandConstant('{app}') + ' usando o Editor VBA do CorelDRAW.', mbInformation, MB_OK);
  end;
end;
