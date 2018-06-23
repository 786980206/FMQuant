VERSION 5.00
Begin VB.UserControl N_Cover 
   BackColor       =   &H00FFFFFF&
   ClientHeight    =   4950
   ClientLeft      =   0
   ClientTop       =   0
   ClientWidth     =   2700
   ScaleHeight     =   330
   ScaleMode       =   3  'Pixel
   ScaleWidth      =   180
   Begin VB.PictureBox Image_Capa 
      Appearance      =   0  'Flat
      BackColor       =   &H00FFFFFF&
      BorderStyle     =   0  'None
      Enabled         =   0   'False
      ForeColor       =   &H80000008&
      Height          =   3375
      Left            =   120
      ScaleHeight     =   225
      ScaleMode       =   3  'Pixel
      ScaleWidth      =   161
      TabIndex        =   8
      TabStop         =   0   'False
      Top             =   0
      Width           =   2415
   End
   Begin VB.Timer Timer1 
      Enabled         =   0   'False
      Interval        =   1
      Left            =   1680
      Top             =   0
   End
   Begin VB.Image Image_Assistir 
      Height          =   225
      Left            =   2280
      Picture         =   "N_Cover.ctx":0000
      Top             =   4560
      Width           =   225
   End
   Begin VB.Image Image_Star 
      Height          =   150
      Index           =   4
      Left            =   960
      Picture         =   "N_Cover.ctx":0209
      Top             =   4740
      Width           =   150
   End
   Begin VB.Image Image_Star 
      Height          =   150
      Index           =   3
      Left            =   720
      Picture         =   "N_Cover.ctx":038B
      Top             =   4740
      Width           =   150
   End
   Begin VB.Image Image_Star 
      Height          =   150
      Index           =   2
      Left            =   480
      Picture         =   "N_Cover.ctx":050D
      Top             =   4740
      Width           =   150
   End
   Begin VB.Image Image_Star 
      Height          =   150
      Index           =   1
      Left            =   240
      Picture         =   "N_Cover.ctx":068F
      Top             =   4740
      Width           =   150
   End
   Begin VB.Image Image_Star 
      Height          =   150
      Index           =   0
      Left            =   0
      Picture         =   "N_Cover.ctx":0811
      Top             =   4740
      Width           =   150
   End
   Begin VB.Shape Shape_Contorno 
      BorderColor     =   &H00E0E0E0&
      Height          =   615
      Left            =   0
      Top             =   0
      Width           =   2535
   End
   Begin VB.Label Label_Titulo 
      BackColor       =   &H00000000&
      BackStyle       =   0  'Transparent
      Caption         =   "Titulo1"
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   9.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00000000&
      Height          =   240
      Left            =   0
      TabIndex        =   7
      Top             =   3480
      Width           =   780
   End
   Begin VB.Label Label_Visitas 
      BackColor       =   &H00FF80FF&
      Caption         =   "Visitas1"
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   6.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00000000&
      Height          =   180
      Left            =   960
      TabIndex        =   6
      Top             =   4440
      Visible         =   0   'False
      Width           =   765
   End
   Begin VB.Label Label_Id_Filme 
      BackColor       =   &H00FF80FF&
      Caption         =   "Id_Filme1"
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   6.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00000000&
      Height          =   180
      Left            =   0
      TabIndex        =   5
      Top             =   3960
      Visible         =   0   'False
      Width           =   765
   End
   Begin VB.Label Label_Capa 
      BackColor       =   &H00FF80FF&
      Caption         =   "Capa1"
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   6.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00000000&
      Height          =   180
      Left            =   960
      TabIndex        =   4
      Top             =   4200
      Visible         =   0   'False
      Width           =   765
   End
   Begin VB.Label Label_Ano 
      BackColor       =   &H00FF80FF&
      Caption         =   "Ano1"
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   6.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00000000&
      Height          =   180
      Left            =   960
      TabIndex        =   3
      Top             =   3960
      Visible         =   0   'False
      Width           =   765
   End
   Begin VB.Label Label_Sinopse 
      BackColor       =   &H00FF80FF&
      Caption         =   "Sinopse1"
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   6.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00000000&
      Height          =   180
      Left            =   0
      TabIndex        =   2
      Top             =   4440
      Visible         =   0   'False
      Width           =   765
   End
   Begin VB.Label Label_Url 
      BackColor       =   &H00FF80FF&
      Caption         =   "Url1"
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   6.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00000000&
      Height          =   180
      Left            =   0
      TabIndex        =   1
      Top             =   4200
      Visible         =   0   'False
      Width           =   765
   End
   Begin VB.Label Label_Categoria 
      BackColor       =   &H00EFF1F2&
      BackStyle       =   0  'Transparent
      Caption         =   "Categoria"
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   6.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00808080&
      Height          =   180
      Left            =   0
      TabIndex        =   0
      Top             =   3720
      Width           =   735
   End
End
Attribute VB_Name = "N_Cover"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'Component: N_Selection
'Copyright (c) 2013 Nikyts software - Informatic and thecnologies
'Developed by Nelson do Carmo
'Contact: nikyts@hotmail.com
'Web: www.nikyts.net
'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'Declaração de variáveis
Private Const LOGPIXELSY = 90
Private Const LF_FACESIZE = 32
Private Const DT_BOTTOM = &H8
Private Const DT_CENTER = &H1
Private Const DT_LEFT = &H0
Private Const DT_RIGHT = &H2
Private Const DT_TOP = &H0
Private Const DT_VCENTER = &H4
Private Const DT_SINGLELINE = &H20
Private Const DT_WORDBREAK = &H10
Private Const DT_CALCRECT = &H400
Private Const DT_END_ELLIPSIS = &H8000
Private Const DT_MODIFYSTRING = &H10000
Private Const DT_WORD_ELLIPSIS = &H40000

'Cores
Private Const COLOR_BTNHIGHLIGHT = 20
Private Const COLOR_BTNSHADOW = 16
Private Const COLOR_BTNFACE = 15
Private Const COLOR_HIGHLIGHT = 13
Private Const COLOR_ACTIVEBORDER = 10
Private Const COLOR_WINDOWFRAME = 6
Private Const COLOR_3DDKSHADOW = 21
Private Const COLOR_3DLIGHT = 22
Private Const COLOR_INFOTEXT = 23
Private Const COLOR_INFOBK = 24
Private Const PATCOPY = &HF00021
Private Const SRCCOPY = &HCC0020
Private Const PS_SOLID = 0
Private Const PS_DASHDOT = 3
Private Const PS_DASHDOTDOT = 4
Private Const PS_DOT = 2
Private Const PS_DASH = 1
Private Const PS_ENDCAP_FLAT = &H200

Private Type RECT
        Left As Long
        Top As Long
        Right As Long
        Bottom As Long
End Type

'Api's utilizadas pelo componente
Private Declare Function WindowFromPoint Lib "User32" (ByVal xPoint As Long, ByVal yPoint As Long) As Long
Private Declare Function GetCursorPos Lib "User32" (lpPoint As POINTAPI) As Long
Private Type POINTAPI
        x As Long
        y As Long
End Type
Private Declare Function SelectClipRgn Lib "gdi32" (ByVal hDC As Long, ByVal hRgn As Long) As Long
Private Declare Function SelectClipPath Lib "gdi32" (ByVal hDC As Long, ByVal iMode As Long) As Long
Private Declare Function CreateRectRgn Lib "gdi32" (ByVal x1 As Long, ByVal y1 As Long, ByVal x2 As Long, ByVal y2 As Long) As Long
Private Declare Function ReleaseDC Lib "User32" (ByVal hWnd As Long, ByVal hDC As Long) As Long
Private Declare Function GetDeviceCaps Lib "gdi32" (ByVal hDC As Long, ByVal nIndex As Long) As Long
Private Declare Function ClientToScreen Lib "User32" (ByVal hWnd As Long, lpPoint As POINTAPI) As Long
Private Declare Function SetCapture Lib "User32" (ByVal hWnd As Long) As Long
Private Declare Function GetCapture Lib "User32" () As Long
Private Declare Function ReleaseCapture Lib "User32" () As Long
'Private Declare Function WindowFromPoint Lib "user32" (ByVal xPoint As Long, ByVal yPoint As Long) As Long ' api repetida
Private Declare Function GetSysColor Lib "User32" (ByVal nIndex As Long) As Long
Private Declare Function LineTo Lib "gdi32" (ByVal hDC As Long, ByVal x As Long, ByVal y As Long) As Long
Private Declare Function SetBkColor Lib "gdi32" (ByVal hDC As Long, ByVal crColor As Long) As Long
Private Declare Function SetBkMode Lib "gdi32" (ByVal hDC As Long, ByVal nBkMode As Long) As Long
Private Declare Function SetTextColor Lib "gdi32" (ByVal hDC As Long, ByVal crColor As Long) As Long
Private Declare Function SelectObject Lib "gdi32" (ByVal hDC As Long, ByVal hObject As Long) As Long
Private Declare Function CreatePen Lib "gdi32" (ByVal nPenStyle As Long, ByVal nWidth As Long, ByVal crColor As Long) As Long
Private Declare Function GetClientRect Lib "User32" (ByVal hWnd As Long, lpRect As RECT) As Long
Private Declare Function MoveToEx Lib "gdi32" (ByVal hDC As Long, ByVal x As Long, ByVal y As Long, lpPoint As Long) As Long
Private Declare Function DeleteObject Lib "gdi32" (ByVal hObject As Long) As Long
Private Declare Function InflateRect Lib "User32" (lpRect As RECT, ByVal x As Long, ByVal y As Long) As Long
Private Declare Function DrawFocusRect Lib "User32" (ByVal hDC As Long, lpRect As RECT) As Long
Private Declare Function CreateCompatibleBitmap Lib "gdi32" (ByVal hDC As Long, ByVal nWidth As Long, ByVal nHeight As Long) As Long
Private Declare Function CreateCompatibleDC Lib "gdi32" (ByVal hDC As Long) As Long
Private Declare Function BitBlt Lib "gdi32" (ByVal hDestDC As Long, ByVal x As Long, ByVal y As Long, ByVal nWidth As Long, ByVal nHeight As Long, ByVal hSrcDC As Long, ByVal xSrc As Long, ByVal ySrc As Long, ByVal dwRop As Long) As Long
Private Declare Function PatBlt Lib "gdi32" (ByVal hDC As Long, ByVal x As Long, ByVal y As Long, ByVal nWidth As Long, ByVal nHeight As Long, ByVal dwRop As Long) As Long
Private Declare Function CreateSolidBrush Lib "gdi32" (ByVal crColor As Long) As Long
Private Declare Function GetDesktopWindow Lib "User32" () As Long
Private Declare Function GetDC Lib "User32" (ByVal hWnd As Long) As Long
Private Declare Function OffsetRect Lib "User32" (lpRect As RECT, ByVal x As Long, ByVal y As Long) As Long

Dim m_MouseInside As Boolean

'Animar o botao/cor da shape
Dim isOver As Boolean
Dim m_State As Integer
Event Click()
Event DblClick()
Event MouseMove(Button As Integer, Shift As Integer, x As Single, y As Single)
Event MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
Event MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
Event MouseEnter()
Event MouseLeave()
Public Event MouseOver()
Public Event MouseOut()
Public Event Resize()

'Eventos para as teclas
Public Event KeyPress(KeyAscii As Integer)
Public Event KeyDown(KeyCode As Integer, Shift As Integer)
Public Event KeyUp(KeyCode As Integer, Shift As Integer)

'Cores utilizadas pelos eventos do botao
Dim cor_contorno_normal As OLE_COLOR
Dim cor_contorno_hover As OLE_COLOR
Dim cor_contorno_down As OLE_COLOR

Dim cor_letra_normal As OLE_COLOR
Dim cor_letra_hover As OLE_COLOR
Dim cor_letra_down As OLE_COLOR

Dim cor_letra_normal_2 As OLE_COLOR
Dim cor_letra_hover_2 As OLE_COLOR
Dim cor_letra_down_2 As OLE_COLOR

Dim m_Picture As StdPicture

Public Event Assistir(ByVal assistir_filme As Boolean)

Private Sub Image_Assistir_MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Indicar que é para fechar o tab ao clicar na cruz
    RaiseEvent MouseDown(Button, Shift, x, y)
    If Button = 1 Then
        RaiseEvent Assistir(True)
    End If
End Sub

Public Property Get Picture() As StdPicture
    Set Picture = m_Picture
End Property

Public Property Set Picture(m_New_Picture As StdPicture)
    On Error Resume Next
    Set m_Picture = m_New_Picture
    PropertyChanged "Picture"
    Set Image_Capa.Picture = m_New_Picture
End Property

Private Sub Label_Titulo_Click()
    'Atalho para
    UserControl_Click
End Sub

Private Sub Label_Titulo_DblClick()
    'Atalho para
    UserControl_DblClick
End Sub

Private Sub Label_Titulo_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mousedown
    RaiseEvent MouseDown(Button, Shift, x, y)
    If Button = 1 Then
        m_State = 2
        Call DrawState
    End If
End Sub

Private Sub Label_Titulo_MouseMove(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mousemove
    RaiseEvent MouseMove(Button, Shift, x, y)
    If Button < 2 Then
        If Not CheckMouseOver Then
            isOver = False
            m_State = 0
            Call DrawState
        Else
            If Button = 0 And Not isOver Then
                Timer1.Enabled = True
                isOver = True
                RaiseEvent MouseEnter
                m_State = 1
                Call DrawState
            ElseIf Button = 1 Then
                isOver = True
                m_State = 2
                Call DrawState
                isOver = False
            End If
        End If
    End If
    
    Label_Titulo.ToolTipText = Label_Titulo.Caption
End Sub

Private Sub Label_Titulo_MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mouseup
    RaiseEvent MouseUp(Button, Shift, x, y)
    If CheckMouseOver Then
        m_State = 1
    Else
        m_State = 0
    End If
    
    RaiseEvent Click
    Call DrawState
End Sub

Private Sub UserControl_AccessKeyPress(KeyAscii As Integer)
    'Evento keypress
    LastButton = 1
    Call UserControl_Click
End Sub

Private Sub UserControl_Click()
    'Evento click
    'RaiseEvent Click
End Sub

Private Sub UserControl_DblClick()
    'Evento duploclick
    RaiseEvent DblClick
End Sub

Public Property Get Titulo() As String
    'Escolher o nome do botão
    Titulo = Label_Titulo.Caption
End Property

Public Property Let Titulo(New_Value As String)
    'Alterar o caption para o novo texto
    Label_Titulo.Caption = New_Value
    PropertyChanged "Titulo"
End Property

Public Property Get Id_Filme() As String
    'Escolher o descrição do botão
    Id_Filme = Label_Id_Filme.Caption
End Property

Public Property Let Id_Filme(New_Value As String)
    'Alterar o descrição para o novo texto
    Label_Id_Filme.Caption = New_Value
    PropertyChanged "Id_Filme"
End Property

Public Property Get Url() As String
    'Escolher o descrição do botão
    Url = Label_Url.Caption
End Property

Public Property Let Url(New_Value As String)
    'Alterar o descrição para o novo texto
    Label_Url.Caption = New_Value
    PropertyChanged "Url"
End Property

Public Property Get Sinopse() As String
    'Escolher o descrição do botão
    Sinopse = Label_Sinopse.Caption
End Property

Public Property Let Sinopse(New_Value As String)
    'Alterar o descrição para o novo texto
    Label_Sinopse.Caption = New_Value
    PropertyChanged "Sinopse"
End Property

Public Property Get Ano() As String
    'Escolher o descrição do botão
    Ano = Label_Ano.Caption
End Property

Public Property Let Ano(New_Value As String)
    'Alterar o descrição para o novo texto
    Label_Ano.Caption = New_Value
    PropertyChanged "Ano"
End Property

Public Property Get Capa() As String
    'Escolher o descrição do botão
    Capa = Label_Capa.Caption
End Property

Public Property Let Capa(New_Value As String)
    'Alterar o descrição para o novo texto
    Label_Capa.Caption = New_Value
    PropertyChanged "Capa"
End Property

Public Property Get Visitas() As String
    'Escolher o descrição do botão
    Visitas = Label_Visitas.Caption
End Property

Public Property Let Visitas(New_Value As String)
    'Alterar o descrição para o novo texto
    Label_Visitas.Caption = New_Value
    PropertyChanged "Visitas"
End Property

Public Property Get Categoria() As String
    'Escolher o descrição do botão
    Categoria = Label_Categoria.Caption
End Property

Public Property Let Categoria(New_Value As String)
    'Alterar o descrição para o novo texto
    Label_Categoria.Caption = New_Value
    PropertyChanged "Categoria"
End Property

Private Sub UserControl_Initialize()
    Ajustar_Botao
End Sub

Private Sub UserControl_InitProperties()
    'Ler as propriedades do botão
    On Error GoTo Corrige_UserControl_InitProperties
    Titulo = UserControl.Extender.Name
    Id_Filme = "Id_Filme"
    Url = "Url"
    Sinopse = "Sinopse"
    Ano = "Ano"
    Capa = "Capa"
    Visitas = "Visitas"
    Categoria = "Categoria"
    Enabled = True
    BorderColorNormal = RGB(255, 255, 255)
    BorderColorHover = &HFFCB35 'Azul
    BorderColorDown = &HFFCB35 'Azul
    FontSize = 8
    FontBold = False
    Font = "Verdana" '"MS Sans Serif"
    ForeColorNormal = &HFFCB35 'Azul
    ForeColorHover = RGB(255, 255, 255)
    ForeColorDown = RGB(255, 255, 255)
    ForeColorNormal_2 = RGB(0, 0, 0)
    ForeColorHover_2 = RGB(255, 255, 255)
    ForeColorDown_2 = RGB(255, 255, 255)
    Call Ajustar_Botao
    
Corrige_UserControl_InitProperties:
End Sub

Private Sub UserControl_KeyDown(KeyCode As Integer, Shift As Integer)
    'Evento keydown, atalho para as teclas
    Select Case KeyCode
        Case vbKeyRight, vbKeyDown
            Call SendKeys("{TAB}")
            Case vbKeyLeft, vbKeyUp
            Call SendKeys("+{TAB}")
        
        Case vbKeyReturn
            UserControl_Click
    End Select
    RaiseEvent KeyDown(KeyCode, Shift)
End Sub

Private Sub UserControl_KeyPress(KeyAscii As Integer)
    'Evento keypress
    RaiseEvent KeyPress(KeyAscii)
End Sub

Private Sub UserControl_KeyUp(KeyCode As Integer, Shift As Integer)
    'Evento keyup
    RaiseEvent KeyUp(KeyCode, Shift)
    UserControl.Refresh
End Sub

Private Sub UserControl_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mousedown
    RaiseEvent MouseDown(Button, Shift, x, y)
    If Button = 1 Then
        m_State = 2
        Call DrawState
    End If
End Sub

Private Sub UserControl_MouseMove(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mousemove
    RaiseEvent MouseMove(Button, Shift, x, y)
    If Button < 2 Then
        If Not CheckMouseOver Then
            isOver = False
            m_State = 0
            Call DrawState
        Else
            If Button = 0 And Not isOver Then
                Timer1.Enabled = True
                isOver = True
                RaiseEvent MouseEnter
                m_State = 1
                Call DrawState
            ElseIf Button = 1 Then
                isOver = True
                m_State = 2
                Call DrawState
                isOver = False
            End If
        End If
    End If
End Sub

Private Sub UserControl_MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mouseup
    RaiseEvent MouseUp(Button, Shift, x, y)
    
    If CheckMouseOver Then
        m_State = 1
    Else
        m_State = 0
    End If
    
    RaiseEvent Click
    Call DrawState
End Sub

Private Function CheckMouseOver() As Boolean
    'Efectuar o over do botao
    Dim PT As POINTAPI
    GetCursorPos PT
    CheckMouseOver = (WindowFromPoint(PT.x, PT.y) = UserControl.hWnd)
End Function

Private Sub DrawState()
    On Error Resume Next
    If m_State = 1 Then 'mouse hover
        Shape_Contorno.BorderColor = cor_contorno_hover
    
    ElseIf m_State = 2 Then 'mouse down
        Shape_Contorno.BorderColor = cor_contorno_down
        
    Else 'normal
        Shape_Contorno.BorderColor = cor_contorno_normal
    End If
End Sub

Private Sub Timer1_Timer()
    'Animar o botão
    If Not CheckMouseOver Then
        Timer1.Enabled = False
        isOver = False
        RaiseEvent MouseLeave
        m_State = 0
        Call DrawState
    End If
End Sub

Public Property Get FontSize() As Integer
    'Escolher o tamanho da letra
    FontSize = Label_Titulo.FontSize
End Property

Public Property Let FontSize(New_Value As Integer)
    'Alterar o tamanho da letra
    Label_Titulo.FontSize = New_Value
    PropertyChanged "FontSize"
End Property

Public Property Get FontBold() As Boolean
    'Indicar se que ou não a letra em negrito
    FontBold = Label_Titulo.FontBold
End Property

Public Property Let FontBold(New_Value As Boolean)
    'Alterar a letra para negrito se for o caso
    Label_Titulo.FontBold = New_Value
    PropertyChanged "FontBold"
End Property

Public Property Get Enabled() As Boolean
    'Escolher se o botão fica activo ou não
    Enabled = UserControl.Enabled
End Property

Public Property Let Enabled(New_Value As Boolean)
    'Verificar se o botão fica activo ou não
    UserControl.Enabled = New_Value
    PropertyChanged "Enabled"
End Property

Private Sub UserControl_ReadProperties(PropBag As PropertyBag)
    'Ler as propriedades do control
    On Error GoTo Corrige_UserControl_ReadProperties
    With PropBag
        Titulo = .ReadProperty("Titulo", "Titulo1")
        Id_Filme = .ReadProperty("Id_Filme", "Id_Filme")
        Url = .ReadProperty("Url", "Url")
        Sinopse = .ReadProperty("Sinopse", "Sinopse")
        Ano = .ReadProperty("Ano", "Ano")
        Capa = .ReadProperty("Capa", "Capa")
        Visitas = .ReadProperty("Visitas", "Visitas")
        Categoria = .ReadProperty("Categoria", "Categoria")
        BorderColorNormal = .ReadProperty("BorderColorNormal", "&H00000000&")
        BorderColorHover = .ReadProperty("BorderColorHover", "&H002D2D2D&")
        BorderColorDown = .ReadProperty("BorderColorDown", "&H80FFFF")
        FontSize = .ReadProperty("FontSize", "8")
        FontBold = .ReadProperty("FontBold", "False")
        Font = .ReadProperty("Font", "MS Sans Serif")
        Enabled = .ReadProperty("Enabled", "True")
        ForeColorNormal = .ReadProperty("ForeColorNormal", "&H00000000&")
        ForeColorHover = .ReadProperty("ForeColorHover", "&H00000000&")
        ForeColorDown = .ReadProperty("ForeColorDown", "&H00FFFFFF&")
        ForeColorNormal_2 = .ReadProperty("ForeColorNormal_2", "&H00000000&")
        ForeColorHover_2 = .ReadProperty("ForeColorHover_2", "&H00000000&")
        ForeColorDown_2 = .ReadProperty("ForeColorDown_2", "&H00FFFFFF&")
        Set m_Picture = .ReadProperty("Picture", Nothing)
    End With
    
Corrige_UserControl_ReadProperties:
End Sub

Private Sub UserControl_WriteProperties(PropBag As PropertyBag)
    'Escrever as propriedades do control
    On Error GoTo Corrige_UserControl_WriteProperties
    With PropBag
        Call .WriteProperty("Titulo", Titulo, "")
        Call .WriteProperty("Id_Filme", Id_Filme, "")
        Call .WriteProperty("Url", Url, "")
        Call .WriteProperty("Sinopse", Sinopse, "")
        Call .WriteProperty("Ano", Ano, "")
        Call .WriteProperty("Capa", Capa, "")
        Call .WriteProperty("Visitas", Visitas, "")
        Call .WriteProperty("Categoria", Categoria, "")
        Call .WriteProperty("BorderColorNormal", BorderColorNormal, "&H00000000&")
        Call .WriteProperty("BorderColorHover", BorderColorHover, "&H002D2D2D&")
        Call .WriteProperty("BorderColorDown", BorderColorDown, "&H80FFFF")
        Call .WriteProperty("FontSize", FontSize, "8")
        Call .WriteProperty("FontBold", FontBold, "False")
        Call .WriteProperty("Font", Font, "MS Sans Serif")
        Call .WriteProperty("Enabled", Enabled, "True")
        Call .WriteProperty("ForeColorNormal", ForeColorNormal, "&HFF8080")
        Call .WriteProperty("ForeColorHover", ForeColorHover, "&HFF8080")
        Call .WriteProperty("ForeColorDown", ForeColorDown, "&H00FFFFFF&")
        Call .WriteProperty("ForeColorNormal_2", ForeColorNormal_2, "&HFF8080")
        Call .WriteProperty("ForeColorHover_2", ForeColorHover_2, "&HFF8080")
        Call .WriteProperty("ForeColorDown_2", ForeColorDown_2, "&H00FFFFFF&")
        Call .WriteProperty("Picture", m_Picture, Nothing)
    End With
    
Corrige_UserControl_WriteProperties:
End Sub

Private Sub UserControl_Resize()
    'Desenhar o botão ajustando os controles do form
    RaiseEvent Resize
    Ajustar_Botao
End Sub

Public Property Get MouseInside() As Boolean
    'Mouse em cima do cntrol
    MouseInside = m_MouseInside
End Property

Public Sub Ajustar_Botao()
    'Actualizar o botão
    'On Error Resume Next
    With UserControl
        .Height = Screen.TwipsPerPixelY * (245 + 85)
        .Width = Screen.TwipsPerPixelX * (160 + 4)
    End With
    
    With Shape_Contorno
        .Top = 0
        .Height = UserControl.ScaleHeight
        .Left = 0
        .Width = UserControl.ScaleWidth
    End With
    
    With Image_Capa
        .Top = 2
        .Height = 245
        .Left = 2
        .Width = 160
    End With
    
    With Label_Titulo
        .Top = Image_Capa.Top + Image_Capa.Height + 10
        .Left = 10
        .Width = UserControl.ScaleWidth - 20
    End With
    
    With Label_Categoria
        .Top = Label_Titulo.Top + Label_Titulo.Height + 1
        .Left = Label_Titulo.Left
        .Width = Label_Titulo.Width
    End With
    
    Dim i As Integer: For i = 0 To Image_Star.Count - 1
        If i = 0 Then
            Image_Star(0).Top = UserControl.ScaleHeight - Image_Star(0).Height - 10
            Image_Star(0).Left = Label_Titulo.Left
        Else
            Image_Star(i).Top = Image_Star(0).Top
            Image_Star(i).Left = Image_Star(i - 1).Left + Image_Star(0).Width + 2
        End If
    Next
    
    With Image_Assistir
        .Top = Image_Star(0).Top
        .Left = UserControl.ScaleWidth - .Width - 10
    End With
End Sub

Public Property Get ForeColorNormal() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    ForeColorNormal = Label_Titulo.ForeColor
End Property

Public Property Let ForeColorNormal(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_letra_normal = New_Value
    Label_Titulo.ForeColor = New_Value
    PropertyChanged "ForeColorNormal"
End Property

Public Property Get ForeColorHover() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    ForeColorHover = cor_letra_hover
End Property

Public Property Let ForeColorHover(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_hover = New_Value
    'UserControl.backcolor  = new_Value
    PropertyChanged "ForeColorHover"
End Property

Public Property Get ForeColorDown() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    ForeColorDown = cor_letra_down
End Property

Public Property Let ForeColorDown(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_down = New_Value
    'UserControl.backcolor  = new_Value
    PropertyChanged "ForeColorDown"
End Property

Public Property Get BorderColorNormal() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    BorderColorNormal = Shape_Contorno.BackColor
End Property

Public Property Let BorderColorNormal(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_contorno_normal = New_Value
    Shape_Contorno.BackColor = New_Value
    PropertyChanged "BorderColorNormal"
End Property

Public Property Get BorderColorHover() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    BorderColorHover = cor_contorno_hover
End Property

Public Property Let BorderColorHover(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_contorno_hover = New_Value
    'UserControl.backcolor  = new_Value
    PropertyChanged "BorderColorHover"
End Property

Public Property Get BorderColorDown() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    BorderColorDown = cor_contorno_down
End Property

Public Property Let BorderColorDown(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_contorno_down = New_Value
    'UserControl.backcolor  = new_Value
    PropertyChanged "BorderColorDown"
End Property

Private Sub Label_Categoria_Click()
    'Atalho para
    UserControl_Click
End Sub

Private Sub Label_Categoria_DblClick()
    'Atalho para
    UserControl_DblClick
End Sub

Private Sub Label_Categoria_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mousedown
    RaiseEvent MouseDown(Button, Shift, x, y)
    If Button = 1 Then
        m_State = 2
        Call DrawState
    End If
End Sub

Private Sub Label_Categoria_MouseMove(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mousemove
    RaiseEvent MouseMove(Button, Shift, x, y)
    If Button < 2 Then
        If Not CheckMouseOver Then
            isOver = False
            m_State = 0
            Call DrawState
        Else
            If Button = 0 And Not isOver Then
                Timer1.Enabled = True
                isOver = True
                RaiseEvent MouseEnter
                m_State = 1
                Call DrawState
            ElseIf Button = 1 Then
                isOver = True
                m_State = 2
                Call DrawState
                isOver = False
            End If
        End If
    End If
    
    Label_Categoria.ToolTipText = Label_Categoria.Caption
End Sub

Private Sub Label_Categoria_MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mouseup
    RaiseEvent MouseUp(Button, Shift, x, y)
    If CheckMouseOver Then
        m_State = 1
    Else
        m_State = 0
    End If
    
    RaiseEvent Click
    Call DrawState
End Sub

Public Property Get ForeColorNormal_2() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    ForeColorNormal_2 = Label_Id_Filme.ForeColor
End Property

Public Property Let ForeColorNormal_2(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_letra_normal_2 = New_Value
    Label_Id_Filme.ForeColor = New_Value
    PropertyChanged "ForeColorNormal_2"
End Property

Public Property Get ForeColorHover_2() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    ForeColorHover_2 = cor_letra_hover_2
End Property

Public Property Let ForeColorHover_2(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_hover_2 = New_Value
    'UserControl.backcolor  = new_Value
    PropertyChanged "ForeColorHover_2"
End Property

Public Property Get ForeColorDown_2() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    ForeColorDown_2 = cor_letra_down_2
End Property

Public Property Let ForeColorDown_2(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_down_2 = New_Value
    'UserControl.backcolor  = new_Value
    PropertyChanged "ForeColorDown_2"
End Property



