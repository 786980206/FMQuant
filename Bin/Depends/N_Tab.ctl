VERSION 5.00
Begin VB.UserControl N_Tab 
   BackColor       =   &H00F9F9F9&
   ClientHeight    =   510
   ClientLeft      =   0
   ClientTop       =   0
   ClientWidth     =   5535
   ScaleHeight     =   34
   ScaleMode       =   3  'Pixel
   ScaleWidth      =   369
   Begin VB.Timer Timer1 
      Enabled         =   0   'False
      Interval        =   1
      Left            =   4080
      Top             =   0
   End
   Begin VB.Label Image_Separador 
      BackColor       =   &H00E0E0E0&
      Enabled         =   0   'False
      Height          =   375
      Left            =   1320
      TabIndex        =   7
      Top             =   0
      Width           =   15
   End
   Begin VB.Label Linha_Menu_Activo 
      BackColor       =   &H00FFCB35&
      Enabled         =   0   'False
      Height          =   30
      Left            =   0
      TabIndex        =   6
      Top             =   420
      Width           =   1095
   End
   Begin VB.Image Icon_Tab 
      Enabled         =   0   'False
      Height          =   105
      Left            =   1800
      Picture         =   "N_Tab.ctx":0000
      Top             =   120
      Visible         =   0   'False
      Width           =   165
   End
   Begin VB.Label Fundo_Menu_Activo 
      Appearance      =   0  'Flat
      BackColor       =   &H00E7E7E7&
      BorderStyle     =   1  'Fixed Single
      ForeColor       =   &H80000008&
      Height          =   375
      Left            =   3360
      TabIndex        =   4
      Top             =   0
      Visible         =   0   'False
      Width           =   375
   End
   Begin VB.Label Fundo_Menu_Over 
      Appearance      =   0  'Flat
      BackColor       =   &H00F2F2F2&
      BorderStyle     =   1  'Fixed Single
      ForeColor       =   &H80000008&
      Height          =   375
      Left            =   2880
      TabIndex        =   3
      Top             =   0
      Visible         =   0   'False
      Width           =   375
   End
   Begin VB.Label Fundo_Menu_Normal 
      Appearance      =   0  'Flat
      BackColor       =   &H00F9F9F9&
      BorderStyle     =   1  'Fixed Single
      ForeColor       =   &H80000008&
      Height          =   375
      Left            =   2400
      TabIndex        =   2
      Top             =   0
      Visible         =   0   'False
      Width           =   375
   End
   Begin VB.Label Label_Close 
      BackColor       =   &H00C0C0C0&
      BackStyle       =   0  'Transparent
      Caption         =   " x "
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H006F6F6F&
      Height          =   225
      Left            =   1440
      TabIndex        =   1
      Top             =   120
      Width           =   225
   End
   Begin VB.Label Label1 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "N_Tab"
      BeginProperty Font 
         Name            =   "Verdana"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H006F6F6F&
      Height          =   195
      Left            =   240
      TabIndex        =   0
      Top             =   120
      Width           =   540
   End
   Begin VB.Label Fundo_Tab 
      Appearance      =   0  'Flat
      BackColor       =   &H00F9F9F9&
      Enabled         =   0   'False
      ForeColor       =   &H80000008&
      Height          =   720
      Left            =   0
      TabIndex        =   5
      Top             =   0
      Width           =   1095
   End
End
Attribute VB_Name = "N_Tab"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'Component: NTab
'Copyright (c) 2013 Nikyts Software - Informatic and thecnologies
'Developed by Nelson do Carmo
'Contact: nikyts@hotmail.com
'Web: www.NikitaSoftware.net
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

'Variáveis das funções que o botão deverá ter
Dim m_Tab_Activo As Boolean
Dim m_Separador_Visivel As Boolean
Dim m_Close_Visivel As Boolean
Dim ajustar_ao_texto As Boolean
Dim m_Menu_Visivel As Boolean

'Cores utilizadas pelos eventos do botao
Dim cor_fundo_normal As OLE_COLOR
Dim cor_fundo_hover As OLE_COLOR
Dim cor_fundo_down As OLE_COLOR

Dim cor_contorno_normal As OLE_COLOR
Dim cor_contorno_hover As OLE_COLOR
Dim cor_contorno_down As OLE_COLOR
Dim cor_contorno_original As OLE_COLOR
Dim cor_contorno_custom As OLE_COLOR

Dim cor_letra_normal As OLE_COLOR
Dim cor_letra_hover As OLE_COLOR
Dim cor_letra_down As OLE_COLOR

Dim cor_linha As OLE_COLOR

'Variavel para saber se é para alterar a cor do border ao receber o focus
Dim alterar_cor_contorno As Boolean

Public Event CloseTab(ByVal eliminar_tab As Boolean)



Private Sub Label_Close_MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
    'Indicar que é para fechar o tab ao clicar na cruz
    RaiseEvent MouseDown(Button, Shift, x, y)
    If Button = 1 Then
        RaiseEvent CloseTab(True)
    End If
End Sub

Private Sub Label1_Change()
    'Ajustar o botao ao alterar o texto da label
    Call Ajustar_Botao
End Sub

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
    If m_Tab_Activo = False Then
        m_Tab_Activo = True
        Linha_Menu_Activo.Visible = True
        Fundo_Tab.BackColor = Fundo_Menu_Normal.BackColor
    End If
End Sub

Private Sub UserControl_DblClick()
    'Evento duploclick
    RaiseEvent DblClick
End Sub

Private Sub UserControl_Initialize()
    'Iniciando o componente
    Call Ajustar_Botao
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

Private Sub UserControl_InitProperties()
    'Ler as propriedades do botão
    On Error GoTo Corrige_UserControl_InitProperties
    Caption = UserControl.Extender.Name
    Enabled = True
    BackGround = &HFFFFFF 'Branco
    FontSize = 8
    FontBold = False
    Font = "Verdana" '"MS Sans Serif"
    ForeColorNormal = RGB(0, 0, 0) '&H0&
    ForeColorHover = RGB(0, 0, 0)
    ForeColorDown = RGB(0, 0, 0)
    Call Ajustar_Botao
    Tab_Activo = False
    Separador_Visivel = True
    Close_Visivel = True
    Menu_Visivel = False
    BackColorLine = RGB(0, 0, 0)
    
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
        Fundo_Tab.BackColor = Fundo_Menu_Over.BackColor

    ElseIf m_State = 2 Then 'mouse down
        Fundo_Tab.BackColor = Fundo_Menu_Activo.BackColor

    Else 'normal
        Fundo_Tab.BackColor = Fundo_Menu_Normal.BackColor
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
    
'    If New_Value = True Then
'        Label1.ForeColor = cor_letra_normal
'    Else
'        Label1.ForeColor = &HB3B3B3  'Cinzento escuro
'    End If
    UserControl.Refresh
End Property

Private Sub UserControl_ReadProperties(PropBag As PropertyBag)
    'Ler as propriedades do control
    On Error GoTo Corrige_UserControl_ReadProperties
    With PropBag
        Caption = .ReadProperty("Caption", "NTab1")
        BackGround = .ReadProperty("BackGround", "&HFF8080")
        FontSize = .ReadProperty("FontSize", "8")
        FontBold = .ReadProperty("FontBold", "False")
        Font = .ReadProperty("Font", "MS Sans Serif")
        Enabled = .ReadProperty("Enabled", "True")
        ForeColorNormal = .ReadProperty("ForeColorNormal", "&H8080FF")
        ForeColorHover = .ReadProperty("ForeColorHover", "&H8080FF")
        ForeColorDown = .ReadProperty("ForeColorDown", "&H8080FF")
        Tab_Activo = .ReadProperty("Tab_Activo", "False")
        Separador_Visivel = .ReadProperty("Separador_Visivel", "False")
        Close_Visivel = .ReadProperty("Close_Visivel", "False")
        Menu_Visivel = .ReadProperty("Menu_Visivel", "False")
        BackColorLine = .ReadProperty("BackColorLine", "&HFF8080")
    End With
    
Corrige_UserControl_ReadProperties:
End Sub

Private Sub UserControl_WriteProperties(PropBag As PropertyBag)
    'Escrever as propriedades do control
    On Error GoTo Corrige_UserControl_WriteProperties
    With PropBag
        Call .WriteProperty("Caption", Caption, "")
        Call .WriteProperty("BackGround", BackGround, "&HFF8080")
        Call .WriteProperty("FontSize", FontSize, "8")
        Call .WriteProperty("FontBold", FontBold, "False")
        Call .WriteProperty("Font", Font, "MS Sans Serif")
        Call .WriteProperty("Enabled", Enabled, "True")
        Call .WriteProperty("ForeColorNormal", ForeColorNormal, "&HFF8080")
        Call .WriteProperty("ForeColorHover", ForeColorHover, "&HFF8080")
        Call .WriteProperty("ForeColorDown", ForeColorDown, "&HFF8080")
        Call .WriteProperty("List_Icons", novo_icon, 1)
        Call .WriteProperty("Tab_Activo", Tab_Activo, "False")
        Call .WriteProperty("Separador_Visivel", Separador_Visivel, "False")
        Call .WriteProperty("Close_Visivel", Close_Visivel, "False")
        Call .WriteProperty("Menu_Visivel", Menu_Visivel, "False")
        Call .WriteProperty("BackColorLine", BackColorLine, "&HFF8080")
    End With
    
Corrige_UserControl_WriteProperties:
End Sub

Public Property Get Tab_Activo() As Boolean
    'Escolher se o botão fica activo ou não
    Tab_Activo = m_Tab_Activo
End Property

Public Property Let Tab_Activo(New_Value As Boolean)
    'Verificar se o botão fica activo ou não
    m_Tab_Activo = New_Value
    PropertyChanged "Tab_Activo"

    If m_Tab_Activo = True Then
        Linha_Menu_Activo.Visible = True
        'Image_Separador.Visible = False
    Else
        Linha_Menu_Activo.Visible = False
        'If m_Separador_Visivel = True Then Image_Separador.Visible = True
    End If
    
    'Call Ajustar_Botao
End Property

Public Property Get Separador_Visivel() As Boolean
    'Escolher se o botão fica activo ou não
    Separador_Visivel = m_Separador_Visivel
End Property

Public Property Let Separador_Visivel(New_Value As Boolean)
    'Verificar se o botão fica activo ou não
    m_Separador_Visivel = New_Value
    PropertyChanged "Separador_Visivel"

    If m_Separador_Visivel = True Then
        If m_Tab_Activo = False Then Image_Separador.Visible = True
    Else
        Image_Separador.Visible = False
    End If
    
    'Call Ajustar_Botao
End Property

Public Property Get Close_Visivel() As Boolean
    'Escolher se o botão fica activo ou não
    Close_Visivel = m_Close_Visivel
End Property

Public Property Let Close_Visivel(New_Value As Boolean)
    'Verificar se o botão fica activo ou não
    m_Close_Visivel = New_Value
    PropertyChanged "Close_Visivel"

    If m_Close_Visivel = True Then
        Label_Close.Visible = True
        Menu_Visivel = False
    Else
        Label_Close.Visible = False
    End If
    Call Ajustar_Botao
End Property

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
        .Height = Screen.TwipsPerPixelY * Fundo_Tab.Height
        If Close_Visivel = True Or Menu_Visivel = True Then
            .Width = Screen.TwipsPerPixelX * (15 + Label1.Width + 15 + Icon_Tab.Width + 10)
        Else
            .Width = Screen.TwipsPerPixelX * (15 + Label1.Width + 15)
        End If
    End With
    
    With Fundo_Tab
        .Top = 0
        .Left = 0
        .Width = UserControl.ScaleWidth
    End With
    
    With Label1
        .Top = (UserControl.ScaleHeight - .Height) \ 2
        .Left = 15
    End With
    
    With Linha_Menu_Activo
        .Top = UserControl.ScaleHeight - .Height
        .Left = 0
        .Width = UserControl.ScaleWidth
    End With
    
    With Image_Separador
        .Top = (UserControl.ScaleHeight - .Height) \ 2
        .Left = UserControl.ScaleWidth - .Width
    End With
    
    With Label_Close
        .Top = (UserControl.ScaleHeight - .Height) \ 2
        .Left = UserControl.ScaleWidth - .Width - 10
    End With
    
    With Icon_Tab
        .Top = (UserControl.ScaleHeight - .Height) \ 2
        .Left = UserControl.ScaleWidth - .Width - 10
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

Public Property Let BackColorLine(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    cor_linha = New_Value
    Linha_Menu_Activo.BackColor = New_Value
    PropertyChanged "BackColorLine"
End Property

Public Property Get BackColorLine() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    BackColorLine = cor_linha
End Property

Public Property Let ForeColorHover(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_hover = New_Value
    PropertyChanged "ForeColorHover"
End Property

Public Property Get ForeColorDown() As OLE_COLOR
    'Escolher a cor inicial da letra do botão
    ForeColorDown = cor_letra_down
End Property

Public Property Let ForeColorDown(New_Value As OLE_COLOR)
    'Alterar a cor inicial da letra do botão
    cor_letra_down = New_Value
    PropertyChanged "ForeColorDown"
End Property

Public Property Get BackGround() As OLE_COLOR
    'Escolher a cor inicial de fundo do botão
    BackGround = UserControl.BackColor
End Property

Public Property Let BackGround(New_Value As OLE_COLOR)
    'Alterar a cor inicial de fundo do botão
    UserControl.BackColor = New_Value
    PropertyChanged "BackGround"
End Property

Public Property Get Menu_Visivel() As Boolean
    'Escolher se o botão fica activo ou não
    Menu_Visivel = m_Menu_Visivel
End Property

Public Property Let Menu_Visivel(New_Value As Boolean)
    'Verificar se o botão fica activo ou não
    m_Menu_Visivel = New_Value
    PropertyChanged "Menu_Visivel"

    If m_Menu_Visivel = True Then
        Icon_Tab.Visible = True
        Close_Visivel = False
    Else
        Icon_Tab.Visible = False
    End If
    Call Ajustar_Botao
End Property
