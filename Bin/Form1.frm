VERSION 5.00
Begin VB.Form Main 
   Appearance      =   0  'Flat
   BackColor       =   &H80000005&
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "FMQuant"
   ClientHeight    =   9570
   ClientLeft      =   2790
   ClientTop       =   1335
   ClientWidth     =   14910
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   9570
   ScaleWidth      =   14910
   Begin VB.Frame Frame3 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "策略回测"
      ForeColor       =   &H80000008&
      Height          =   5895
      Left            =   3960
      TabIndex        =   7
      Top             =   3600
      Width           =   10815
      Begin 工程1.N_Shape N_Shape4 
         Height          =   375
         Left            =   9600
         TabIndex        =   35
         Top             =   5400
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "Form1.frx":0000
         Picture_Down    =   "Form1.frx":001C
         Picture_Hover   =   "Form1.frx":0038
         Stretch         =   0   'False
         Caption         =   " 开始回测 "
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
      Begin 工程1.CheckButton CheckButton1 
         Height          =   255
         Left            =   8400
         TabIndex        =   34
         Top             =   3600
         Width           =   1695
         _ExtentX        =   2990
         _ExtentY        =   450
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "宋体"
            Size            =   9
            Charset         =   134
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Caption         =   "显示回测窗口"
         BackColor       =   -2147483643
      End
      Begin 工程1.N_TextBox N_TextBox6 
         Height          =   375
         Left            =   5160
         TabIndex        =   33
         Top             =   4440
         Width           =   2775
         _ExtentX        =   4895
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
      Begin 工程1.N_TextBox N_TextBox5 
         Height          =   375
         Left            =   5160
         TabIndex        =   31
         Top             =   3960
         Width           =   2775
         _ExtentX        =   4895
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
      Begin 工程1.N_TextBox N_TextBox4 
         Height          =   375
         Left            =   5160
         TabIndex        =   29
         Top             =   3480
         Width           =   2775
         _ExtentX        =   4895
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
      Begin 工程1.N_TextBox N_TextBox3 
         Height          =   375
         Left            =   1080
         TabIndex        =   27
         Top             =   4440
         Width           =   2775
         _ExtentX        =   4895
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
      Begin 工程1.N_TextBox N_TextBox2 
         Height          =   375
         Left            =   1080
         TabIndex        =   25
         Top             =   3960
         Width           =   2775
         _ExtentX        =   4895
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
      Begin 工程1.N_TextBox N_TextBox1 
         Height          =   375
         Left            =   1080
         TabIndex        =   23
         Top             =   3480
         Width           =   2775
         _ExtentX        =   4895
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
      Begin VB.ListBox List5 
         Appearance      =   0  'Flat
         Height          =   2370
         Left            =   120
         TabIndex        =   20
         Top             =   600
         Width           =   10575
      End
      Begin 工程1.N_Shape N_Shape9 
         Height          =   375
         Left            =   8400
         TabIndex        =   40
         Top             =   5400
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "Form1.frx":0054
         Picture_Down    =   "Form1.frx":0070
         Picture_Hover   =   "Form1.frx":008C
         Stretch         =   0   'False
         Caption         =   " 保存参数 "
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
      Begin VB.Line Line3 
         X1              =   120
         X2              =   10680
         Y1              =   5280
         Y2              =   5280
      End
      Begin VB.Label Label14 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "市场参与："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   4200
         TabIndex        =   32
         Top             =   4560
         Width           =   900
      End
      Begin VB.Label Label13 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "交易滑点："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   4200
         TabIndex        =   30
         Top             =   4080
         Width           =   900
      End
      Begin VB.Label Label12 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "交易成本："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   4200
         TabIndex        =   28
         Top             =   3600
         Width           =   900
      End
      Begin VB.Label Label11 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "初始资金："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   120
         TabIndex        =   26
         Top             =   4560
         Width           =   900
      End
      Begin VB.Label Label10 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "结束日期："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   120
         TabIndex        =   24
         Top             =   4080
         Width           =   900
      End
      Begin VB.Label Label9 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "开始日期："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   120
         TabIndex        =   22
         Top             =   3560
         Width           =   900
      End
      Begin VB.Line Line2 
         X1              =   120
         X2              =   10680
         Y1              =   3360
         Y2              =   3360
      End
      Begin VB.Label Label8 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "回测参数："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   120
         TabIndex        =   21
         Top             =   3120
         Width           =   900
      End
      Begin VB.Label Label7 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "回测记录："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   120
         TabIndex        =   19
         Top             =   360
         Width           =   900
      End
   End
   Begin VB.Frame Frame2 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "策略参数"
      ForeColor       =   &H80000008&
      Height          =   3495
      Left            =   3960
      TabIndex        =   6
      Top             =   0
      Width           =   10815
      Begin 工程1.N_Shape N_Shape5 
         Height          =   195
         Left            =   1740
         TabIndex        =   36
         Top             =   360
         Width           =   375
         _ExtentX        =   661
         _ExtentY        =   344
         Picture_Normal  =   "Form1.frx":00A8
         Picture_Down    =   "Form1.frx":00C4
         Picture_Hover   =   "Form1.frx":00E0
         Stretch         =   0   'False
         Caption         =   "+"
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   -2147483642
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
      Begin 工程1.SComboBox SComboBox3 
         Height          =   375
         Left            =   7440
         TabIndex        =   18
         Top             =   1200
         Width           =   3255
         _ExtentX        =   5741
         _ExtentY        =   661
         AppearanceCombo =   13
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
         Text            =   ""
      End
      Begin 工程1.SComboBox SComboBox2 
         Height          =   375
         Left            =   7440
         TabIndex        =   15
         Top             =   720
         Width           =   3255
         _ExtentX        =   5741
         _ExtentY        =   661
         AppearanceCombo =   13
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
         Text            =   ""
      End
      Begin VB.ListBox List4 
         Appearance      =   0  'Flat
         Height          =   2730
         Left            =   4360
         TabIndex        =   12
         Top             =   600
         Width           =   2000
      End
      Begin VB.ListBox List3 
         Appearance      =   0  'Flat
         Height          =   2730
         Left            =   2240
         TabIndex        =   10
         Top             =   600
         Width           =   2000
      End
      Begin VB.ListBox List2 
         Appearance      =   0  'Flat
         Height          =   2730
         Left            =   120
         TabIndex        =   8
         Top             =   600
         Width           =   2000
      End
      Begin 工程1.N_Shape N_Shape6 
         Height          =   195
         Left            =   3855
         TabIndex        =   37
         Top             =   360
         Width           =   375
         _ExtentX        =   661
         _ExtentY        =   344
         Picture_Normal  =   "Form1.frx":00FC
         Picture_Down    =   "Form1.frx":0118
         Picture_Hover   =   "Form1.frx":0134
         Stretch         =   0   'False
         Caption         =   "+"
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   -2147483642
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
         Height          =   195
         Left            =   5975
         TabIndex        =   38
         Top             =   360
         Width           =   375
         _ExtentX        =   661
         _ExtentY        =   344
         Picture_Normal  =   "Form1.frx":0150
         Picture_Down    =   "Form1.frx":016C
         Picture_Hover   =   "Form1.frx":0188
         Stretch         =   0   'False
         Caption         =   "+"
         BackGround      =   15725042
         BackColorNormal =   15725042
         BackColorHover  =   14737632
         BackColorDown   =   16777215
         BorderColorNormal=   -2147483642
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
         Left            =   9600
         TabIndex        =   39
         Top             =   3000
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "Form1.frx":01A4
         Picture_Down    =   "Form1.frx":01C0
         Picture_Hover   =   "Form1.frx":01DC
         Stretch         =   0   'False
         Caption         =   " 保存参数 "
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
      Begin VB.Label Label6 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "行情频率："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   6480
         TabIndex        =   17
         Top             =   1300
         Width           =   900
      End
      Begin VB.Label Label5 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "行情类型："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   6480
         TabIndex        =   16
         Top             =   800
         Width           =   900
      End
      Begin VB.Line Line1 
         X1              =   6480
         X2              =   10680
         Y1              =   600
         Y2              =   600
      End
      Begin VB.Label Label4 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "行情参数："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   6480
         TabIndex        =   14
         Top             =   360
         Width           =   900
      End
      Begin VB.Label Label3 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "账户列表："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   4360
         TabIndex        =   13
         Top             =   360
         Width           =   900
      End
      Begin VB.Label Label2 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "订阅字段："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   2235
         TabIndex        =   11
         Top             =   360
         Width           =   900
      End
      Begin VB.Label Label1 
         Appearance      =   0  'Flat
         AutoSize        =   -1  'True
         BackColor       =   &H80000005&
         Caption         =   "订阅标的："
         ForeColor       =   &H80000008&
         Height          =   180
         Left            =   120
         TabIndex        =   9
         Top             =   360
         Width           =   900
      End
   End
   Begin VB.Frame Frame1 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "策略列表"
      ForeColor       =   &H80000008&
      Height          =   9495
      Left            =   120
      TabIndex        =   0
      Top             =   0
      Width           =   3735
      Begin 工程1.N_Shape N_Shape3 
         Height          =   375
         Left            =   2520
         TabIndex        =   5
         Top             =   9000
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "Form1.frx":01F8
         Picture_Down    =   "Form1.frx":0214
         Picture_Hover   =   "Form1.frx":0230
         Stretch         =   0   'False
         Caption         =   " 删除策略 "
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
         Left            =   1320
         TabIndex        =   4
         Top             =   9000
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "Form1.frx":024C
         Picture_Down    =   "Form1.frx":0268
         Picture_Hover   =   "Form1.frx":0284
         Stretch         =   0   'False
         Caption         =   " 编辑策略 "
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
         Top             =   9000
         Width           =   1080
         _ExtentX        =   1905
         _ExtentY        =   661
         Picture_Normal  =   "Form1.frx":02A0
         Picture_Down    =   "Form1.frx":02BC
         Picture_Hover   =   "Form1.frx":02D8
         Stretch         =   0   'False
         Caption         =   " 新建策略 "
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
      Begin 工程1.SComboBox SComboBox1 
         Height          =   435
         Left            =   120
         TabIndex        =   2
         Top             =   360
         Width           =   3495
         _ExtentX        =   6165
         _ExtentY        =   767
         Alignment       =   2
         AppearanceCombo =   13
         ArrowColor      =   12583104
         DisabledColor   =   65535
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "宋体"
            Size            =   9
            Charset         =   134
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         GradientColor1  =   65280
         MaxListLength   =   -1
         NumberItemsToShow=   -1
         ShadowColorText =   6908265
      End
      Begin VB.ListBox List1 
         Appearance      =   0  'Flat
         Height          =   7950
         Left            =   120
         TabIndex        =   1
         Top             =   960
         Width           =   3495
      End
   End
   Begin VB.Menu 文件 
      Caption         =   "文件"
      Index           =   1
      Begin VB.Menu 新建 
         Caption         =   "新建"
         Index           =   11
      End
      Begin VB.Menu 打开 
         Caption         =   "打开"
         Index           =   12
      End
   End
   Begin VB.Menu 设置 
      Caption         =   "设置"
      Index           =   2
      Begin VB.Menu 基本设置 
         Caption         =   "基本设置"
         Index           =   21
      End
   End
End
Attribute VB_Name = "Main"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Dim Setting As String
Dim SettingPath As String
Dim stg_path_array() As String
Public PythonPath As String
Public PY_GetData_Path As String
Dim SelStgIndex As Integer
Dim MainPath As String
Dim MainConfigPath As String
'####################################### 程序启动加载 ##############################################
Private Sub Form_Load()
    SelStgIndex = -1
    '读取配置文件
    SettingPath = "Setting\Setting.ini"
    Setting = CommonUsedMod.ReadUTF8File("Setting\Setting.ini")
    '加载参数
    PythonPath = CommonUsedMod.GetPar(Setting, "BASIC_CONFIG", "PythonPath")
    PY_GetData_Path = CommonUsedMod.GetPar(Setting, "BASIC_CONFIG", "PY_GetData_Path")
    MainPath = CommonUsedMod.GetPar(Setting, "BASIC_CONFIG", "MainPath")
    MainConfigPath = CommonUsedMod.GetPar(Setting, "BASIC_CONFIG", "MainConfigPath")
    '加载策略列表
    stg_num = CInt(CommonUsedMod.GetPar(Setting, "Stg_Config", "stg_num"))
    ReDim stg_path_array(stg_num)
    For i = 1 To stg_num
        TempStgPath = CommonUsedMod.GetPar(Setting, "stg_" + CStr(i), "path")
        stg_path_array(i - 1) = TempStgPath
        TempStgName = CommonUsedMod.GetFileName(TempStgPath)
        TempStgFolder = CommonUsedMod.GetFolder(TempStgPath)
        List1.AddItem (TempStgName)
    Next
End Sub
'####################################### 策略列表-双击 ##############################################
Private Sub List1_DblClick()
    TempIndex = List1.ListIndex
    SelStgIndex = TempIndex
    TempStgPath = stg_path_array(TempIndex)
    '加载策略参数
    Call LoadStgPar(TempStgPath)
    '加载策略回测记录
    Call LoadStgBackTestRec(TempStgPath)
    '加载策略回测参数
    Call LoadStgBackTestPar(TempStgPath)
End Sub
'####################################### 加载策略参数 ##############################################
Sub LoadStgPar(TempStgPath)
    TempStgConfig = Replace(TempStgPath, ".py", ".ini")
    If Dir(TempStgConfig) = "" Then
        FileCopy App.Path + "\..\Setting\StgConfigSample.ini", TempStgConfig
    End If
    TempStgConfig = CommonUsedMod.ReadUTF8File(TempStgConfig)
    '加载订阅代码
    List2.Clear
    TempCodeList = CommonUsedMod.GetPar(TempStgConfig, "QuoteDataConfig", "CodeList")
    TempCodeListArray = Split(TempCodeList, ",")
    For i = 0 To UBound(TempCodeListArray)
        If TempCodeListArray(i) <> "" Then List2.AddItem (TempCodeListArray(i))
    Next
    '加载订阅字段
    List3.Clear
    TempItem = CommonUsedMod.GetPar(TempStgConfig, "QuoteDataConfig", "Item")
    TempItemArray = Split(TempItem, ",")
    For i = 0 To UBound(TempItemArray)
        If TempItemArray(i) <> "" Then List3.AddItem (TempItemArray(i))
    Next
    '加载账户列表
    List4.Clear
    TempAccNum = CInt(CommonUsedMod.GetPar(TempStgConfig, "AccountConfig", "AccountNum"))
    For i = 0 To TempAccNum - 1
        TempAcc = CommonUsedMod.GetPar(TempStgConfig, "AccountConfig", "Account" + CStr(i + 1))
        List4.AddItem (TempAcc)
    Next
    '加载行情类型
    SComboBox2.AddItem ("TrdMin")
    SComboBox2.AddItem ("Tick")
    TempQuoteType = CommonUsedMod.GetPar(TempStgConfig, "QuoteDataConfig", "Type")
    SComboBox2.Text = TempQuoteType
    '加载行情频率
    SComboBox3.AddItem ("1Day")
    SComboBox3.AddItem ("1Min")
    SComboBox3.AddItem ("5Min")
    SComboBox3.AddItem ("15Min")
    SComboBox3.AddItem ("30Min")
    SComboBox3.AddItem ("60Min")
    TempQuoteTimeInterval = CommonUsedMod.GetPar(TempStgConfig, "QuoteDataConfig", "TimeInterval")
    SComboBox3.Text = TempQuoteTimeInterval
End Sub
'####################################### 加载策略回测记录 ##############################################
Sub LoadStgBackTestRec(TempStgPath)
    List5.Clear
    TempStgBackTestRecFolder = Replace(TempStgPath, ".py", "_BackTestResult")
    TempStgBackTestRec = Dir(TempStgBackTestRecFolder + "\", vbDirectory)
    Do While TempStgBackTestRec <> ""
        If TempStgBackTestRec <> "." And TempStgBackTestRec <> ".." Then
            List5.AddItem (TempStgBackTestRecFolder + "\" + TempStgBackTestRec)
        End If
        TempStgBackTestRec = Dir
    Loop
End Sub
'####################################### 加载策略回测参数 ##############################################
Sub LoadStgBackTestPar(TempStgPath)
    TempStgConfig = Replace(TempStgPath, ".py", ".ini")
    If Dir(TempStgConfig) = "" Then
        FileCopy App.Path + "\..\Setting\StgConfigSample.ini", TempStgConfig
    End If
    TempStgConfig = CommonUsedMod.ReadUTF8File(TempStgConfig)
    '加载策略开始时间
    TempStartTime = CommonUsedMod.GetPar(TempStgConfig, "MatchConfig", "StartTime")
    N_TextBox1.Text = TempStartTime
    '加载策略结束时间
    TempEndTime = CommonUsedMod.GetPar(TempStgConfig, "MatchConfig", "EndTime")
    N_TextBox2.Text = TempEndTime
    '加载策略初始资金
    TempInitCash = CommonUsedMod.GetPar(TempStgConfig, "MatchConfig", "InitCash")
    N_TextBox3.Text = TempInitCash
    '加载策略交易成本
    TempCostRatio = CommonUsedMod.GetPar(TempStgConfig, "MatchConfig", "CostRatio")
    N_TextBox4.Text = TempCostRatio
    '加载策略交易滑点
    TempSlippage = CommonUsedMod.GetPar(TempStgConfig, "MatchConfig", "Slippage")
    N_TextBox5.Text = TempSlippage
    '加载策略市场参与度
    TempMarketPartcipation = CommonUsedMod.GetPar(TempStgConfig, "MatchConfig", "MarketPartcipation")
    N_TextBox6.Text = TempMarketPartcipation
End Sub
'####################################### 新建策略 ##############################################
Private Sub N_Shape1_Click()
Mark1:
    TempName = InputBox("输入策略名称:", "新建策略", "StgSample")
    If TempName = "" Then Exit Sub
    StgPath = CommonUsedMod.GetPar(Setting, "BASIC_CONFIG", "StgPath")
    If Dir(StgPath + "\" + TempName + ".py") <> "" Then
        MsgBox "策略无效或已存在，请重新输入!", vbOKOnly + vbExclamation, "新建策略"
        GoTo Mark1:
    Else
        FileCopy App.Path + "\..\Setting\StgSample.py", StgPath + "\" + TempName + ".py"
        FileCopy App.Path + "\..\Setting\StgConfigSample.ini", StgPath + "\" + TempName + ".ini"
        List1.AddItem (TempName)
        stg_path_array = CommonUsedMod.ArrInsert(stg_path_array, UBound(stg_path_array), StgPath + "\" + TempName + ".py")
        List1.Selected(List1.ListCount - 1) = True
        Call List1_DblClick
        Call N_Shape2_Click
    End If
    Call SaveStgList
End Sub

'####################################### 编辑策略 ##############################################
Private Sub N_Shape2_Click()
    FileEditorPath = CommonUsedMod.GetPar(Setting, "BASIC_CONFIG", "FileEditorPath")
    If List1.ListIndex = -1 Then
        MsgBox "请先选择策略!", vbExclamation, "编辑策略"
    Else
        Call CommonUsedMod.Cmd(FileEditorPath + " " + stg_path_array(List1.ListIndex))
    End If
End Sub
'####################################### 删除策略 ##############################################
Private Sub N_Shape3_Click()
    If List1.ListIndex = -1 Then MsgBox "请先选择策略!", vbExclamation, "删除策略": Exit Sub
    TempRet = MsgBox("是 : 删除策略文件及回测记录" + vbNewLine + "否 : 仅删除列表记录", vbYesNoCancel + vbInformation, "删除策略")
    Select Case TempRet
    Case vbYes
        On Error Resume Next
        Kill stg_path_array(List1.ListIndex)
        Kill Replace(stg_path_array(List1.ListIndex), ".py", ".ini")
        Call CommonUsedMod.DelFolder(Replace(stg_path_array(List1.ListIndex), ".py", "_BackTestResult"))
        stg_path_array = CommonUsedMod.ArrDel(stg_path_array, List1.ListIndex)
        List1.RemoveItem (List1.ListIndex)
    Case vbNo
        stg_path_array = CommonUsedMod.ArrDel(stg_path_array, List1.ListIndex)
        List1.RemoveItem (List1.ListIndex)
    Case Else
    End Select
    Call SaveStgList
End Sub
'####################################### 保存StgList ##############################################
Sub SaveStgList()
    TempNum = CInt(CommonUsedMod.GetPar(Setting, "Stg_Config", "stg_num"))
    For i = 1 To TempNum
        Setting = CommonUsedMod.DelPar(Setting, "stg_" + CStr(i), SettingPath)
    Next
    Setting = CommonUsedMod.SavePar(Setting, "Stg_Config", "stg_num", CStr(List1.ListCount), SettingPath)
    For i = 0 To List1.ListCount - 1
        Setting = CommonUsedMod.SavePar(Setting, "stg_" + CStr(i + 1), "path", stg_path_array(i), SettingPath)
    Next
End Sub
'####################################### 修改订阅标的 ##############################################
Private Sub List2_Click()
    CodeSelect.Show 1, Me
    'CodeSelect.Show
End Sub
Private Sub N_Shape5_Click()
    If SelStgIndex <> -1 Then CodeSelect.Show 1, Me
End Sub
'####################################### 保存策略参数 ##############################################
Private Sub N_Shape8_Click()
    If SelStgIndex = -1 Then Exit Sub
    TempStgPath = stg_path_array(SelStgIndex)
    TempStgConfigPath = Replace(TempStgPath, ".py", ".ini")
    If Dir(TempStgConfigPath) = "" Then
        FileCopy App.Path + "\..\Setting\StgConfigSample.ini", TempStgConfigPath
    End If
    TempStgConfig = CommonUsedMod.ReadUTF8File(TempStgConfigPath)
    '保存订阅代码
    TempStr = ""
    For i = 0 To List2.ListCount - 1
        TempStr = TempStr + List2.List(i) + ","
    Next
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "QuoteDataConfig", "CodeList", TempStr, TempStgConfigPath)
    '保存订阅字段
    TempStr = ""
    For i = 0 To List3.ListCount - 1
        TempStr = TempStr + List3.List(i) + ","
    Next
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "QuoteDataConfig", "Item", TempStr, TempStgConfigPath)
    '保存账户列表
    TempStr = ""
    For i = 0 To List4.ListCount - 1
        TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "AccountConfig", "Account" + CStr(i + 1), List4.List(i), TempStgConfigPath)
    Next
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "AccountConfig", "AccountNum", List4.ListCount, TempStgConfigPath)
    '保存行情类型
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "QuoteDataConfig", "Type", SComboBox2.Text, TempStgConfigPath)
    '保存行情频率
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "QuoteDataConfig", "TimeInterval", SComboBox3.Text, TempStgConfigPath)
End Sub
'####################################### 保存回测参数 ##############################################
Private Sub N_Shape9_Click()
    If SelStgIndex = -1 Then Exit Sub
    TempStgPath = stg_path_array(SelStgIndex)
    TempStgConfigPath = Replace(TempStgPath, ".py", ".ini")
    If Dir(TempStgConfigPath) = "" Then
        FileCopy App.Path + "\..\Setting\StgConfigSample.ini", TempStgConfigPath
    End If
    TempStgConfig = CommonUsedMod.ReadUTF8File(TempStgConfigPath)
    '保存策略开始时间
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "MatchConfig", "StartTime", N_TextBox1.Text, TempStgConfigPath)
    '保存策略结束时间
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "MatchConfig", "EndTime", N_TextBox2.Text, TempStgConfigPath)
    '保存策略初始资金
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "MatchConfig", "InitCash", N_TextBox3.Text, TempStgConfigPath)
    '保存策略交易成本
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "MatchConfig", "CostRatio", N_TextBox4.Text, TempStgConfigPath)
    '保存策略交易滑点
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "MatchConfig", "Slippage", N_TextBox5.Text, TempStgConfigPath)
    '保存策略市场参与度
    TempStgConfig = CommonUsedMod.SavePar(TempStgConfig, "MatchConfig", "MarketPartcipation", N_TextBox6.Text, TempStgConfigPath)
End Sub
'####################################### 开始回测按钮 ##############################################
Private Sub N_Shape4_Click()
    If SelStgIndex = -1 Then Exit Sub
    Call N_Shape8_Click
    Call N_Shape9_Click
    TempStgPath = stg_path_array(SelStgIndex)
    '配置策略路径参数
    TempFile = CommonUsedMod.GetFileName(TempStgPath)
    TempFile = Replace(TempFile, ".py", "")
    TempFile = Replace(TempFile, ".Py", "")
    TempFile = Replace(TempFile, ".PY", "")
    TempFolder = CommonUsedMod.GetFolder(TempStgPath)
    TempMainSetting = CommonUsedMod.ReadUTF8File(MainConfigPath)
    TempMainSetting = CommonUsedMod.SavePar(TempMainSetting, "StgConfig", "StrategyName", TempFile, MainConfigPath)
    TempMainSetting = CommonUsedMod.SavePar(TempMainSetting, "StgConfig", "StrategyFolder", TempFolder, MainConfigPath)
    '开始回测
    'Call CommonUsedMod.PyEx(PythonPath, MainPath, "")
    Call CommonUsedMod.Cmd(PythonPath + " " + MainPath)

End Sub
