Attribute VB_Name = "FileCodeTran"
'VB 文件编码互换模块，支持对Ansi,UTF-8,Unicode(little endian),Unicode big endian编码之间进行转换。

Option Explicit
Public Declare Function MultiByteToWideChar Lib "kernel32.dll" (ByVal CodePage As Long, ByVal dwFlags As Long, ByVal lpMultiByteStr As String, ByVal cchMultiByte As Long, ByVal lpWideCharStr As String, ByVal cchWideChar As Long) As Long
Public Declare Function WideCharToMultiByte Lib "kernel32.dll" (ByVal CodePage As Long, ByVal dwFlags As Long, ByVal lpWideCharStr As Long, ByVal cchWideChar As Long, ByRef lpMultiByteStr As Any, ByVal cchMultiByte As Long, ByVal lpDefaultChar As String, ByVal lpUsedDefaultChar As Long) As Long
Public Const CP_ACP As Long = 0
Public Const CP_UTF8 As Long = 65001

'Ansi纯文本文件转换为Unicode(Little Endian)文本文件
Public Function AnsiToULE(ByVal Inputansifile As String, ByVal OutputULEfile As String) As Boolean
        Dim Filebyte() As Byte, sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUnicodeBuffer As String
       
        On Error Resume Next
       
        '打开Ansi纯文本文件Inputansifile
        FileNumber = FreeFile
        If Dir(Inputansifile) = "" Then AnsiToULE = False: Exit Function
        Open Inputansifile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
          
        sAnsi = StrConv(Filebyte, vbUnicode) '转换为VB6可显示的字符串
        retLen = MultiByteToWideChar(CP_ACP, 0, sAnsi, LenB(sAnsi), vbNullChar, 0) '取得转换后需要的空间大小retLen
        sUnicodeBuffer = String$(LenB(sAnsi), vbNullChar)  '设置缓冲区大小
        If retLen > 0 Then
           retLen = MultiByteToWideChar(CP_ACP, 0, sAnsi, LenB(sAnsi), sUnicodeBuffer, retLen) '开始转换
        Else
           AnsiToULE = False: Exit Function
        End If
       
        '保存为Unicode(Little Endian)文本文件OutputULEfile
        If retLen > 0 Then
           FileNumber = FreeFile
           If Dir(OutputULEfile) <> "" Then Kill (OutputULEfile)
           Open OutputULEfile For Binary As #FileNumber
           Put #FileNumber, , &HFEFF '加上Unicode(Little Endian)文件头BOM标志FFFE
           Put #FileNumber, , sUnicodeBuffer '保存文件内容
           Close #FileNumber
           AnsiToULE = True
        Else
           AnsiToULE = False: Exit Function
        End If
End Function

'Ansi纯文本文件转换为Unicode Big Endian文本文件
Public Function AnsiToUBE(ByVal Inputansifile As String, ByVal OutputUBEfile As String) As Boolean
        Dim Filebyte() As Byte, Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUnicodeBuffer As String
        Dim i As Long
       
        On Error Resume Next
       
        '打开Ansi纯文本文件Inputansifile
        FileNumber = FreeFile
        If Dir(Inputansifile) = "" Then AnsiToUBE = False: Exit Function
        Open Inputansifile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        sAnsi = StrConv(Filebyte, vbUnicode) '转换为VB6可显示的字符串
        retLen = MultiByteToWideChar(CP_ACP, 0, sAnsi, LenB(sAnsi), vbNullChar, 0) '取得转换后需要的空间大小retLen
        sUnicodeBuffer = String$(LenB(sAnsi), vbNullChar)  '设置缓冲区大小
        If retLen > 0 Then
           retLen = MultiByteToWideChar(CP_ACP, 0, sAnsi, LenB(sAnsi), sUnicodeBuffer, retLen) '开始转换
        Else
           AnsiToUBE = False: Exit Function
        End If
       
        '保存为Unicode Big Endian文本文件OutputUBEfile
        If retLen > 0 Then
           ReDim Filebyte(LenB(sAnsi) - 1), Fbyte(LenB(sAnsi) - 1)
           Filebyte = StrConv(sUnicodeBuffer, vbFromUnicode)
           For i = 0 To UBound(Filebyte)
               If i Mod 2 = 0 Then
                  Fbyte(i) = Filebyte(i + 1)
               Else
                  Fbyte(i) = Filebyte(i - 1)
               End If
           Next
           FileNumber = FreeFile
           If Dir(OutputUBEfile) <> "" Then Kill (OutputUBEfile)
           Open OutputUBEfile For Binary As #FileNumber
           Put #FileNumber, , &HFFFE '加上Unicode(Big Endian)文件头BOM标志FEFF
           Put #FileNumber, , Fbyte ' sUnicodeBuffer   '保存文件内容
           Close #FileNumber
           AnsiToUBE = True
        Else
           AnsiToUBE = False: Exit Function
        End If
End Function

'Ansi纯文本文件转换为UTF-8文本文件
Public Function AnsiToUTF8(ByVal Inputansifile As String, ByVal OutputUTF8file As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer() As Byte, S As String
       
        On Error Resume Next
       
        '打开Ansi纯文本文件Inputansifile
        FileNumber = FreeFile
        If Dir(Inputansifile) = "" Then AnsiToUTF8 = False: Exit Function
        Open Inputansifile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        S = Filebyte
        sAnsi = StrConv(S, vbUnicode)  '转换为VB6可显示的字符串
        retLen = WideCharToMultiByte(CP_UTF8, 0, StrPtr(sAnsi), -1, vbNullString, 0, vbNullString, 0) '取得转换后需要的空间大小retLen
       
        If retLen > 0 Then
           ReDim sUTF8Buffer(retLen - 1) ' = String$(retLen, vbNullChar) '设置缓冲区大小
           retLen = WideCharToMultiByte(CP_UTF8, 0, StrPtr(sAnsi), -1, sUTF8Buffer(0), retLen, vbNullString, 0) '开始转换
        Else
           AnsiToUTF8 = False: Exit Function
        End If
       
        '保存为UTF-8文本文件OutputUTF8file
        If retLen > 0 Then
           ReDim Preserve sUTF8Buffer(retLen - 1)
           S = StrConv(sUTF8Buffer, vbUnicode)
           FileNumber = FreeFile
           If Dir(OutputUTF8file) <> "" Then Kill (OutputUTF8file)
           Open OutputUTF8file For Binary As #FileNumber
           Put #FileNumber, , &HBFBBEF '加上UTF-8文件头BOM标志EFBBBF
           Put #FileNumber, 4, S '保存文件内容
           Close #FileNumber
           AnsiToUTF8 = True
        Else
           AnsiToUTF8 = False: Exit Function
        End If
End Function

'UTF-8文本文件转换为Unicode(Little Endian)文本文件
Public Function UTF8ToULE(ByVal InputUTF8file As String, ByVal OutputULEfile As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer As String, S As String
       
        On Error Resume Next
       
        '打开UTF-8文本文件InputUTF8file
        FileNumber = FreeFile
        If Dir(InputUTF8file) = "" Then UTF8ToULE = False: Exit Function
        Open InputUTF8file For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
        
        MsgBox Hex$(Filebyte(0))
        MsgBox Hex$(Filebyte(1))
        MsgBox Hex$(Filebyte(2))
        If Hex$(Filebyte(0)) = "EF" And Hex$(Filebyte(1)) = "BB" And Hex$(Filebyte(2)) = "BF" Then
           S = Filebyte
        Else
           MsgBox (InputUTF8file & " 为非UTF-8编码格式文件!")
           UTF8ToULE = False: Exit Function
        End If
        sAnsi = StrConv(S, vbUnicode) '转换为VB6可显示的字符串
        retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, vbNullChar, 0) '取得转换后需要的空间大小retLen
       
        If retLen > 0 Then
           sUTF8Buffer = String$(retLen * 2, vbNullChar)  '设置缓冲区大小
           retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, sUTF8Buffer, retLen * 2)  '开始转换
        Else
           UTF8ToULE = False: Exit Function
        End If
       
        '保存为Unicode(Little Endian)文本文件OutputULEfile
        If retLen > 0 Then
           S = Left$(sUTF8Buffer, retLen * 2)
           FileNumber = FreeFile
           If Dir(OutputULEfile) <> "" Then Kill (OutputULEfile)
           Open OutputULEfile For Binary As #FileNumber
           Put #FileNumber, , S '保存文件内容，程序自动加上了Unicode(Little Endian)文件头BOM标志FFFE
           Close #FileNumber
           UTF8ToULE = True
        Else
           UTF8ToULE = False: Exit Function
        End If
End Function

'UTF-8文本文件转换为Unicode(Big Endian)文本文件
Public Function UTF8ToUBE(ByVal InputUTF8file As String, ByVal OutputUBEfile As String) As Boolean
        Dim Filebyte() As Byte, Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer As String, S As String
        Dim i As Long
       
        On Error Resume Next
       
        '打开UTF-8文本文件InputUTF8file
        FileNumber = FreeFile
        If Dir(InputUTF8file) = "" Then UTF8ToUBE = False: Exit Function
        Open InputUTF8file For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        If Hex$(Filebyte(0)) = "EF" And Hex$(Filebyte(1)) = "BB" And Hex$(Filebyte(2)) = "BF" Then
           S = Filebyte
        Else
           MsgBox (InputUTF8file & " 为非UTF-8编码格式文件!")
           UTF8ToUBE = False: Exit Function
        End If
        sAnsi = StrConv(S, vbUnicode) '转换为VB6可显示的字符串
        retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, vbNullString, 0) '取得转换后需要的空间大小retLen
                      
        If retLen > 0 Then
           sUTF8Buffer = String$(retLen * 2, vbNullChar)  '设置缓冲区大小
           retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, sUTF8Buffer, retLen * 2)  '开始转换
        Else
           UTF8ToUBE = False: Exit Function
        End If
       
        '保存为Unicode Big Endian文本文件OutputUBEfile
        If retLen > 0 Then
           ReDim Filebyte(LenB(sAnsi) - 1), Fbyte(LenB(sAnsi) - 1)
           Filebyte = StrConv(Left$(sUTF8Buffer, retLen * 2), vbFromUnicode)
           For i = 0 To UBound(Filebyte)
               If i Mod 2 = 0 Then
                  Fbyte(i) = Filebyte(i + 1)
               Else
                  Fbyte(i) = Filebyte(i - 1)
               End If
           Next
           FileNumber = FreeFile
           If Dir(OutputUBEfile) <> "" Then Kill (OutputUBEfile)
           Open OutputUBEfile For Binary As #FileNumber
           Put #FileNumber, , Fbyte '保存文件内容，程序自动加上了Unicode(Big Endian)文件头BOM标志FEFF
           Close #FileNumber
           UTF8ToUBE = True
        Else
           UTF8ToUBE = False: Exit Function
        End If
End Function

'UTF-8文本文件转换为Ansi纯文本文件
Public Function UTF8ToAnsi(ByVal InputUTF8file As String, ByVal OutputAnsifile As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer As String, S As String
        'Dim i As Long
       
        On Error Resume Next
       
        '打开UTF-8文本文件InputUTF8file
        FileNumber = FreeFile
        If Dir(InputUTF8file) = "" Then UTF8ToAnsi = False: Exit Function
        Open InputUTF8file For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        If Hex$(Filebyte(0)) = "EF" And Hex$(Filebyte(1)) = "BB" And Hex$(Filebyte(2)) = "BF" Then
           S = Filebyte
        Else
           MsgBox (InputUTF8file & " 为非UTF-8编码格式文件!")
           UTF8ToAnsi = False: Exit Function
        End If
        sAnsi = StrConv(S, vbUnicode) '转换为VB6可显示的字符串
        retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, vbNullString, 0) '取得转换后需要的空间大小retLen
       
        If retLen > 0 Then
           sUTF8Buffer = String$(retLen * 2, vbNullChar) '设置缓冲区大小
           retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, sUTF8Buffer, retLen * 2) '开始转换
        Else
           UTF8ToAnsi = False: Exit Function
        End If
         
        '保存为Ansi纯文本文件OutputAnsifile
        If retLen > 0 Then
           S = Left$(sUTF8Buffer, retLen * 2)
           S = StrConv(S, vbFromUnicode)
           Mid$(S, 1, 1) = " ": S = Trim(S)
           FileNumber = FreeFile
           If Dir(OutputAnsifile) <> "" Then Kill (OutputAnsifile)
           Open OutputAnsifile For Binary As #FileNumber
           Put #FileNumber, , S '保存文件内容
           Close #FileNumber
           UTF8ToAnsi = True
        Else
           UTF8ToAnsi = False: Exit Function
        End If
End Function

'Unicode(Little Endian)文本文件转换为Ansi纯文本文件
Public Function ULEToAnsi(ByVal InputULEfile As String, ByVal OutputAnsifile As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUnicodeBuffer() As Byte, S As String
        'Dim i As Long
       
        On Error Resume Next
       
        '打开Unicode(Little Endian)文本文件InputULEfile
        FileNumber = FreeFile
        If Dir(InputULEfile) = "" Then ULEToAnsi = False: Exit Function
        Open InputULEfile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        If Hex$(Filebyte(0)) = "FF" And Hex$(Filebyte(1)) = "FE" Then
           S = Filebyte
        Else
           MsgBox (InputULEfile & " 为非Unicode(Little Endian)编码格式文件!")
           ULEToAnsi = False: Exit Function
        End If
        sAnsi = StrConv(S, vbNarrow)  '转换为VB6可显示的字符串
        '到这个地方，应该说可以结束了，VB6用StrConv转换，直接将sAnsi存入文件即可
        '下面是用API转换为Ansi代码
        sAnsi = S
        retLen = WideCharToMultiByte(CP_ACP, 0, StrPtr(sAnsi), -1, vbNullString, 0, vbNullString, 0) '取得转换后需要的空间大小retLen
       
        If retLen > 0 Then
           ReDim sUnicodeBuffer(retLen * 2 - 1) ' String$(retLen * 2, vbNullChar)'设置缓冲区大小
           retLen = WideCharToMultiByte(CP_ACP, 0, StrPtr(sAnsi), -1, sUnicodeBuffer(0), retLen * 2, vbNullString, 0) '开始转换
        Else
           ULEToAnsi = False: Exit Function
        End If
       
        '保存为Ansi纯文本文件OutputAnsifile
        If retLen > 0 Then
           ReDim Preserve sUnicodeBuffer(retLen - 1)
           S = StrConv(sUnicodeBuffer, vbUnicode)
           Mid$(S, 1, 1) = " ": S = Trim(S)
           FileNumber = FreeFile
           If Dir(OutputAnsifile) <> "" Then Kill (OutputAnsifile)
           Open OutputAnsifile For Binary As #FileNumber
           Put #FileNumber, , S '保存文件内容
           Close #FileNumber
           ULEToAnsi = True
        Else
           ULEToAnsi = False: Exit Function
        End If
End Function

'Unicode(Little Endian)文本文件转换为Unicode Big Endian文本文件。
'Unicode Big Endian文本文件转换为Unicode(Little Endian)文本文件，
'只须将Hex$(Filebyte(0)) = "FF" And Hex$(Filebyte(1)) = "FE"改为
'Hex$(Filebyte(0)) = "FE" And Hex$(Filebyte(1)) = "FF"即可。
Public Function ULEToUBE(ByVal InputULEfile As String, ByVal OutputUBEfile As String) As Boolean
        Dim Filebyte() As Byte, Fbyte() As Byte
        'Dim sAnsi As String, retLen As Long
        'Dim sUnicodeBuffer() As Byte, S As String
        Dim i As Long, FileNumber As Long
       
        On Error Resume Next
       
        '打开Unicode(Little Endian)文本文件InputULEfile
        FileNumber = FreeFile
        If Dir(InputULEfile) = "" Then ULEToUBE = False: Exit Function
        Open InputULEfile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1), Fbyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        If Hex$(Filebyte(0)) = "FF" And Hex$(Filebyte(1)) = "FE" Then
           'Unicode(Little Endian)编码格式文件
        Else
           MsgBox (InputULEfile & " 为非Unicode(Little Endian)编码格式文件!")
           ULEToUBE = False: Exit Function
        End If
       
        For i = 0 To UBound(Filebyte)
            If i Mod 2 = 0 Then
               Fbyte(i) = Filebyte(i + 1)
            Else
               Fbyte(i) = Filebyte(i - 1)
            End If
        Next
               
        '保存为Unicode Big Endian文本文件OutputUBEfile
       
        FileNumber = FreeFile
        If Dir(OutputUBEfile) <> "" Then Kill (OutputUBEfile)
        Open OutputUBEfile For Binary As #FileNumber
        Put #FileNumber, , Fbyte '保存文件内容
        Close #FileNumber
End Function

'Unicode(Little Endian)文本文件转换为UTF-8文本文件
Public Function ULEToUTF8(ByVal InputULEfile As String, ByVal OutputUTF8file As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer() As Byte, S As String
       
        On Error Resume Next
       
        '打开Unicode(Little Endian)文本文件InputULEfile
        FileNumber = FreeFile
        If Dir(InputULEfile) = "" Then ULEToUTF8 = False: Exit Function
        Open InputULEfile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
        If Hex$(Filebyte(0)) = "FF" And Hex$(Filebyte(1)) = "FE" Then
           S = Filebyte
        Else
           MsgBox (InputULEfile & " 为非Unicode(Little Endian)编码格式文件!")
           ULEToUTF8 = False: Exit Function
        End If
        sAnsi = StrConv(S, vbNarrow)  '转换为VB6可显示的字符串
        Mid$(sAnsi, 1, 1) = " ": sAnsi = Trim(sAnsi)
        retLen = WideCharToMultiByte(CP_UTF8, 0, StrPtr(sAnsi), -1, vbNullString, 0, vbNullString, 0) '取得转换后需要的空间大小retLen
       
        If retLen > 0 Then
           ReDim sUTF8Buffer(retLen - 1) ' = String$(retLen, vbNullChar) '设置缓冲区大小
           retLen = WideCharToMultiByte(CP_UTF8, 0, StrPtr(sAnsi), -1, sUTF8Buffer(0), retLen, vbNullString, 0) '开始转换
        Else
           ULEToUTF8 = False: Exit Function
        End If
       
        '保存为UTF-8文本文件OutputUTF8file
        If retLen > 0 Then
           ReDim Preserve sUTF8Buffer(retLen - 1)
           S = StrConv(sUTF8Buffer, vbUnicode)
           FileNumber = FreeFile
           If Dir(OutputUTF8file) <> "" Then Kill (OutputUTF8file)
           Open OutputUTF8file For Binary As #FileNumber
           Put #FileNumber, , &HBFBBEF '加上UTF-8文件头BOM标志EFBBBF
           Put #FileNumber, 4, S '保存文件内容
           Close #FileNumber
           ULEToUTF8 = True
        Else
           ULEToUTF8 = False: Exit Function
        End If
End Function

Public Function ReadFile(FilePath As String, Code As String)
    Dim TempStr As String
    If Code = "UTF8" Then
        Call UTF8ToULE(FilePath, FilePath)
    End If
    Open FilePath For Binary As #1
        TempStr = Input(LOF(1), #1)
    Close #1
    Debug.Print TempStr
    ReadFile = TempStr
End Function
'
'public Sub Command1_Click()
'        '先新建一个Ansi纯文本文件"d:\AnsiCodeFile.txt"
'        'Ansi纯文本文件转换为Unicode(Little Endian)文本文件
'        Call AnsiToULE("d:\AnsiCodeFile.txt", "d:\AnsiToUnicodeLEFile.txt")
'
'        'Ansi纯文本文件转换为Unicode(Big Endian)文本文件
'        Call AnsiToUBE("d:\AnsiCodeFile.txt", "d:\AnsiToUnicodeBEFile.txt")
'
'        'Ansi纯文本文件转换为UTF-8文本文件
'        Call AnsiToUTF8("d:\AnsiCodeFile.txt", "d:\AnsiToUTF8File.txt")
'
'        'UTF-8文本文件转换为Unicode(Little Endian)文本文件
'        Call UTF8ToULE("d:\AnsiToUTF8File.txt", "d:\UTF8ToUnicodeLEFile.txt")
'
'        'UTF-8文本文件转换为Unicode Big Endian文本文件
'        Call UTF8ToUBE("d:\AnsiToUTF8File.txt", "d:\UTF8ToUnicodeBEFile.txt")
'
'        'UTF-8文本文件转换为Ansi纯文本文件
'        Call UTF8ToAnsi("d:\AnsiToUTF8File.txt", "d:\UTF8ToAnsiFile.txt")
'
'        'Unicode(Little Endian)文本文件转换为Ansi纯文本文件
'        Call ULEToAnsi("d:\AnsiToUnicodeLEFile.txt", "d:\UnicodeLEToAnsiFile.txt")
'
'        'Unicode(Little Endian)文本文件转换为Unicode Big Endian文本文件
'        Call ULEToUBE("d:\AnsiToUnicodeLEFile.txt", "d:\UnicodeLEToUnicodeBEFile.txt")
'
'        'Unicode(Little Endian)文本文件转换为UTF-8文本文件
'        Call ULEToUTF8("d:\AnsiToUnicodeLEFile.txt", "d:\UnicodeLEToUTF8File.txt")
'End Sub
