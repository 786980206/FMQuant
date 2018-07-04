VERSION 5.00
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.0#0"; "MSCOMCTL.OCX"
Begin VB.Form CodeSelect 
   Caption         =   "选择证券"
   ClientHeight    =   6750
   ClientLeft      =   7440
   ClientTop       =   2640
   ClientWidth     =   5280
   LinkTopic       =   "Form1"
   ScaleHeight     =   6750
   ScaleWidth      =   5280
   Begin 工程1.N_Shape CB_SureSelect 
      Height          =   375
      Left            =   4080
      TabIndex        =   7
      Top             =   6240
      Width           =   1080
      _ExtentX        =   1905
      _ExtentY        =   661
      Picture_Normal  =   "CodeSelect.frx":0000
      Picture_Down    =   "CodeSelect.frx":001C
      Picture_Hover   =   "CodeSelect.frx":0038
      Stretch         =   0   'False
      Caption         =   "    确定    "
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
   Begin 工程1.N_Shape CB_AllSelect 
      Height          =   375
      Left            =   2880
      TabIndex        =   6
      Top             =   6240
      Width           =   1080
      _ExtentX        =   1905
      _ExtentY        =   661
      Picture_Normal  =   "CodeSelect.frx":0054
      Picture_Down    =   "CodeSelect.frx":0070
      Picture_Hover   =   "CodeSelect.frx":008C
      Stretch         =   0   'False
      Caption         =   "    全选    "
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
   Begin 工程1.N_Shape CB_getPlaeSymbol 
      Height          =   375
      Left            =   2880
      TabIndex        =   5
      Top             =   120
      Width           =   1200
      _ExtentX        =   2117
      _ExtentY        =   661
      Picture_Normal  =   "CodeSelect.frx":00A8
      Picture_Down    =   "CodeSelect.frx":00C4
      Picture_Hover   =   "CodeSelect.frx":00E0
      Stretch         =   0   'False
      Caption         =   "  获取代码  "
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
   Begin 工程1.N_TextBox TB_ManualSelect 
      Height          =   375
      Left            =   2880
      TabIndex        =   4
      Top             =   5760
      Width           =   2295
      _ExtentX        =   4048
      _ExtentY        =   661
      Text            =   ""
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
   Begin VB.ListBox LB_CodeList 
      Appearance      =   0  'Flat
      Height          =   4710
      Left            =   2880
      MultiSelect     =   1  'Simple
      Sorted          =   -1  'True
      TabIndex        =   2
      Top             =   600
      Width           =   2295
   End
   Begin VB.CommandButton Command1 
      Caption         =   "Command1"
      Height          =   495
      Left            =   10200
      TabIndex        =   1
      Top             =   4800
      Width           =   855
   End
   Begin MSComctlLib.TreeView TV_plate 
      Height          =   6495
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   2655
      _ExtentX        =   4683
      _ExtentY        =   11456
      _Version        =   393217
      LabelEdit       =   1
      LineStyle       =   1
      Style           =   7
      BorderStyle     =   1
      Appearance      =   0
   End
   Begin VB.Label LB_SelectInfo 
      Appearance      =   0  'Flat
      AutoSize        =   -1  'True
      BackColor       =   &H80000005&
      Caption         =   "手动输入:"
      ForeColor       =   &H80000008&
      Height          =   180
      Left            =   2880
      TabIndex        =   3
      Top             =   5520
      Width           =   690
   End
End
Attribute VB_Name = "CodeSelect"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'Option Explicit
Dim Plate As String
Dim RetCodeSelect As String
Public Msg2SendNum As Integer
Public SingleChoice As Boolean

Private Sub Form_Load()
RetCodeSelect = ""
Msg2SendNum = -1
SingleChoice = False
'添加板块分类
Dim nodx As Node
Plate = CommonUsedMod.ReadUTF8File(App.Path + "\..\DataMod\Gui\Setting\Plate.ini")
TempPlate = Split(Plate, vbCrLf)
'TV_plate.Nodes.Add
Set nodx = TV_plate.Nodes.Add(, , "P10", "股票")
Set nodx = TV_plate.Nodes.Add(, , "P13", "基金")
Set nodx = TV_plate.Nodes.Add(, , "P14", "指数")
Set nodx = TV_plate.Nodes.Add(, , "P17", "期货")
Set nodx = TV_plate.Nodes.Add(, , "P20", "债券")
Set nodx = TV_plate.Nodes.Add(, , "P21", "期权")
For i = 1 To UBound(TempPlate)
    Item = Split(TempPlate(i), ",")
    If Item(2) = "1级" Then
        'Set nodx = TV_plate.Nodes.Add(, , "P" + Item(4), Item(5) + "(" + Item(1) + ")")
        Set nodx = TV_plate.Nodes.Add("P" + Item(6), tvwChild, "P" + Item(4), Item(5) + "(" + Item(1) + ")")
    Else
        Set nodx = TV_plate.Nodes.Add("P" + Item(6), tvwChild, "P" + Item(4), Item(5) + "(" + Item(1) + ")")
    End If
Next
'nodx.EnsureVisible
End Sub

Private Sub CB_AllSelect_Click()
    If CB_AllSelect.Caption = "    全选    " Then
        For i = 0 To LB_CodeList.ListCount - 1
            LB_CodeList.Selected(i) = True
        Next
        CB_AllSelect.Caption = "    清空    "
    Else
        For i = 0 To LB_CodeList.ListCount - 1
            LB_CodeList.Selected(i) = False
        Next
        CB_AllSelect.Caption = "    全选    "
    End If
End Sub

Private Sub CB_getPlaeSymbol_Click()
    GTA_QTApi_PLATE_ID = Mid(TV_plate.SelectedItem.Key, 2)
    AimFields = "'Symbol','Market', 'ShortName'"
    AimDataType = "STOCK_BASIC"
    AimGroupType = "Default"
    AimDataSource = "GTA_QTApi"
    AimSpecialConfig = "'GTA_QTApi_PLATE_ID':'" + GTA_QTApi_PLATE_ID + "'"
    AimStr = MakeGetDataStr(, , AimFields, AimDataType, , AimDataSource, AimSpecialConfig)
    TempPath = App.Path + "\CodeSelect.gd"
    TempSavePath = App.Path + "\CodeSelect.gdret"
    ret = CommonUsedMod.WriteUTF8File(TempSavePath + vbNewLine + AimStr + vbNewLine + "---", TempPath)
    ret = CommonUsedMod.PyEx(Main.PythonPath, Main.PY_GetData_Path, TempPath)
    'UsedMod.Cmd3 ("E:\Miniconda3-Py3.5.2\python.exe E:/OneDrive/0_Coding/010_MyQuantSystem/Beta3.0/DataMod/GetData.py")
    '到这代表选股窗口选股成功-------------------------------------------------------
    LB_CodeList.Clear
    TempStr = CommonUsedMod.ReadUTF8File(TempSavePath)
    CodeStr = Split(TempStr, vbCrLf)
    For i = 1 To UBound(CodeStr)
        If CodeStr(i) <> "" Then
            TempCode = Split(CodeStr(i), ",")
            TempItem = TempCode(0) + "." + TempCode(1) + "  (" + TempCode(2) + ")"
            CodeSelect.LB_CodeList.AddItem (TempItem)
        End If
    Next
End Sub

Private Sub CB_SureSelect_Click()
    RetCodeSelect = CommonUsedMod.GetListBoxSelectedText(LB_CodeList)
'    RetCodeSelect = Replace(RetCodeSelect, "[", "")
'    RetCodeSelect = Replace(RetCodeSelect, "]", "")
    RetCodeSelect = Replace(RetCodeSelect, "'", "")
    If TB_ManualSelect.Text <> "" Then
        If RetCodeSelect <> "" Then
            RetCodeSelect = RetCodeSelect + "," + TB_ManualSelect.Text
        Else
            RetCodeSelect = TB_ManualSelect.Text
        End If
    End If
    '到这里已经选好股票了，形式如“000001.SZSE,000002.SZSE”
    TempCodeSelected = Split(RetCodeSelect, ",")
    Main.List2.Clear
    For i = 0 To UBound(TempCodeSelected)
        Main.List2.AddItem (TempCodeSelected(i))
        'Main.List2.Selected(i) = True
    Next
    On Error Resume Next
    Kill App.Path + "\CodeSelect.gd"
    Kill App.Path + "\CodeSelect.gdret"
    Unload CodeSelect
End Sub
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
Private Sub Command1_Click()
    MsgBox 1
End Sub


