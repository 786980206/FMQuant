VERSION 5.00
Begin VB.Form Wait4Data 
   Appearance      =   0  'Flat
   BackColor       =   &H80000005&
   Caption         =   "获取数据中"
   ClientHeight    =   1665
   ClientLeft      =   7860
   ClientTop       =   5745
   ClientWidth     =   4485
   LinkTopic       =   "Form1"
   ScaleHeight     =   1665
   ScaleWidth      =   4485
   Begin VB.TextBox N_TextBox1 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      Height          =   975
      Left            =   120
      MultiLine       =   -1  'True
      TabIndex        =   3
      Text            =   "Wait4Data.frx":0000
      Top             =   120
      Width           =   4215
   End
   Begin 工程1.N_Shape N_Shape1 
      Height          =   375
      Left            =   240
      TabIndex        =   0
      Top             =   1200
      Width           =   1320
      _ExtentX        =   2328
      _ExtentY        =   661
      Picture_Normal  =   "Wait4Data.frx":0006
      Picture_Down    =   "Wait4Data.frx":0022
      Picture_Hover   =   "Wait4Data.frx":003E
      Stretch         =   0   'False
      Caption         =   "打开储存目录"
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
   Begin 工程1.N_Shape N_Shape2 
      Height          =   375
      Left            =   1800
      TabIndex        =   1
      Top             =   1200
      Width           =   960
      _ExtentX        =   1693
      _ExtentY        =   661
      Picture_Normal  =   "Wait4Data.frx":005A
      Picture_Down    =   "Wait4Data.frx":0076
      Picture_Hover   =   "Wait4Data.frx":0092
      Stretch         =   0   'False
      Caption         =   "停止等待"
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
   Begin 工程1.N_Shape N_Shape3 
      Height          =   375
      Left            =   3120
      TabIndex        =   2
      Top             =   1200
      Width           =   1110
      _ExtentX        =   1958
      _ExtentY        =   661
      Picture_Normal  =   "Wait4Data.frx":00AE
      Picture_Down    =   "Wait4Data.frx":00CA
      Picture_Hover   =   "Wait4Data.frx":00E6
      Stretch         =   0   'False
      Caption         =   "N_Shape1"
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
Attribute VB_Name = "Wait4Data"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'Option Explicit
Dim SavePath As String
Private Sub Form_Activate()
    DoEvents
    N_Shape1.Enabled = False
    N_TextBox1.Text = "等待加载数据文件夹"
    Do While Dir(App.Path & "\Cache\TaskSavePath.tmp") = ""
        '不存在
        'MsgBox ("不存在")
        UsedMod.Sleep2 300 'ms
    Loop
    '存在
    SavePath = CodeTran.ReadUTF8File(App.Path & "\Cache\TaskSavePath.tmp")
    Kill App.Path & "\Cache\TaskSavePath.tmp"
    N_TextBox1.Text = "开始下载数据"
    '开始逐任务下载
    Do While Dir(App.Path & "\Cache\TaskRet.tmp") = ""
        '不存在
        UsedMod.Sleep2 300 'ms
    Loop
    N_Shape1.Enabled = True
    Condition = True
    Do While Condition = True
        TempRet = CodeTran.ReadUTF8File(App.Path & "\Cache\TaskRet.tmp")
        TempA = Split(TempRet, "Task")
        TempStr = Left(TempA(UBound(TempA)), InStr(TempA(UBound(TempA)), " ") - 1)
        TempStr = Replace(TempStr, vbNewLine, "")
        N_TextBox1.Text = "当前任务(" + Str(TempStr) + "/" + Str(GetData.TASK_LIST.ListCount) + "):" + vbNewLine + TempRet
        UsedMod.Sleep2 300 'ms
        If TempStr = CStr(GetData.TASK_LIST.ListCount) Then Condition = False
    Loop
    Kill App.Path & "\Cache\TaskRet.tmp"
End Sub

Private Sub N_Shape1_Click()
    UsedMod.Cmd ("explorer " + SavePath)
End Sub
Private Sub N_Shape2_Click()
    On Error Resume Next
    Kill App.Path & "\Cache\TaskRet.tmp"
    Kill App.Path & "\Cache\TaskSavePath.tmp"
    Unload Me
    
End Sub
