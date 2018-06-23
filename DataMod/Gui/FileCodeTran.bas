Attribute VB_Name = "FileCodeTran"
'VB �ļ����뻥��ģ�飬֧�ֶ�Ansi,UTF-8,Unicode(little endian),Unicode big endian����֮�����ת����

Option Explicit
Public Declare Function MultiByteToWideChar Lib "kernel32.dll" (ByVal CodePage As Long, ByVal dwFlags As Long, ByVal lpMultiByteStr As String, ByVal cchMultiByte As Long, ByVal lpWideCharStr As String, ByVal cchWideChar As Long) As Long
Public Declare Function WideCharToMultiByte Lib "kernel32.dll" (ByVal CodePage As Long, ByVal dwFlags As Long, ByVal lpWideCharStr As Long, ByVal cchWideChar As Long, ByRef lpMultiByteStr As Any, ByVal cchMultiByte As Long, ByVal lpDefaultChar As String, ByVal lpUsedDefaultChar As Long) As Long
Public Const CP_ACP As Long = 0
Public Const CP_UTF8 As Long = 65001

'Ansi���ı��ļ�ת��ΪUnicode(Little Endian)�ı��ļ�
Public Function AnsiToULE(ByVal Inputansifile As String, ByVal OutputULEfile As String) As Boolean
        Dim Filebyte() As Byte, sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUnicodeBuffer As String
       
        On Error Resume Next
       
        '��Ansi���ı��ļ�Inputansifile
        FileNumber = FreeFile
        If Dir(Inputansifile) = "" Then AnsiToULE = False: Exit Function
        Open Inputansifile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
          
        sAnsi = StrConv(Filebyte, vbUnicode) 'ת��ΪVB6����ʾ���ַ���
        retLen = MultiByteToWideChar(CP_ACP, 0, sAnsi, LenB(sAnsi), vbNullChar, 0) 'ȡ��ת������Ҫ�Ŀռ��СretLen
        sUnicodeBuffer = String$(LenB(sAnsi), vbNullChar)  '���û�������С
        If retLen > 0 Then
           retLen = MultiByteToWideChar(CP_ACP, 0, sAnsi, LenB(sAnsi), sUnicodeBuffer, retLen) '��ʼת��
        Else
           AnsiToULE = False: Exit Function
        End If
       
        '����ΪUnicode(Little Endian)�ı��ļ�OutputULEfile
        If retLen > 0 Then
           FileNumber = FreeFile
           If Dir(OutputULEfile) <> "" Then Kill (OutputULEfile)
           Open OutputULEfile For Binary As #FileNumber
           Put #FileNumber, , &HFEFF '����Unicode(Little Endian)�ļ�ͷBOM��־FFFE
           Put #FileNumber, , sUnicodeBuffer '�����ļ�����
           Close #FileNumber
           AnsiToULE = True
        Else
           AnsiToULE = False: Exit Function
        End If
End Function

'Ansi���ı��ļ�ת��ΪUnicode Big Endian�ı��ļ�
Public Function AnsiToUBE(ByVal Inputansifile As String, ByVal OutputUBEfile As String) As Boolean
        Dim Filebyte() As Byte, Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUnicodeBuffer As String
        Dim i As Long
       
        On Error Resume Next
       
        '��Ansi���ı��ļ�Inputansifile
        FileNumber = FreeFile
        If Dir(Inputansifile) = "" Then AnsiToUBE = False: Exit Function
        Open Inputansifile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        sAnsi = StrConv(Filebyte, vbUnicode) 'ת��ΪVB6����ʾ���ַ���
        retLen = MultiByteToWideChar(CP_ACP, 0, sAnsi, LenB(sAnsi), vbNullChar, 0) 'ȡ��ת������Ҫ�Ŀռ��СretLen
        sUnicodeBuffer = String$(LenB(sAnsi), vbNullChar)  '���û�������С
        If retLen > 0 Then
           retLen = MultiByteToWideChar(CP_ACP, 0, sAnsi, LenB(sAnsi), sUnicodeBuffer, retLen) '��ʼת��
        Else
           AnsiToUBE = False: Exit Function
        End If
       
        '����ΪUnicode Big Endian�ı��ļ�OutputUBEfile
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
           Put #FileNumber, , &HFFFE '����Unicode(Big Endian)�ļ�ͷBOM��־FEFF
           Put #FileNumber, , Fbyte ' sUnicodeBuffer   '�����ļ�����
           Close #FileNumber
           AnsiToUBE = True
        Else
           AnsiToUBE = False: Exit Function
        End If
End Function

'Ansi���ı��ļ�ת��ΪUTF-8�ı��ļ�
Public Function AnsiToUTF8(ByVal Inputansifile As String, ByVal OutputUTF8file As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer() As Byte, S As String
       
        On Error Resume Next
       
        '��Ansi���ı��ļ�Inputansifile
        FileNumber = FreeFile
        If Dir(Inputansifile) = "" Then AnsiToUTF8 = False: Exit Function
        Open Inputansifile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        S = Filebyte
        sAnsi = StrConv(S, vbUnicode)  'ת��ΪVB6����ʾ���ַ���
        retLen = WideCharToMultiByte(CP_UTF8, 0, StrPtr(sAnsi), -1, vbNullString, 0, vbNullString, 0) 'ȡ��ת������Ҫ�Ŀռ��СretLen
       
        If retLen > 0 Then
           ReDim sUTF8Buffer(retLen - 1) ' = String$(retLen, vbNullChar) '���û�������С
           retLen = WideCharToMultiByte(CP_UTF8, 0, StrPtr(sAnsi), -1, sUTF8Buffer(0), retLen, vbNullString, 0) '��ʼת��
        Else
           AnsiToUTF8 = False: Exit Function
        End If
       
        '����ΪUTF-8�ı��ļ�OutputUTF8file
        If retLen > 0 Then
           ReDim Preserve sUTF8Buffer(retLen - 1)
           S = StrConv(sUTF8Buffer, vbUnicode)
           FileNumber = FreeFile
           If Dir(OutputUTF8file) <> "" Then Kill (OutputUTF8file)
           Open OutputUTF8file For Binary As #FileNumber
           Put #FileNumber, , &HBFBBEF '����UTF-8�ļ�ͷBOM��־EFBBBF
           Put #FileNumber, 4, S '�����ļ�����
           Close #FileNumber
           AnsiToUTF8 = True
        Else
           AnsiToUTF8 = False: Exit Function
        End If
End Function

'UTF-8�ı��ļ�ת��ΪUnicode(Little Endian)�ı��ļ�
Public Function UTF8ToULE(ByVal InputUTF8file As String, ByVal OutputULEfile As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer As String, S As String
       
        On Error Resume Next
       
        '��UTF-8�ı��ļ�InputUTF8file
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
           MsgBox (InputUTF8file & " Ϊ��UTF-8�����ʽ�ļ�!")
           UTF8ToULE = False: Exit Function
        End If
        sAnsi = StrConv(S, vbUnicode) 'ת��ΪVB6����ʾ���ַ���
        retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, vbNullChar, 0) 'ȡ��ת������Ҫ�Ŀռ��СretLen
       
        If retLen > 0 Then
           sUTF8Buffer = String$(retLen * 2, vbNullChar)  '���û�������С
           retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, sUTF8Buffer, retLen * 2)  '��ʼת��
        Else
           UTF8ToULE = False: Exit Function
        End If
       
        '����ΪUnicode(Little Endian)�ı��ļ�OutputULEfile
        If retLen > 0 Then
           S = Left$(sUTF8Buffer, retLen * 2)
           FileNumber = FreeFile
           If Dir(OutputULEfile) <> "" Then Kill (OutputULEfile)
           Open OutputULEfile For Binary As #FileNumber
           Put #FileNumber, , S '�����ļ����ݣ������Զ�������Unicode(Little Endian)�ļ�ͷBOM��־FFFE
           Close #FileNumber
           UTF8ToULE = True
        Else
           UTF8ToULE = False: Exit Function
        End If
End Function

'UTF-8�ı��ļ�ת��ΪUnicode(Big Endian)�ı��ļ�
Public Function UTF8ToUBE(ByVal InputUTF8file As String, ByVal OutputUBEfile As String) As Boolean
        Dim Filebyte() As Byte, Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer As String, S As String
        Dim i As Long
       
        On Error Resume Next
       
        '��UTF-8�ı��ļ�InputUTF8file
        FileNumber = FreeFile
        If Dir(InputUTF8file) = "" Then UTF8ToUBE = False: Exit Function
        Open InputUTF8file For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        If Hex$(Filebyte(0)) = "EF" And Hex$(Filebyte(1)) = "BB" And Hex$(Filebyte(2)) = "BF" Then
           S = Filebyte
        Else
           MsgBox (InputUTF8file & " Ϊ��UTF-8�����ʽ�ļ�!")
           UTF8ToUBE = False: Exit Function
        End If
        sAnsi = StrConv(S, vbUnicode) 'ת��ΪVB6����ʾ���ַ���
        retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, vbNullString, 0) 'ȡ��ת������Ҫ�Ŀռ��СretLen
                      
        If retLen > 0 Then
           sUTF8Buffer = String$(retLen * 2, vbNullChar)  '���û�������С
           retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, sUTF8Buffer, retLen * 2)  '��ʼת��
        Else
           UTF8ToUBE = False: Exit Function
        End If
       
        '����ΪUnicode Big Endian�ı��ļ�OutputUBEfile
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
           Put #FileNumber, , Fbyte '�����ļ����ݣ������Զ�������Unicode(Big Endian)�ļ�ͷBOM��־FEFF
           Close #FileNumber
           UTF8ToUBE = True
        Else
           UTF8ToUBE = False: Exit Function
        End If
End Function

'UTF-8�ı��ļ�ת��ΪAnsi���ı��ļ�
Public Function UTF8ToAnsi(ByVal InputUTF8file As String, ByVal OutputAnsifile As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer As String, S As String
        'Dim i As Long
       
        On Error Resume Next
       
        '��UTF-8�ı��ļ�InputUTF8file
        FileNumber = FreeFile
        If Dir(InputUTF8file) = "" Then UTF8ToAnsi = False: Exit Function
        Open InputUTF8file For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        If Hex$(Filebyte(0)) = "EF" And Hex$(Filebyte(1)) = "BB" And Hex$(Filebyte(2)) = "BF" Then
           S = Filebyte
        Else
           MsgBox (InputUTF8file & " Ϊ��UTF-8�����ʽ�ļ�!")
           UTF8ToAnsi = False: Exit Function
        End If
        sAnsi = StrConv(S, vbUnicode) 'ת��ΪVB6����ʾ���ַ���
        retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, vbNullString, 0) 'ȡ��ת������Ҫ�Ŀռ��СretLen
       
        If retLen > 0 Then
           sUTF8Buffer = String$(retLen * 2, vbNullChar) '���û�������С
           retLen = MultiByteToWideChar(CP_UTF8, 0, sAnsi, -1, sUTF8Buffer, retLen * 2) '��ʼת��
        Else
           UTF8ToAnsi = False: Exit Function
        End If
         
        '����ΪAnsi���ı��ļ�OutputAnsifile
        If retLen > 0 Then
           S = Left$(sUTF8Buffer, retLen * 2)
           S = StrConv(S, vbFromUnicode)
           Mid$(S, 1, 1) = " ": S = Trim(S)
           FileNumber = FreeFile
           If Dir(OutputAnsifile) <> "" Then Kill (OutputAnsifile)
           Open OutputAnsifile For Binary As #FileNumber
           Put #FileNumber, , S '�����ļ�����
           Close #FileNumber
           UTF8ToAnsi = True
        Else
           UTF8ToAnsi = False: Exit Function
        End If
End Function

'Unicode(Little Endian)�ı��ļ�ת��ΪAnsi���ı��ļ�
Public Function ULEToAnsi(ByVal InputULEfile As String, ByVal OutputAnsifile As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUnicodeBuffer() As Byte, S As String
        'Dim i As Long
       
        On Error Resume Next
       
        '��Unicode(Little Endian)�ı��ļ�InputULEfile
        FileNumber = FreeFile
        If Dir(InputULEfile) = "" Then ULEToAnsi = False: Exit Function
        Open InputULEfile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        If Hex$(Filebyte(0)) = "FF" And Hex$(Filebyte(1)) = "FE" Then
           S = Filebyte
        Else
           MsgBox (InputULEfile & " Ϊ��Unicode(Little Endian)�����ʽ�ļ�!")
           ULEToAnsi = False: Exit Function
        End If
        sAnsi = StrConv(S, vbNarrow)  'ת��ΪVB6����ʾ���ַ���
        '������ط���Ӧ��˵���Խ����ˣ�VB6��StrConvת����ֱ�ӽ�sAnsi�����ļ�����
        '��������APIת��ΪAnsi����
        sAnsi = S
        retLen = WideCharToMultiByte(CP_ACP, 0, StrPtr(sAnsi), -1, vbNullString, 0, vbNullString, 0) 'ȡ��ת������Ҫ�Ŀռ��СretLen
       
        If retLen > 0 Then
           ReDim sUnicodeBuffer(retLen * 2 - 1) ' String$(retLen * 2, vbNullChar)'���û�������С
           retLen = WideCharToMultiByte(CP_ACP, 0, StrPtr(sAnsi), -1, sUnicodeBuffer(0), retLen * 2, vbNullString, 0) '��ʼת��
        Else
           ULEToAnsi = False: Exit Function
        End If
       
        '����ΪAnsi���ı��ļ�OutputAnsifile
        If retLen > 0 Then
           ReDim Preserve sUnicodeBuffer(retLen - 1)
           S = StrConv(sUnicodeBuffer, vbUnicode)
           Mid$(S, 1, 1) = " ": S = Trim(S)
           FileNumber = FreeFile
           If Dir(OutputAnsifile) <> "" Then Kill (OutputAnsifile)
           Open OutputAnsifile For Binary As #FileNumber
           Put #FileNumber, , S '�����ļ�����
           Close #FileNumber
           ULEToAnsi = True
        Else
           ULEToAnsi = False: Exit Function
        End If
End Function

'Unicode(Little Endian)�ı��ļ�ת��ΪUnicode Big Endian�ı��ļ���
'Unicode Big Endian�ı��ļ�ת��ΪUnicode(Little Endian)�ı��ļ���
'ֻ�뽫Hex$(Filebyte(0)) = "FF" And Hex$(Filebyte(1)) = "FE"��Ϊ
'Hex$(Filebyte(0)) = "FE" And Hex$(Filebyte(1)) = "FF"���ɡ�
Public Function ULEToUBE(ByVal InputULEfile As String, ByVal OutputUBEfile As String) As Boolean
        Dim Filebyte() As Byte, Fbyte() As Byte
        'Dim sAnsi As String, retLen As Long
        'Dim sUnicodeBuffer() As Byte, S As String
        Dim i As Long, FileNumber As Long
       
        On Error Resume Next
       
        '��Unicode(Little Endian)�ı��ļ�InputULEfile
        FileNumber = FreeFile
        If Dir(InputULEfile) = "" Then ULEToUBE = False: Exit Function
        Open InputULEfile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1), Fbyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
       
        If Hex$(Filebyte(0)) = "FF" And Hex$(Filebyte(1)) = "FE" Then
           'Unicode(Little Endian)�����ʽ�ļ�
        Else
           MsgBox (InputULEfile & " Ϊ��Unicode(Little Endian)�����ʽ�ļ�!")
           ULEToUBE = False: Exit Function
        End If
       
        For i = 0 To UBound(Filebyte)
            If i Mod 2 = 0 Then
               Fbyte(i) = Filebyte(i + 1)
            Else
               Fbyte(i) = Filebyte(i - 1)
            End If
        Next
               
        '����ΪUnicode Big Endian�ı��ļ�OutputUBEfile
       
        FileNumber = FreeFile
        If Dir(OutputUBEfile) <> "" Then Kill (OutputUBEfile)
        Open OutputUBEfile For Binary As #FileNumber
        Put #FileNumber, , Fbyte '�����ļ�����
        Close #FileNumber
End Function

'Unicode(Little Endian)�ı��ļ�ת��ΪUTF-8�ı��ļ�
Public Function ULEToUTF8(ByVal InputULEfile As String, ByVal OutputUTF8file As String) As Boolean
        Dim Filebyte() As Byte ', Fbyte() As Byte
        Dim sAnsi As String, retLen As Long, FileNumber As Long
        Dim sUTF8Buffer() As Byte, S As String
       
        On Error Resume Next
       
        '��Unicode(Little Endian)�ı��ļ�InputULEfile
        FileNumber = FreeFile
        If Dir(InputULEfile) = "" Then ULEToUTF8 = False: Exit Function
        Open InputULEfile For Binary As #FileNumber
        ReDim Filebyte(LOF(FileNumber) - 1)
        Get #FileNumber, , Filebyte
        Close #FileNumber
        If Hex$(Filebyte(0)) = "FF" And Hex$(Filebyte(1)) = "FE" Then
           S = Filebyte
        Else
           MsgBox (InputULEfile & " Ϊ��Unicode(Little Endian)�����ʽ�ļ�!")
           ULEToUTF8 = False: Exit Function
        End If
        sAnsi = StrConv(S, vbNarrow)  'ת��ΪVB6����ʾ���ַ���
        Mid$(sAnsi, 1, 1) = " ": sAnsi = Trim(sAnsi)
        retLen = WideCharToMultiByte(CP_UTF8, 0, StrPtr(sAnsi), -1, vbNullString, 0, vbNullString, 0) 'ȡ��ת������Ҫ�Ŀռ��СretLen
       
        If retLen > 0 Then
           ReDim sUTF8Buffer(retLen - 1) ' = String$(retLen, vbNullChar) '���û�������С
           retLen = WideCharToMultiByte(CP_UTF8, 0, StrPtr(sAnsi), -1, sUTF8Buffer(0), retLen, vbNullString, 0) '��ʼת��
        Else
           ULEToUTF8 = False: Exit Function
        End If
       
        '����ΪUTF-8�ı��ļ�OutputUTF8file
        If retLen > 0 Then
           ReDim Preserve sUTF8Buffer(retLen - 1)
           S = StrConv(sUTF8Buffer, vbUnicode)
           FileNumber = FreeFile
           If Dir(OutputUTF8file) <> "" Then Kill (OutputUTF8file)
           Open OutputUTF8file For Binary As #FileNumber
           Put #FileNumber, , &HBFBBEF '����UTF-8�ļ�ͷBOM��־EFBBBF
           Put #FileNumber, 4, S '�����ļ�����
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
'        '���½�һ��Ansi���ı��ļ�"d:\AnsiCodeFile.txt"
'        'Ansi���ı��ļ�ת��ΪUnicode(Little Endian)�ı��ļ�
'        Call AnsiToULE("d:\AnsiCodeFile.txt", "d:\AnsiToUnicodeLEFile.txt")
'
'        'Ansi���ı��ļ�ת��ΪUnicode(Big Endian)�ı��ļ�
'        Call AnsiToUBE("d:\AnsiCodeFile.txt", "d:\AnsiToUnicodeBEFile.txt")
'
'        'Ansi���ı��ļ�ת��ΪUTF-8�ı��ļ�
'        Call AnsiToUTF8("d:\AnsiCodeFile.txt", "d:\AnsiToUTF8File.txt")
'
'        'UTF-8�ı��ļ�ת��ΪUnicode(Little Endian)�ı��ļ�
'        Call UTF8ToULE("d:\AnsiToUTF8File.txt", "d:\UTF8ToUnicodeLEFile.txt")
'
'        'UTF-8�ı��ļ�ת��ΪUnicode Big Endian�ı��ļ�
'        Call UTF8ToUBE("d:\AnsiToUTF8File.txt", "d:\UTF8ToUnicodeBEFile.txt")
'
'        'UTF-8�ı��ļ�ת��ΪAnsi���ı��ļ�
'        Call UTF8ToAnsi("d:\AnsiToUTF8File.txt", "d:\UTF8ToAnsiFile.txt")
'
'        'Unicode(Little Endian)�ı��ļ�ת��ΪAnsi���ı��ļ�
'        Call ULEToAnsi("d:\AnsiToUnicodeLEFile.txt", "d:\UnicodeLEToAnsiFile.txt")
'
'        'Unicode(Little Endian)�ı��ļ�ת��ΪUnicode Big Endian�ı��ļ�
'        Call ULEToUBE("d:\AnsiToUnicodeLEFile.txt", "d:\UnicodeLEToUnicodeBEFile.txt")
'
'        'Unicode(Little Endian)�ı��ļ�ת��ΪUTF-8�ı��ļ�
'        Call ULEToUTF8("d:\AnsiToUnicodeLEFile.txt", "d:\UnicodeLEToUTF8File.txt")
'End Sub
