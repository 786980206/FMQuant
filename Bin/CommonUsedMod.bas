Attribute VB_Name = "CommonUsedMod"
'###############################################��дUtf-8�ļ�#########################################
'��Ҫ����-���� Activx Data Object 2.8
Function WriteUTF8File(Str, FilePath)
    Dim adostream As New ADODB.Stream
    With adostream
        .Type = adTypeText
        .Mode = adModeReadWrite
        .Charset = "utf-8"
        .Open
        .Position = 0
        .WriteText Str
        .SaveToFile FilePath, adSaveCreateOverWrite
        .Close
    End With
    Set adostream = Nothing
End Function
Function ReadUTF8File(FilePath)
    Dim adostream As New ADODB.Stream
    Set adostream = New ADODB.Stream
    'With adostream
        adostream.Type = adTypeText
        adostream.Mode = adModeReadWrite
       adostream.Charset = "utf-8"
       adostream.Open
       adostream.LoadFromFile (FilePath)
        ReadUTF8File = adostream.ReadText
        adostream.Close
    'End With
    Set adostream = Nothing
End Function
Function AddUTF8File(Str, FilePath)
    Dim strm As New ADODB.Stream
    If Dir(FilePath) = Empty Then
        strm.Type = adTypeText
        strm.Mode = adModeReadWrite
        strm.Open
        strm.Charset = "UTF-8"
        strm.WriteText Str
        strm.SaveToFile FilePath, adSaveCreateOverWrite
        strm.Close
    Else
        strm.Type = adTypeText
        strm.Mode = adModeReadWrite
        strm.Open
        strm.Charset = "UTF-8"
        strm.LoadFromFile FilePath
        strm.Position = strm.Size
        strm.WriteText Str
        strm.SaveToFile FilePath, adSaveCreateOverWrite
        strm.Close
    End If
    Set strm = Nothing
End Function
'#########################################Json��Ϣ��������####################################################
Public Function JSONParse(ByVal JSONPath As String, ByVal JSONString As String) As Variant
    Dim JSON As Object
    Set JSON = CreateObject("MSScriptControl.ScriptControl")
    JSON.Language = "JScript"
    JSONParse = JSON.eval("JSON=" & JSONString & ";JSON." & JSONPath & ";")
    Set JSON = Nothing
End Function
'###################################### ��ȡ�����ļ���ö��ֵ ########################################
Function GetParByName(ByVal Source As String, ByVal EnumName As String, ByVal VariableName As String)
    '����class��λ��
    TempStr = Mid(Source, InStr(Source, "EnumStart"))
    TempStr = Left(TempStr, InStr(TempStr, "EnumEnd"))
    '��EnumName��λ��
     TempStr = Mid(TempStr, InStr(TempStr, EnumName))
    If InStr(TempStr, "class") <> 0 Then
        Tempclass = Split(TempStr, "class")
        TempStr = Tempclass(0)
    End If
    TempArray = Split(TempStr, vbNewLine)
    Dim AimArray() As String
    ReDim AimArray(0)
    GetParByName = ""
    For i = 0 To UBound(TempArray)
        TempArray(i) = Replace(TempArray(i), vbTab, "")
        TempArray(i) = Replace(TempArray(i), " ", "")
        If InStr(TempArray(i), VariableName) = 1 And InStr(TempArray(i), "=") <> 0 Then
            GetParByName = Mid(TempArray(i), InStr(TempArray(i), "=") + 1)
            If InStr(GetParByName, "#") <> 0 Then
                GetParByName = Left(GetParByName, InStr(GetParByName, "#") - 1) ' + Mid(TempArray(i), InStr(TempArray(i), "#"))
            End If
        End If
    Next
End Function
'###################################### ��ȡ�����ļ�Ŀ��ֵ ########################################
Function GetPar(ByVal Source As String, ByVal EnumName As String, ByVal VariableName As String)
    Source = Replace(Source, "[[", "[")
    Source = Replace(Source, "]]", "]")
    Source = Replace(Source, vbTab, "")
    'Source = Replace(Source, " ", "")
    Source = LTrim(Source)
    Source = RTrim(Source)
    TempStr = Mid(Source, InStr(Source, "[" + EnumName + "]"))
    If InStr(TempStr, "[") <> 0 Then
        Tempclass = Split(TempStr, "[")
        TempStr = Tempclass(1)
    End If
    TempArray = Split(TempStr, vbNewLine)
    Dim AimArray() As String
    ReDim AimArray(0)
    GetPar = ""
    For i = 0 To UBound(TempArray)
        If InStr(TempArray(i), VariableName) = 1 And InStr(TempArray(i), "=") <> 0 Then
            GetPar = Mid(TempArray(i), InStr(TempArray(i), "=") + 1)
            If InStr(GetPar, "#") <> 0 Then
                GetPar = Left(GetPar, InStr(GetPar, "#") - 1) ' + Mid(TempArray(i), InStr(TempArray(i), "#"))
            End If
            GetPar = LTrim(GetPar)
            GetPar = RTrim(GetPar)
        End If
    Next
End Function
'###################################### ���������ļ�Ŀ��ֵ ##################################################
Function SavePar(ByVal Source As String, ByVal EnumName As String, ByVal VariableName As String, ByVal Value As String, ByVal Path As String)
    Source = Replace(Source, vbTab, "")
    'Source = Replace(Source, " ", "")
    Source = LTrim(Source)
    Source = RTrim(Source)
    If InStr(Source, "[" + EnumName + "]") <> 0 Then
        TempStr = Mid(Source, InStr(Source, "[" + EnumName + "]"))
        If InStr(TempStr, "[") <> 0 Then
            Tempclass = Split(TempStr, "[")
            TempStr = Tempclass(1)
        End If
        TempStr2 = TempStr
        If InStr(Replace(TempStr2, " ", ""), VariableName + "=") <> 0 Then
            AimStr = Mid(TempStr2, InStr(TempStr2, VariableName))
            If InStr(AimStr, vbNewLine) <> 0 Then
                AimStr = Left(AimStr, InStr(AimStr, vbNewLine) - 1)
            End If
            TempStr2 = Replace(TempStr2, AimStr, VariableName + "=" + Value)
        Else
            TempStr2 = Left(TempStr2, InStr(TempStr2, vbNewLine)) + VariableName + "=" + Value + Mid(TempStr2, InStr(TempStr2, vbNewLine))
        End If
        AimSource = Replace(Source, TempStr, TempStr2)
    Else
        TempStr = vbNewLine + "[" + EnumName + "]" + vbNewLine + VariableName + "=" + Value
        AimSource = Source + TempStr
    End If
    Call WriteUTF8File(AimSource, Path)
    SavePar = AimSource
End Function
'###################################### ɾ�������ļ��ڵ� ##################################################
Function DelPar(ByVal Source As String, ByVal EnumName As String, ByVal Path As String)
    Source = Replace(Source, vbTab, "")
    'Source = Replace(Source, " ", "")
    Source = LTrim(Source)
    Source = RTrim(Source)
    TempStr = Mid(Source, InStr(Source, "[" + EnumName + "]"))
    If InStr(TempStr, "[") <> 0 Then
        Tempclass = Split(TempStr, "[")
        TempStr = Tempclass(1)
    End If
    AimSource = Replace(Source, "[" + TempStr, "")
    Call WriteUTF8File(AimSource, Path)
    DelPar = AimSource
End Function
'###################################### ��ȡ�ļ��������ļ��� ########################################
Function GetFileName(Path)
    TempArray = Split(Path, "\")
    GetFileName = TempArray(UBound(TempArray))
End Function
Function GetFolder(Path)
    TempArray = Split(Path, "\")
    TempStr = TempArray(UBound(TempArray))
    GetFolder = Left(Path, InStr(Path, TempStr) - 2)
End Function
'###################################### ֱ��ִ��cmd��� ########################################
Public Function Cmd(ByVal Str As String)
    On Error GoTo Error
    Dim WScript As Object
    Set WScript = CreateObject("WSCript.shell")
    Cmd = WScript.run(Str, , True)
    Set WScript = Nothing
    If Cmd = 0 Then Cmd = 1
    Exit Function
Error:
    Cmd = 0
End Function
'###################################### ֱ��ִ��cmd����Ҳ��ȴ� ########################################
Public Function CmdWithoutWait(ByVal Str As String)
    On Error GoTo Error
    Dim WScript As Object
    Set WScript = CreateObject("WSCript.shell")
    CmdWithoutWait = WScript.run(Str, , False)
    Set WScript = Nothing
    If CmdWithoutWait = 0 Then CmdWithoutWait = 1
    Exit Function
Error:
    CmdWithoutWait = 0
End Function
'###################################### ֱ��ִ��cmd��䲢��ȡ���ؽ�� ########################################
Public Function Cmd2(ByVal Str As String)
    On Error GoTo Error
    Dim WScript As Object
    Set WScript = CreateObject("WSCript.shell")
    Set a = WScript.exec(Str).stdout()
    B = a.readall()
    Set WScript = Nothing
    Cmd2 = B
    Exit Function
Error:
    Cmd2 = 0
End Function
'###################################### ֱ��ִ��cmd��䲢���ж�ȡ���ؽ�� ########################################
Public Function Cmd3(ByVal Str As String)
    'On Error GoTo Error
    On Error Resume Next
    DoEvents
    Dim WScript As Object
    Set WScript = CreateObject("WSCript.shell")
    Set a = WScript.exec(Str).stdout
    Do Until a.atendofstream
         MsgBox a.readline
    Loop
    B = a.readall()
    Set WScript = Nothing
    Cmd3 = B
End Function
'###################################### ֱ��ִ��Py�ļ�########################################
Public Function PyEx(PyrhonPath, FilePath, ConfigPath)
    On Error GoTo Error
    TempStr = PyrhonPath + " " + FilePath + " " + ConfigPath
    PyEx = Cmd(TempStr)
    'MsgBox PyEx
    Exit Function
Error:
    PyEx = 0
End Function
'###################################### ֱ��ִ��Py�ļ��Ҳ��ȴ�########################################
Public Function PyExWithoutWait(PyrhonPath, FilePath, ConfigPath)
    On Error GoTo Error
    TempStr = PyrhonPath + " " + FilePath + " " + ConfigPath
    PyExWithoutWait = CmdWithoutWait(TempStr)
    'MsgBox PyEx
    Exit Function
Error:
    PyExWithoutWait = 0
End Function
'###################################### vb������� ########################################
'1.ȥ����ֵ
Public Function ArrRmSpace(Arr)
    Dim TempArr() As String
    ReDim TempArr(0)
    For i = 0 To UBound(Arr)
        If Arr(i) <> "" Then
            TempArr = ArrInsert(TempArr, UBound(TempArr), Arr(i))
        End If
    Next
    TempArr = ArrDel(TempArr, UBound(TempArr))
    ArrRmSpace = TempArr
End Function
'2.����Ԫ��
Public Function ArrInsert(Arr, Index, Str)
    Dim TempArr() As String
    ReDim TempArr(UBound(Arr) + 1)
    For i = UBound(Arr) To 0 Step -1
         If i >= Index Then
            TempArr(i + 1) = Arr(i)
         Else
            TempArr(i) = Arr(i)
         End If
    Next
    TempArr(Index) = Str
    ArrInsert = TempArr
End Function
'3.ɾ��Ԫ��
Public Function ArrDel(Arr, Index)
    Dim TempArr() As String
    ReDim TempArr(UBound(Arr) - 1)
    For i = UBound(Arr) To 0 Step -1
         If i > Index Then
            TempArr(i - 1) = Arr(i)
         Else
            If i <> Index Then TempArr(i) = Arr(i)
         End If
    Next
    ArrDel = TempArr
End Function
'###################################### ɾ���ļ��� ########################################
Public Function DelFolder(Path)
    Shell "cmd.exe /c rd " + Path + " /s/q", vbHide
End Function
'####################################### ��ȡlistboxȫ��ѡ������ ####################################
Public Function GetListBoxSelectedText(ByVal ListBox As ListBox) As String
    GetListBoxSelectedText = ""
    TempStr = ""
    For i = 0 To ListBox.ListCount - 1
        If ListBox.Selected(i) = True Then
            If InStr(ListBox.List(i), " ") <> 0 Then
                TempStr = Left(ListBox.List(i), InStr(ListBox.List(i), " ") - 1)
            Else
                TempStr = ListBox.List(i)
            End If
            If Right(TempStr, 1) = "." Then TempStr = Left(TempStr, Len(TempStr) - 1)
            GetListBoxSelectedText = GetListBoxSelectedText & "'" & TempStr & "',"
        End If
    Next
    If Right(GetListBoxSelectedText, 1) = "," Then GetListBoxSelectedText = Left(GetListBoxSelectedText, Len(GetListBoxSelectedText) - 1)
    '############����һ��ע�͵�����
    'GetListBoxSelectedText = "[" & GetListBoxSelectedText & "]"
    'MsgBox GetListBoxSelectedText
End Function
'####################################### ����text��ȡCombox���� ####################################
Public Function GetIndexByText(ByVal Str As String, ByVal ComBox As ComboBox) As Integer
    Dim i As Integer
    For i = 0 To ComBox.ListCount - 1
        If ComBox.List(i) = Str Then
            GetIndexByText = i
            Exit For
        End If
    Next
End Function
