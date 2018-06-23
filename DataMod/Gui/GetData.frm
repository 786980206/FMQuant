VERSION 5.00
Begin VB.Form GetData 
   Appearance      =   0  'Flat
   BackColor       =   &H80000005&
   BorderStyle     =   0  'None
   Caption         =   "GetData"
   ClientHeight    =   6465
   ClientLeft      =   5535
   ClientTop       =   3255
   ClientWidth     =   10200
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   431
   ScaleMode       =   3  'Pixel
   ScaleWidth      =   680
   ShowInTaskbar   =   0   'False
   Begin VB.Frame Frame2 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "信息确认"
      ForeColor       =   &H80000008&
      Height          =   6375
      Left            =   5160
      TabIndex        =   5
      Top             =   0
      Width           =   4935
      Begin VB.ListBox TASK_LIST 
         Appearance      =   0  'Flat
         Height          =   5070
         IntegralHeight  =   0   'False
         Left            =   120
         TabIndex        =   12
         Top             =   240
         Width           =   4695
      End
      Begin 工程1.N_TextBox SAVE_PATH 
         Height          =   375
         Left            =   120
         TabIndex        =   11
         Top             =   5400
         Width           =   4695
         _ExtentX        =   8281
         _ExtentY        =   661
         Text            =   "Super TextBox"
         AlignementHorizontal=   2
         NumberBox       =   0   'False
         AlignementVertical=   1
         Locked          =   0   'False
         Enabled         =   -1  'True
         ForeColor       =   13655080
         BorderColor     =   13655080
         BackColor       =   16777215
         BeginProperty FONT {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Arial"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         LabelBox        =   0   'False
         SelOnFocus      =   -1  'True
         Header          =   0   'False
         HeaderAlignement=   2
         HeaderForeColor =   -2147483640
         HeaderBackColor =   -2147483633
         BeginProperty HeaderFont {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   6.75
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         HeaderCaption   =   "Header"
      End
      Begin 工程1.N_Shape N_Shape5 
         Height          =   375
         Left            =   120
         TabIndex        =   13
         Top             =   5880
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "GetData.frx":0000
         Picture_Down    =   "GetData.frx":001C
         Picture_Hover   =   "GetData.frx":0038
         Stretch         =   0   'False
         Caption         =   " 手动添加 "
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   11776947
         BorderColorHover=   11776947
         BorderColorDown =   11776947
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         BorderCustom    =   11776947
         Style           =   0
         ForeColorNormal =   0
         ForeColorHover  =   0
         ForeColorDown   =   0
         Text_Visible    =   -1  'True
      End
      Begin 工程1.N_Shape N_Shape6 
         Height          =   375
         Left            =   1320
         TabIndex        =   14
         Top             =   5880
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "GetData.frx":0054
         Picture_Down    =   "GetData.frx":0070
         Picture_Hover   =   "GetData.frx":008C
         Stretch         =   0   'False
         Caption         =   " 删除任务 "
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   11776947
         BorderColorHover=   11776947
         BorderColorDown =   11776947
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         BorderCustom    =   11776947
         Style           =   0
         ForeColorNormal =   0
         ForeColorHover  =   0
         ForeColorDown   =   0
         Text_Visible    =   -1  'True
      End
      Begin 工程1.N_Shape N_Shape7 
         Height          =   375
         Left            =   2520
         TabIndex        =   15
         Top             =   5880
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "GetData.frx":00A8
         Picture_Down    =   "GetData.frx":00C4
         Picture_Hover   =   "GetData.frx":00E0
         Stretch         =   0   'False
         Caption         =   " 保存列表 "
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   11776947
         BorderColorHover=   11776947
         BorderColorDown =   11776947
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         BorderCustom    =   11776947
         Style           =   0
         ForeColorNormal =   0
         ForeColorHover  =   0
         ForeColorDown   =   0
         Text_Visible    =   -1  'True
      End
      Begin 工程1.N_Shape N_Shape8 
         Height          =   375
         Left            =   3720
         TabIndex        =   16
         Top             =   5880
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "GetData.frx":00FC
         Picture_Down    =   "GetData.frx":0118
         Picture_Hover   =   "GetData.frx":0134
         Stretch         =   0   'False
         Caption         =   " 开始获取 "
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   11776947
         BorderColorHover=   11776947
         BorderColorDown =   11776947
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         BorderCustom    =   11776947
         Style           =   0
         ForeColorNormal =   0
         ForeColorHover  =   0
         ForeColorDown   =   0
         Text_Visible    =   -1  'True
      End
   End
   Begin VB.Frame Frame1 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "参数设置"
      ForeColor       =   &H80000008&
      Height          =   6375
      Left            =   120
      TabIndex        =   0
      Top             =   0
      Width           =   4935
      Begin VB.ListBox FIELDS 
         Appearance      =   0  'Flat
         BeginProperty Font 
            Name            =   "微软雅黑"
            Size            =   9
            Charset         =   134
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   4575
         IntegralHeight  =   0   'False
         Left            =   2520
         MultiSelect     =   2  'Extended
         TabIndex        =   10
         Top             =   1200
         Width           =   2295
      End
      Begin 工程1.N_Shape N_Shape2 
         Height          =   375
         Left            =   1320
         TabIndex        =   4
         Top             =   5880
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "GetData.frx":0150
         Picture_Down    =   "GetData.frx":016C
         Picture_Hover   =   "GetData.frx":0188
         Stretch         =   0   'False
         Caption         =   " 代码选择 "
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   11776947
         BorderColorHover=   11776947
         BorderColorDown =   11776947
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         BorderCustom    =   11776947
         Style           =   0
         ForeColorNormal =   0
         ForeColorHover  =   0
         ForeColorDown   =   0
         Text_Visible    =   -1  'True
      End
      Begin 工程1.N_Shape N_Shape1 
         Height          =   375
         Left            =   120
         TabIndex        =   3
         Top             =   5880
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "GetData.frx":01A4
         Picture_Down    =   "GetData.frx":01C0
         Picture_Hover   =   "GetData.frx":01DC
         Stretch         =   0   'False
         Caption         =   " 代码选择 "
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   11776947
         BorderColorHover=   11776947
         BorderColorDown =   11776947
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         BorderCustom    =   11776947
         Style           =   0
         ForeColorNormal =   0
         ForeColorHover  =   0
         ForeColorDown   =   0
         Text_Visible    =   -1  'True
      End
      Begin VB.ListBox CODE_LIST 
         Appearance      =   0  'Flat
         Height          =   5070
         IntegralHeight  =   0   'False
         Left            =   120
         MultiSelect     =   2  'Extended
         TabIndex        =   2
         Top             =   720
         Width           =   2295
      End
      Begin 工程1.SComboBox DATA_TYPE 
         Height          =   315
         Left            =   120
         TabIndex        =   1
         Top             =   240
         Width           =   2295
         _ExtentX        =   4048
         _ExtentY        =   556
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "宋体"
            Size            =   9
            Charset         =   134
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         MaxListLength   =   -1
         NumberItemsToShow=   -1
         ShadowColorText =   6908265
         Text            =   "K_DAY"
      End
      Begin 工程1.N_TextBox TIME_END 
         Height          =   375
         Left            =   2520
         TabIndex        =   6
         Top             =   720
         Width           =   2295
         _ExtentX        =   4048
         _ExtentY        =   661
         Text            =   "2018-02-05"
         AlignementHorizontal=   2
         NumberBox       =   0   'False
         AlignementVertical=   1
         Locked          =   0   'False
         Enabled         =   -1  'True
         ForeColor       =   13655080
         BorderColor     =   13655080
         BackColor       =   16777215
         BeginProperty FONT {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Arial"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         LabelBox        =   0   'False
         SelOnFocus      =   -1  'True
         Header          =   0   'False
         HeaderAlignement=   2
         HeaderForeColor =   -2147483640
         HeaderBackColor =   -2147483633
         BeginProperty HeaderFont {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   6.75
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         HeaderCaption   =   "Header"
      End
      Begin 工程1.N_TextBox TIME_START 
         Height          =   375
         Left            =   2520
         TabIndex        =   7
         Top             =   240
         Width           =   2295
         _ExtentX        =   4048
         _ExtentY        =   661
         Text            =   "2018-02-01"
         AlignementHorizontal=   2
         NumberBox       =   0   'False
         AlignementVertical=   1
         Locked          =   0   'False
         Enabled         =   -1  'True
         ForeColor       =   13655080
         BorderColor     =   13655080
         BackColor       =   16777215
         BeginProperty FONT {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Arial"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         LabelBox        =   0   'False
         SelOnFocus      =   -1  'True
         Header          =   0   'False
         HeaderAlignement=   2
         HeaderForeColor =   -2147483640
         HeaderBackColor =   -2147483633
         BeginProperty HeaderFont {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   6.75
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         HeaderCaption   =   "Header"
      End
      Begin 工程1.N_Shape N_Shape3 
         Height          =   375
         Left            =   2520
         TabIndex        =   8
         Top             =   5880
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "GetData.frx":01F8
         Picture_Down    =   "GetData.frx":0214
         Picture_Hover   =   "GetData.frx":0230
         Stretch         =   0   'False
         Caption         =   " 代码选择 "
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   11776947
         BorderColorHover=   11776947
         BorderColorDown =   11776947
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         BorderCustom    =   11776947
         Style           =   0
         ForeColorNormal =   0
         ForeColorHover  =   0
         ForeColorDown   =   0
         Text_Visible    =   -1  'True
      End
      Begin 工程1.N_Shape N_Shape4 
         Height          =   375
         Left            =   3720
         TabIndex        =   9
         Top             =   5880
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "GetData.frx":024C
         Picture_Down    =   "GetData.frx":0268
         Picture_Hover   =   "GetData.frx":0284
         Stretch         =   0   'False
         Caption         =   " 添加任务 "
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   11776947
         BorderColorHover=   11776947
         BorderColorDown =   11776947
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "Verdana"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         BorderCustom    =   11776947
         Style           =   0
         ForeColorNormal =   0
         ForeColorHover  =   0
         ForeColorDown   =   0
         Text_Visible    =   -1  'True
      End
   End
   Begin VB.Menu 文件 
      Caption         =   "文件"
      Index           =   1
      Begin VB.Menu 打开 
         Caption         =   "打开"
      End
   End
   Begin VB.Menu 设置 
      Caption         =   "设置"
   End
End
Attribute VB_Name = "GetData"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
    Public DataDef As String
Public Setting As String
Public PythonPath As String
Public PY_GetData_Path As String


'#################################### 窗体加载 ########################################################
Private Sub Form_Load()
22
    '清除缓存文件
    Kill App.Path + "\Cache\TempTaskList.gd"
    Kill App.Path + "\Cache\TaskList.gd"
    Kill App.Path + "\Cache\CodeSelect.gdret"
    Kill App.Path + "\Cache\CodeSelect.gd"
    MkDir App.Path + "\SaveFile"
    MkDir App.Path + "\Cache"
    '读取配置文件
    SAVE_PATH.Text = App.Path + "\SaveFile\"
    DataDef = CodeTran.ReadUTF8File("..\DataDef.py")
    Setting = CodeTran.ReadUTF8File("Setting\Setting.ini")
    '调试的时候要用下面这个
    DataDef = CodeTran.ReadUTF8File("E:\OneDrive\0_Coding\010_MyQuantSystem\Beta3.0\DataMod\DataDef.py")
    '------------------------------------
    PythonPath = UsedMod.GetEnumList("BASIC_CONFIG", Setting)(0)
    PY_GetData_Path = UsedMod.GetEnumList("BASIC_CONFIG", Setting)(1)
    Enum_DATA_TYPE = UsedMod.GetEnumList("DATA_TYPE", DataDef)
    '填充数据类型选择
    '在ComBox中添加
    For i = 0 To UBound(Enum_DATA_TYPE)
        DATA_TYPE.AddItem (Enum_DATA_TYPE(i))
    Next
    Call DATA_TYPE_SelectionMade("K_DAY", 0)
End Sub
'#################################### 数据类型选择 ####################################################
Private Sub DATA_TYPE_SelectionMade(ByVal SelectedItem As String, ByVal SelectedItemIndex As Long)
    On Error Resume Next
    FIELDS.Clear
    TempFields = UsedMod.GetEnumList("FIELDS_" + DATA_TYPE.Text, DataDef)
    For i = 0 To UBound(TempFields)
        FIELDS.AddItem (TempFields(i))
    Next
End Sub
'#################################### 关闭窗口按钮 #################################################
Private Sub Form_Unload(Cancel As Integer)
    On Error Resume Next
    Unload CodeSelect
    Unload TaskInfo
End Sub

'#################################### 代码选择按钮 ####################################################
Private Sub N_Shape1_Click()
    CodeSelect.Show vbModal, Me
End Sub
'#################################### 添加任务按钮 ####################################################
Private Sub N_Shape4_Click()
    AimCodeList = UsedMod.GetListBoxSelectedText(CODE_LIST)
    AimTimeList = "'" + TIME_START.Text + "','" + TIME_END.Text + "'"
    AimFields = UsedMod.GetListBoxSelectedText(FIELDS)
    AimDataType = DATA_TYPE.Text
    AimStr = UsedMod.MakeGetDataStr(AimCodeList, AimTimeList, AimFields, AimDataType)
    ret = CodeTran.AddUTF8File(AimStr + vbNewLine + "---" + vbNewLine, App.Path + "\Cache\TempTaskList.gd")
    TASK_LIST.AddItem (AimStr)
End Sub
'#################################### 手动添加任务按钮 #################################################
Private Sub N_Shape5_Click()
    TaskInfo.N_Shape2.Enabled = False
    TaskInfo.N_TextBox1.Text = "[]"
    TaskInfo.N_TextBox2.Text = "[]"
    TaskInfo.N_TextBox3.Text = "[]"
    TaskInfo.N_TextBox4.Text = "'K_DAY'"
    TaskInfo.N_TextBox5.Text = "'Default'"
    TaskInfo.N_TextBox6.Text = "'CycleAll'"
    TaskInfo.N_TextBox7.Text = "{}"
    TaskInfo.Show vbModal, Me
End Sub
'#################################### 删除任务按钮 #################################################
Private Sub N_Shape6_Click()
    'MsgBox TASK_LIST.ListIndex
    If TASK_LIST.ListIndex <> -1 Then
        TempTaskList = CodeTran.ReadUTF8File(App.Path + "\Cache\TempTaskList.gd")
        TempTaskInfo = Split(TempTaskList, vbNewLine + "---" + vbNewLine)
        For i = 0 To UBound(TempTaskInfo)
            If TempTaskInfo(i) <> "" And i <> TASK_LIST.ListIndex Then
                AimStr = AimStr + TempTaskInfo(i) + vbNewLine + "---" + vbNewLine
            End If
        Next
        ret = CodeTran.WriteUTF8File(AimStr, App.Path + "\Cache\TempTaskList.gd")
        Call UsedMod.TaskFile2List
    End If
End Sub
'#################################### 保存任务列表按钮 #################################################
Private Sub N_Shape7_Click()
    SavePath = InputBox("请输入保存路径，如“C:\Test.gd”或 “Test.gd”储存在SaveFile文件夹下面。", "保存路径", "Test.gd")
    If InStr(SavePath, "\") <> 0 Then
        FileCopy App.Path + "\Cache\TempTaskList.gd", SavePath
    Else
        FileCopy App.Path + "\Cache\TempTaskList.gd", App.Path + "\SaveFile\" + SavePath
    End If
End Sub
'#################################### 开始获取数据按钮 #################################################
Private Sub N_Shape8_Click()
    If TASK_LIST.ListCount = 0 Then Exit Sub
    TempStr = CodeTran.ReadUTF8File(App.Path + "\Cache\TempTaskList.gd")
    SavePath = SAVE_PATH.Text
    AimStr = SavePath + vbNewLine + TempStr
    ret = CodeTran.WriteUTF8File(AimStr, App.Path + "\Cache\TaskList.gd")
    
    ret = UsedMod.PyExWithoutWait(GetData.PythonPath, GetData.PY_GetData_Path, App.Path + "\Cache\TaskList.gd")
    Wait4Data.Show vbModal, Me
    
    'Wait4Data.Show vbModal, Me
    
End Sub

'#################################### 双击TASK_LISTTASK_LIST修改任务按钮 ################################
Private Sub TASK_LIST_DblClick()
    TempTaskList = CodeTran.ReadUTF8File(App.Path + "\Cache\TempTaskList.gd")
    TempTaskInfo = Split(TempTaskList, vbNewLine + "---" + vbNewLine)
    TaskInfo.N_Shape1.Enabled = False
    TempInfo = Split(TempTaskInfo(TASK_LIST.ListIndex), vbNewLine)
    TaskInfo.N_TextBox1.Text = Mid(TempInfo(1), InStr(TempInfo(1), "=") + 1)
    TaskInfo.N_TextBox2.Text = Mid(TempInfo(2), InStr(TempInfo(2), "=") + 1)
    TaskInfo.N_TextBox3.Text = Mid(TempInfo(3), InStr(TempInfo(3), "=") + 1)
    TaskInfo.N_TextBox4.Text = Mid(TempInfo(4), InStr(TempInfo(4), "=") + 1)
    TaskInfo.N_TextBox5.Text = Mid(TempInfo(5), InStr(TempInfo(5), "=") + 1)
    TaskInfo.N_TextBox6.Text = Mid(TempInfo(6), InStr(TempInfo(6), "=") + 1)
    TaskInfo.N_TextBox7.Text = Mid(TempInfo(7), InStr(TempInfo(7), "=") + 1)
    TaskInfo.Show vbModal, Me
End Sub

