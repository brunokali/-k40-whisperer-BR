Attribute VB_Name = "K40StudioBridge"
' Macro de Integração CorelDRAW -> K40 Studio BR
' Desenvolvido para K40 Studio BR

Sub ExportToK40Studio()
    Dim doc As Document
    Dim exp As ExportFilter
    Dim svgPath As String
    Dim pythonPath As String
    Dim scriptPath As String
    Dim shellCommand As String
    Dim installDir As String
    Dim wsh As Object
    
    ' --- CONFIGURAÇÕES DO AMBIENTE ---
    ' Lendo o diretório de instalação do Windows Registry criado pelo instalador
    On Error Resume Next
    Set wsh = CreateObject("WScript.Shell")
    installDir = wsh.RegRead("HKCU\Software\K40 Studio BR\InstallDir")
    On Error GoTo 0
    
    ' Fallback caso não ache no registro
    If installDir = "" Then
        installDir = "C:\K40_Studio_BR"
    End If
    
    pythonPath = "pythonw" 
    scriptPath = installDir & "\k40_whisperer.py"
    svgPath = Environ("TEMP") & "\k40_studio_bridge.svg"
    
    Set doc = ActiveDocument
    If doc Is Nothing Then
        MsgBox "Por favor, abra um documento no CorelDRAW antes de exportar.", vbExclamation
        Exit Sub
    End If
    
    ' --- CONFIGURAÇÕES DE EXPORTAÇÃO SVG ---
    Dim se As StructExportOptions
    Set se = CreateStructExportOptions
    se.MaintainLayers = True
    
    If doc.ActiveSelection.Shapes.Count > 0 Then
        se.SelectedOnly = True
    Else
        se.SelectedOnly = False
    End If
    
    ' Executa a exportação
    Set exp = doc.ExportEx(svgPath, cdrSVG, cdrAllPages, se)
    
    If exp.FilterError = 0 Then
        shellCommand = """" & pythonPath & """ """ & scriptPath & """ --open """ & svgPath & """"
        On Error Resume Next
        Shell shellCommand, vbNormalFocus
        If Err.Number <> 0 Then
            MsgBox "Não foi possível localizar o Python ou o script do K40. Verifique se o Python está instalado e se o K40 Studio BR foi instalado corretamente.", vbCritical
        End If
    Else
        MsgBox "Houve um erro técnico ao exportar o SVG para o K40. Código: " & exp.FilterError, vbCritical
    End If
End Sub
