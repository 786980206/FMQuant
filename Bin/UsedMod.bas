Attribute VB_Name = "UsedMod"
Public Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
Private Declare Function GetTickCount Lib "kernel32" () As Long
Public Sub Sleep2(ByVal msec As Long)
    Dim iTick As Long
    iTick = GetTickCount
    While GetTickCount - iTick < msec
        DoEvents
    Wend
End Sub
'####################################### 根据text获取Combox索引 ####################################
Public Function GetIndexByText(ByVal Str As String, ByVal ComBox As ComboBox) As Integer
    Dim i As Integer
    For i = 0 To ComBox.ListCount - 1
        If ComBox.List(i) = Str Then
            GetIndexByText = i
            Exit For
        End If
    Next
End Function
'###################################### 合成用于展示的Msg ########################################
Public Function MsgFormat(ByRef Msg2Send() As String) As String
    TempStr = "Func = " + Msg2Send(0) + vbCrLf + vbCrLf
    For i = 0 To Main.CB_par.ListCount - 1
        TempStr = TempStr & Main.CB_par.List(i) & " = " & Msg2Send(i + 1) & vbCrLf
    Next
    MsgFormat = TempStr
End Function
'####################################### 获取listbox全部选中内容 ####################################
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
    '############下面一句注释掉试试
    'GetListBoxSelectedText = "[" & GetListBoxSelectedText & "]"
    'MsgBox GetListBoxSelectedText
End Function
'###################################### 用于Array插入元素 ########################################
Public Sub ArrayInsert(ByVal Index As Integer, ByVal Value As Variant, ByRef TempArray() As String)
    TempArray2 = TempArray
    ReDim TempArray(UBound(TempArray) + 1)
    For i = 0 To UBound(TempArray)
        If i < Index Then
            TempArray(i) = TempArray2(i)
        ElseIf i = Index Then
            TempArray(i) = Value
        Else
            TempArray(i) = TempArray2(i - 1)
        End If
    Next
End Sub
'###################################### 直接执行cmd语句 ########################################
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
'###################################### 直接执行cmd语句且不等待 ########################################
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
'###################################### 直接执行cmd语句并读取返回结果 ########################################
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
'###################################### 直接执行cmd语句并逐行读取返回结果 ########################################
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
'###################################### 直接执行Py文件########################################
Public Function PyEx(PyrhonPath, FilePath, ConfigPath)
    On Error GoTo Error
    TempStr = PyrhonPath + " " + FilePath + " " + ConfigPath
    PyEx = Cmd(TempStr)
    'MsgBox PyEx
    Exit Function
Error:
    PyEx = 0
End Function
'###################################### 直接执行Py文件且不等待########################################
Public Function PyExWithoutWait(PyrhonPath, FilePath, ConfigPath)
    On Error GoTo Error
    TempStr = PyrhonPath + " " + FilePath + " " + ConfigPath
    PyExWithoutWait = CmdWithoutWait(TempStr)
    'MsgBox PyEx
    Exit Function
Error:
    PyExWithoutWait = 0
End Function
'###################################### 清除VSFlexGrid多余项 ########################################
'Public Sub ClearGrid(ByRef VsFlexGrid As VsFlexGrid, Optional RemainNum As Integer = 10)
'    With VsFlexGrid
'        For i = .Rows - 1 To RemainNum Step -1
'            .RemoveItem i
'        Next
'    End With
'End Sub
'###################################### 获取DataDef.py的枚举值 ########################################
Function GetEnumList(EnumName As String, ByVal Source As String)
    '定了class的位置
    TempStr = Mid(Source, InStr(Source, "EnumStart"))
    TempStr = Left(TempStr, InStr(TempStr, "EnumEnd"))
    '定EnumName的位置
    TempStr = Mid(TempStr, InStr(TempStr, EnumName))
    If InStr(TempStr, "class") <> 0 Then
        Tempclass = Split(TempStr, "class")
        TempStr = Tempclass(0)
    End If
    TempArray = Split(TempStr, vbNewLine)
    Dim AimArray() As String
    ReDim AimArray(0)
    For i = 0 To UBound(TempArray)
        If InStr(TempArray(i), "=") = 0 Then
            TempArray(i) = ""
        Else
            TempArray(i) = Left(TempArray(i), InStr(TempArray(i), "=") - 1) ' + Mid(TempArray(i), InStr(TempArray(i), "#"))
            TempArray(i) = Replace(TempArray(i), vbTab, "")
            If AimArray(0) <> "" Then
                ReDim Preserve AimArray(UBound(AimArray) + 1)
            End If
            AimArray(UBound(AimArray)) = TempArray(i)
        End If
    Next
    GetEnumList = AimArray
End Function
'###################################### 生成GetData配置文件 ########################################
Function MakeGetDataStr(Optional ByVal AimCodeList As String = "", _
                        Optional ByVal AimTimeList As String = "", _
                        Optional ByVal AimFields As String = "All", _
                        Optional ByVal AimDataType As String = "K_DAY", _
                        Optional ByVal AimGroupType As String = "Default", _
                        Optional ByVal AimDataSource As String = "CycleAll", _
                        Optional ByVal AimSpecialConfig As String = "")
    TempStr = "GetDataStart:" + vbNewLine
    TempStr = TempStr + "CodeList=[" + AimCodeList + "]" + vbNewLine
    TempStr = TempStr + "TimeList=[" + AimTimeList + "]" + vbNewLine
    TempStr = TempStr + "Fields=[" + AimFields + "]" + vbNewLine
    TempStr = TempStr + "DataType='" + AimDataType + "'" + vbNewLine
    TempStr = TempStr + "GroupByType='" + AimGroupType + "'" + vbNewLine
    TempStr = TempStr + "DataSource='" + AimDataSource + "'" + vbNewLine
    TempStr = TempStr + "SpecialConfig=" + "{" + AimSpecialConfig + "}"
    MakeGetDataStr = TempStr
End Function
'###################################### 解析文件到TASK_LIST ########################################
Sub TaskFile2List()
    GetData.TASK_LIST.Clear
    TempTaskList = CodeTran.ReadUTF8File(App.Path + "\Cache\TempTaskList.gd")
    TempTaskInfo = Split(TempTaskList, vbNewLine + "---" + vbNewLine)
    For i = 0 To UBound(TempTaskInfo)
        If TempTaskInfo(i) <> "" Then
            GetData.TASK_LIST.AddItem (TempTaskInfo(i))
        End If
    Next
End Sub

