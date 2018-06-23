VERSION 5.00
Begin VB.UserControl N_Selection 
   BackColor       =   &H00EFF1F2&
   ClientHeight    =   780
   ClientLeft      =   0
   ClientTop       =   0
   ClientWidth     =   2730
   ScaleHeight     =   52
   ScaleMode       =   3  'Pixel
   ScaleWidth      =   182
   Begin VB.Timer Timer1 
      Enabled         =   0   'False
      Interval        =   1
      Left            =   1680
      Top             =   0
   End
   Begin VB.Image Image1 
      Height          =   615
      Left            =   2160
      Picture         =   "N_Selection.ctx":0000
      Top             =   0
      Visible         =   0   'False
      Width           =   210
   End
   Begin VB.Label Label_Descricao 
      AutoSize        =   -1  'True
      BackColor       =   &H00EFF1F2&
      BackStyle       =   0  'Transparent
      Caption         =   "NDescricao1"
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
      Left            =   120
      TabIndex        =   1
      Top             =   360
      Width           =   990
   End
   Begin VB.Label Label1 
      AutoSize        =   -1  'True
      BackColor       =   &H00000000&
      BackStyle       =   0  'Transparent
      Caption         =   "NSelection1"
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
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   1170
   End
End
Attribute VB_Name = "N_Selection"
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
        left As Long
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
Private Declare Function SelectClipRgn Lib "gdi32" (ByVal hdc As Long, ByVal hRgn As Long) As Long
Private Declare Function SelectClipPath Lib "gdi32" (ByVal hdc As Long, ByVal iMode As Long) As Long
Private Declare Function CreateRectRgn Lib "gdi32" (ByVal X1 As Long, ByVal Y1 As Long, ByVal X2 As Long, ByVal Y2 As Long) As Long
Private Declare Function ReleaseDC Lib "User32" (ByVal hWnd As Long, ByVal hdc As Long) As Long
Private Declare Function GetDeviceCaps Lib "gdi32" (ByVal hdc As Long, ByVal nIndex As Long) As Long
Private Declare Function ClientToScreen Lib "User32" (ByVal hWnd As Long, lpPoint As POINTAPI) As Long
Private Declare Function SetCapture Lib "User32" (ByVal hWnd As Long) As Long
Private Declare Function GetCapture Lib "User32" () As Long
Private Declare Function ReleaseCapture Lib "User32" () As Long
'Private Declare Function WindowFromPoint Lib "user32" (ByVal xPoint As Long, ByVal yPoint As Long) As Long ' api repetida
Private Declare Function GetSysColor Lib "User32" (ByVal nIndex As Long) As Long
Private Declare Function LineTo Lib "gdi32" (ByVal hdc As Long, ByVal x As Long, ByVal y As Long) As Long
Private Declare Function SetBkColor Lib "gdi32" (ByVal hdc As Long, ByVal crColor As Long) As Long
Private Declare Function SetBkMode Lib "gdi32" (ByVal hdc As Long, ByVal nBkMode As Long) As Long
Private Declare Function SetTextColor Lib "gdi32" (ByVal hdc As Long, ByVal crColor As Long) As Long
Private Declare Function SelectObject Lib "gdi32" (ByVal hdc As Long, ByVal hObject As Long) As Long
Private Declare Function CreatePen Lib "gdi32" (ByVal nPenStyle As Long, ByVal nWidth As Long, ByVal crColor As Long) As Long
Private Declare Function GetClientRect Lib "User32" (ByVal hWnd As Long, lpRect As RECT) As Long
Private Declare Function MoveToEx Lib "gdi32" (ByVal hdc As Long, ByVal x As Long, ByVal y As Long, lpPoint As Long) As Long
Private Declare Function DeleteObject Lib "gdi32" (ByVal hObject As Long) As Long
Private Declare Function InflateRect Lib "User32" (lpRect As RECT, ByVal x As Long, ByVal y As Long) As Long
Private Declare Function DrawFocusRect Lib "User32" (ByVal hdc As Long, lpRect As RECT) As Long
Private Declare Function CreateCompatibleBitmap Lib "gdi32" (ByVal hdc As Long, ByVal nWidth As Long, ByVal nHeight As Long) As Long
Private Declare Function CreateCompatibleDC Lib "gdi32" (ByVal hdc As Long) As Long
Private Declare Function BitBlt Lib "gdi32" (ByVal hDestDC As Long, ByVal x As Long, ByVal y As Long, ByVal nWidth As Long, ByVal nHeight As Long, ByVal hSrcDC As Long, ByVal xSrc As Long, ByVal ySrc As Long, ByVal dwRop As Long) As Long
Private Declare Function PatBlt Lib "gdi32" (ByVal hdc As Long, ByVal x As Long, ByVal y As Long, ByVal nWidth As Long, ByVal nHeight As Long, ByVal dwRop As Long) As Long
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
Dim cor_fundo_normal As OLE_COLOR
Dim cor_fundo_hover As OLE_COLOR
Dim cor_fundo_down As OLE_COLOR

Dim cor_letra_normal As OLE_COLOR
Dim cor_letra_hover As OLE_COLOR
Dim cor_letra_down As OLE_COLOR

Dim cor_letra_normal_2 As OLE_COLOR
Dim cor_letra_hover_2 As OLE_COLOR
Dim cor_letra_down_2 As OLE_COLOR

Private Sub Label1_Click()
    'Atalho para
    UserControl_Click
End Sub

Private Sub Label1_DblClick()
    'Atalho para
    UserControl_DblClick
End Sub

Private Sub Label1_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mousedown
    RaiseEvent MouseDown(Button, Shift, x, y)
    If Button = 1 Then
        m_State = 2
        Call DrawState
    End If
End Sub

Private Sub Label1_MouseMove(Button As Integer, Shift As Integer, x As Single, y As Single)
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

Private Sub Label1_MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
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

Public Property Get Caption() As String
    'Escolher o nome do botão
    Caption = Label1.Caption
End Property

Public Property Let Caption(New_Value As String)
    'Alterar o caption para o novo texto
    Label1.Caption = New_Value
    PropertyChanged "Caption"
End Property

Public Property Get Description() As String
    'Escolher o descrição do botão
    Description = Label_Descricao.Caption
End Property

Public Property Let Description(New_Value As String)
    'Alterar o descrição para o novo texto
    Label_Descricao.Caption = New_Value
    PropertyChanged "Description"
End Property

Private Sub UserControl_InitProperties()
    'Ler as propriedades do botão
    On Error GoTo Corrige_UserControl_InitProperties
    Caption = UserControl.Extender.Name
    Description = "Descrição"
    Enabled = True
    BackColorNormal = RGB(0, 0, 0)
    BackColorHover = RGB(45, 45, 45)
    BackColorDown = RGB(255, 255, 255)
    FontSize = 8
    FontBold = False
    Font = "Verdana" '"MS Sans Serif"
    ForeColorNormal = RGB(255, 255, 255)
    ForeColorHover = RGB(255, 255, 255)
    ForeColorDown = RGB(0, 0, 0)
    ForeColorNormal_2 = RGB(255, 255, 255)
    ForeColorHover_2 = RGB(255, 255, 255)
    ForeColorDown_2 = RGB(0, 0, 0)
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
    Dim pt As POINTAPI
    GetCursorPos pt
    CheckMouseOver = (WindowFromPoint(pt.x, pt.y) = UserControl.hWnd)
End Function

Private Sub DrawState()
    On Error Resume Next
    If m_State = 1 Then 'mouse hover
        UserControl.backcolor = cor_fundo_hover
        Label1.ForeColor = cor_letra_hover
        Label_Descricao.ForeColor = cor_letra_hover_2
    
    ElseIf m_State = 2 Then 'mouse down
        UserControl.backcolor = cor_fundo_down
        Label1.ForeColor = cor_letra_down
        Label_Descricao.ForeColor = cor_letra_down_2
        
    Else 'normal
        UserControl.backcolor = cor_fundo_normal
        Label1.ForeColor = cor_letra_normal
        Label_Descricao.ForeColor = cor_letra_normal_2
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
    FontSize = Label1.FontSize
End Property

Public Property Let FontSize(New_Value As Integer)
    'Alterar o tamanho da letra
    Label1.FontSize = New_Value
    PropertyChanged "FontSize"
End Property

Public Property Get FontBold() As Boolean
    'Indicar se que ou não a letra em negrito
    FontBold = Label1.FontBold
End Property

Public Property Let FontBold(New_Value As Boolean)
    'Alterar a letra para negrito se for o caso
    Label1.FontBold = New_Value
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
        Caption = .ReadProperty("Caption", "NSelection1")
        Description = .ReadProperty("Description", "Descrição")
        BackColorNormal = .ReadProperty("BackColorNormal", "&H00000000&")
        BackColorHover = .ReadProperty("BackColorHover", "&H002D2D2D&")
        BackColorDown = .ReadProperty("BackColorDown", "&H80FFFF")
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
    End With
    
Corrige_UserControl_ReadProperties:
End Sub

Private Sub UserControl_WriteProperties(PropBag As PropertyBag)
    'Escrever as propriedades do control
    On Error GoTo Corrige_UserControl_WriteProperties
    With PropBag
        Call .WriteProperty("Caption", Caption, "")
        Call .WriteProperty("Description", Description, "")
        Call .WriteProperty("BackColorNormal", BackColorNormal, "&H00000000&")
        Call .WriteProperty("BackColorHover", BackColorHover, "&H002D2D2D&")
        Call .WriteProperty("BackColorDown", BackColorDown, "&H80FFFF")
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
    On Error Resume Next
    With UserControl
        .Height = Screen.TwipsPerPixelY * Image1.Height
    End With
    
    With Label1
        .Top = (UserControl.ScaleHeight / 2) - Label1.Height
        .left = 35
    End With
    
    With Label_Descricao
        .Top = (UserControl.ScaleHeight / 2)
        .left = Label1.left
    End With
End Sub

Public Property Get ForeColorNormal() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    ForeColorNormal = Label1.ForeColor
End Property

Public Property Let ForeColorNormal(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_letra_normal = New_Value
    Label1.ForeColor = New_Value
    PropertyChanged "ForeColorNormal"
End Property

Public Property Get ForeColorHover() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    ForeColorHover = cor_letra_hover
End Property

Public Property Let ForeColorHover(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_hover = New_Value
    'UserControl.BackColor  = new_Value
    PropertyChanged "ForeColorHover"
End Property

Public Property Get ForeColorDown() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    ForeColorDown = cor_letra_down
End Property

Public Property Let ForeColorDown(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_down = New_Value
    'UserControl.BackColor  = new_Value
    PropertyChanged "ForeColorDown"
End Property

Public Property Get BackColorNormal() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    BackColorNormal = UserControl.backcolor
End Property

Public Property Let BackColorNormal(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_fundo_normal = New_Value
    UserControl.backcolor = New_Value
    PropertyChanged "BackColorNormal"
End Property

Public Property Get BackColorHover() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    BackColorHover = cor_fundo_hover
End Property

Public Property Let BackColorHover(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_fundo_hover = New_Value
    'UserControl.BackColor  = new_Value
    PropertyChanged "BackColorHover"
End Property

Public Property Get BackColorDown() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    BackColorDown = cor_fundo_down
End Property

Public Property Let BackColorDown(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_fundo_down = New_Value
    'UserControl.BackColor  = new_Value
    PropertyChanged "BackColorDown"
End Property

Private Sub Label_Descricao_Click()
    'Atalho para
    UserControl_Click
End Sub

Private Sub Label_Descricao_DblClick()
    'Atalho para
    UserControl_DblClick
End Sub

Private Sub Label_Descricao_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Evento mousedown
    RaiseEvent MouseDown(Button, Shift, x, y)
    If Button = 1 Then
        m_State = 2
        Call DrawState
    End If
End Sub

Private Sub Label_Descricao_MouseMove(Button As Integer, Shift As Integer, x As Single, y As Single)
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

Private Sub Label_Descricao_MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
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
    ForeColorNormal_2 = Label_Descricao.ForeColor
End Property

Public Property Let ForeColorNormal_2(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_letra_normal_2 = New_Value
    Label_Descricao.ForeColor = New_Value
    PropertyChanged "ForeColorNormal_2"
End Property

Public Property Get ForeColorHover_2() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    ForeColorHover_2 = cor_letra_hover_2
End Property

Public Property Let ForeColorHover_2(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_hover_2 = New_Value
    'UserControl.BackColor  = new_Value
    PropertyChanged "ForeColorHover_2"
End Property

Public Property Get ForeColorDown_2() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    ForeColorDown_2 = cor_letra_down_2
End Property

Public Property Let ForeColorDown_2(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_down_2 = New_Value
    'UserControl.BackColor  = new_Value
    PropertyChanged "ForeColorDown_2"
End Property



