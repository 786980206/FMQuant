VERSION 5.00
Begin VB.Form TaskInfo 
   Appearance      =   0  'Flat
   BackColor       =   &H80000005&
   BorderStyle     =   1  'Fixed Single
   Caption         =   "任务信息"
   ClientHeight    =   4140
   ClientLeft      =   9045
   ClientTop       =   3660
   ClientWidth     =   3630
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   4140
   ScaleWidth      =   3630
   Begin 工程1.N_Shape N_Shape1 
      Height          =   375
      Left            =   1320
      TabIndex        =   14
      Top             =   3600
      Width           =   1020
      _ExtentX        =   1799
      _ExtentY        =   661
      Picture_Normal  =   "TaskInfo.frx":0000
      Picture_Down    =   "TaskInfo.frx":001C
      Picture_Hover   =   "TaskInfo.frx":0038
      Stretch         =   0   'False
      Caption         =   "   添 加   "
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
   Begin 工程1.N_TextBox N_TextBox1 
      Height          =   375
      Left            =   1560
      TabIndex        =   0
      Top             =   120
      Width           =   1815
      _ExtentX        =   3201
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
   Begin 工程1.N_TextBox N_TextBox2 
      Height          =   375
      Left            =   1560
      TabIndex        =   1
      Top             =   600
      Width           =   1815
      _ExtentX        =   3201
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
   Begin 工程1.N_TextBox N_TextBox3 
      Height          =   375
      Left            =   1560
      TabIndex        =   2
      Top             =   1080
      Width           =   1815
      _ExtentX        =   3201
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
   Begin 工程1.N_TextBox N_TextBox4 
      Height          =   375
      Left            =   1560
      TabIndex        =   3
      Top             =   1560
      Width           =   1815
      _ExtentX        =   3201
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
   Begin 工程1.N_TextBox N_TextBox5 
      Height          =   375
      Left            =   1560
      TabIndex        =   4
      Top             =   2040
      Width           =   1815
      _ExtentX        =   3201
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
   Begin 工程1.N_TextBox N_TextBox6 
      Height          =   375
      Left            =   1560
      TabIndex        =   5
      Top             =   2520
      Width           =   1815
      _ExtentX        =   3201
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
   Begin 工程1.N_TextBox N_TextBox7 
      Height          =   375
      Left            =   1560
      TabIndex        =   6
      Top             =   3000
      Width           =   1815
      _ExtentX        =   3201
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
   Begin 工程1.N_Shape N_Shape2 
      Height          =   375
      Left            =   2400
      TabIndex        =   15
      Top             =   3600
      Width           =   900
      _ExtentX        =   1588
      _ExtentY        =   661
      Picture_Normal  =   "TaskInfo.frx":0054
      Picture_Down    =   "TaskInfo.frx":0070
      Picture_Hover   =   "TaskInfo.frx":008C
      Stretch         =   0   'False
      Caption         =   "  保 存  "
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
   Begin VB.Label Label7 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "SpecialConfig:"
      ForeColor       =   &H80000008&
      Height          =   180
      Left            =   0
      TabIndex        =   13
      Top             =   3120
      Width           =   1500
   End
   Begin VB.Label Label6 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "DataSource:"
      ForeColor       =   &H80000008&
      Height          =   180
      Left            =   0
      TabIndex        =   12
      Top             =   2640
      Width           =   1500
   End
   Begin VB.Label Label5 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "GroupByType:"
      ForeColor       =   &H80000008&
      Height          =   180
      Left            =   0
      TabIndex        =   11
      Top             =   2160
      Width           =   1500
   End
   Begin VB.Label Label4 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "DataType:"
      ForeColor       =   &H80000008&
      Height          =   180
      Left            =   0
      TabIndex        =   10
      Top             =   1680
      Width           =   1500
   End
   Begin VB.Label Label3 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "Fields:"
      ForeColor       =   &H80000008&
      Height          =   180
      Left            =   0
      TabIndex        =   9
      Top             =   1200
      Width           =   1500
   End
   Begin VB.Label Label2 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "TimeList:"
      ForeColor       =   &H80000008&
      Height          =   180
      Left            =   0
      TabIndex        =   8
      Top             =   720
      Width           =   1500
   End
   Begin VB.Label Label1 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "CodeList:"
      ForeColor       =   &H80000008&
      Height          =   180
      Left            =   0
      TabIndex        =   7
      Top             =   240
      Width           =   1500
   End
End
Attribute VB_Name = "TaskInfo"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Sub N_Shape1_Click()
    '新加的gd
    TempStr = "GetDataStart:" + vbNewLine
    TempStr = TempStr + "CodeList=" + N_TextBox1.Text + vbNewLine
    TempStr = TempStr + "TimeList=" + N_TextBox2.Text + vbNewLine
    TempStr = TempStr + "Fields=" + N_TextBox3.Text + vbNewLine
    TempStr = TempStr + "DataType=" + N_TextBox4.Text + vbNewLine
    TempStr = TempStr + "GroupByType=" + N_TextBox5.Text + vbNewLine
    TempStr = TempStr + "DataSource=" + N_TextBox6.Text + vbNewLine
    TempStr = TempStr + "SpecialConfig=" + N_TextBox7.Text
    '重新保存文件
    AimStr = TempTaskList + TempStr + vbNewLine + "---" + vbNewLine
    ret = CodeTran.AddUTF8File(AimStr, App.Path + "\Cache\TempTaskList.gd")
    GetData.TASK_LIST.AddItem (AimStr)
    Call UsedMod.TaskFile2List
    Unload Me
End Sub

Private Sub N_Shape2_Click()
    TempTaskList = CodeTran.ReadUTF8File(App.Path + "\Cache\TempTaskList.gd")
    TempTaskInfo = Split(TempTaskList, vbNewLine + "---" + vbNewLine)
    TempStr = "GetDataStart:" + vbNewLine
    TempStr = TempStr + "CodeList=" + N_TextBox1.Text + vbNewLine
    TempStr = TempStr + "TimeList=" + N_TextBox2.Text + vbNewLine
    TempStr = TempStr + "Fields=" + N_TextBox3.Text + vbNewLine
    TempStr = TempStr + "DataType=" + N_TextBox4.Text + vbNewLine
    TempStr = TempStr + "GroupByType=" + N_TextBox5.Text + vbNewLine
    TempStr = TempStr + "DataSource=" + N_TextBox6.Text + vbNewLine
    TempStr = TempStr + "SpecialConfig=" + N_TextBox7.Text
    TempTaskInfo(GetData.TASK_LIST.ListIndex) = TempStr
    '########## 重新保存 ##################
    AimStr = ""
    For i = 0 To UBound(TempTaskInfo)
        If TempTaskInfo(i) <> "" Then
            AimStr = AimStr + TempTaskInfo(i) + vbNewLine + "---" + vbNewLine
        End If
    Next
    ret = CodeTran.WriteUTF8File(AimStr, App.Path + "\Cache\TempTaskList.gd")
    Call UsedMod.TaskFile2List
    Unload Me
End Sub
