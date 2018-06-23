Attribute VB_Name = "CodeTran"
Private Declare Function WideCharToMultiByte Lib "kernel32" (ByVal CodePage As Long, ByVal dwFlags As Long, ByVal lpWideCharStr As Long, ByVal cchWideChar As Long, ByRef lpMultiByteStr As Any, ByVal cchMultiByte As Long, ByVal lpDefaultChar As String, ByVal lpUsedDefaultChar As Long) As Long
Private Declare Function MultiByteToWideChar Lib "kernel32" (ByVal CodePage As Long, ByVal dwFlags As Long, ByVal lpMultiByteStr As Long, ByVal cchMultiByte As Long, ByVal lpWideCharStr As Long, ByVal cchWideChar As Long) As Long
Private Const CP_UTF8 = 65001
'######################################UTF-8与Unicode字符转换#####################################
Function Utf8ToUnicode(ByRef Utf() As Byte) As String
    Dim lRet As Long
    Dim lLength As Long
    Dim lBufferSize As Long
    lLength = UBound(Utf) - LBound(Utf) + 1
    If lLength <= 0 Then Exit Function
    lBufferSize = lLength * 2
    Utf8ToUnicode = String$(lBufferSize, Chr(0))
    lRet = MultiByteToWideChar(CP_UTF8, 0, VarPtr(Utf(0)), lLength, StrPtr(Utf8ToUnicode), lBufferSize)
    If lRet <> 0 Then
        Utf8ToUnicode = Left(Utf8ToUnicode, lRet)
    End If
End Function
Function UnicodeToUtf8(ByVal UCS As String) As Byte()
    Dim lLength As Long
    Dim lBufferSize As Long
    Dim lResult As Long
    Dim abUTF8() As Byte
    lLength = Len(UCS)
    If lLength = 0 Then Exit Function
    lBufferSize = lLength * 3 + 1
    ReDim abUTF8(lBufferSize - 1)
    lResult = WideCharToMultiByte(CP_UTF8, 0, StrPtr(UCS), lLength, abUTF8(0), lBufferSize, vbNullString, 0)
    If lResult <> 0 Then
    lResult = lResult - 1
    ReDim Preserve abUTF8(lResult)
    UnicodeToUtf8 = abUTF8
    End If
End Function
'###############################################读写Utf-8文件#########################################
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
'#########################################Json信息解析函数####################################################
Public Function JSONParse(ByVal JSONPath As String, ByVal JSONString As String) As Variant
    Dim JSON As Object
    Set JSON = CreateObject("MSScriptControl.ScriptControl")
    JSON.Language = "JScript"
    JSONParse = JSON.eval("JSON=" & JSONString & ";JSON." & JSONPath & ";")
    Set JSON = Nothing
End Function
'#########################################函数构造函数####################################################
Public Function FuncMake(ByVal Func As String, ByRef Par() As String) As String
    FuncMake = Func + "("
    For i = 0 To UBound(Par)
        FuncMake = FuncMake + Par(i) + ","
    Next
    If Right(FuncMake, 1) = "," Then FuncMake = Left(FuncMake, Len(FuncMake) - 1)
    FuncMake = FuncMake + ")"
    'FuncMake = Replace(FuncMake, "'", "+")
End Function
'##################################用Adodb的方式读UTF8有问题，自己写一个试试##############################
Public Function ReadUTF8(FilePath)
    Dim TempByetArray() As Byte
    ReDim TempByetArray(FileLen(FilePath) - 1)
    Open FilePath For Binary As #1
        Get #1, , TempByetArray
        'TempStr = Input(LOF(1), #1)
    Close #1
    ReadUTF8 = Utf8ToUnicode(TempByetArray)
End Function
'################################## 文件编码转化到Unicode ##############################################
Public Sub FileCodeFromUTF8ToUnicode(FilePath As String, Optional NewFilePath As String)
    If NewFilePath = "" Then NewFilePath = FilePath
    TempStr = ReadUTF8(FilePath)
    Open NewFilePath For Output As #1
        Print #1, TempStr
    Close #1
End Sub
'################################## 将消息中的'和\等转换为+号 ##############################################
Public Function MsgSymbolChange(ByVal Msg As String, Optional Symbol1 As String = "+", Optional Symbol2 As String = "|")
    MsgSymbolChange = Replace(Msg, "'", Symbol1)
    MsgSymbolChange = Replace(MsgSymbolChange, """", Symbol1)
    MsgSymbolChange = Replace(MsgSymbolChange, "\", Symbol2)
End Function

