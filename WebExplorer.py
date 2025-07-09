import wx
import wx.html2
from configuracion import ConfiguracionDialog
from urllib.parse import urlparse
from history import HistorialDialog
from marcators import MarcadoresDialog


class NavegadorFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(NavegadorFrame, self).__init__(*args, **kwargs)
        
        # Variables compartidas
        self.home_page = "https://www.google.com"  # Página de inicio predeterminada
        self.pestanas_abiertas = []  # Lista para gestionar las pestañas abiertas
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz principal del navegador."""
        # Configuración de la ventana principal
        self.SetTitle("IWExplor")
        self.SetSize((1024, 768))
        
        # Crear una barra de menú
        self.crear_menu_barra()
        
        # Crear un panel principal
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Barra de navegación
        self.nav_panel = wx.Panel(panel)
        nav_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Etiqueta para la barra de direcciones
        self.lbl_url = wx.StaticText(self.nav_panel, label="Barra de direcciones web:")
        self.input_url = wx.TextCtrl(self.nav_panel, style=wx.TE_PROCESS_ENTER)
        
        # Botones
        self.btn_recargar = wx.Button(self.nav_panel, label="Recargar")
        self.btn_ir = wx.Button(self.nav_panel, label="Ir")
        
        # Conectar eventos a los botones
        self.btn_ir.Bind(wx.EVT_BUTTON, self.navegar_a_url)
        self.input_url.Bind(wx.EVT_TEXT_ENTER, self.navegar_a_url)
        self.btn_recargar.Bind(wx.EVT_BUTTON, self.recargar_pagina)
        
        # Agregar widgets a la barra de navegación
        nav_box.Add(self.btn_recargar, 0, wx.ALL, 5)
        nav_box.Add(self.lbl_url, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        nav_box.Add(self.input_url, 1, wx.ALL | wx.EXPAND, 5)
        nav_box.Add(self.btn_ir, 0, wx.ALL, 5)
        self.nav_panel.SetSizer(nav_box)
        
        # WebView para renderizar contenido web
        self.web_view = wx.html2.WebView.New(panel)
        
        # Agregar barra de navegación y WebView al layout principal
        vbox.Add(self.nav_panel, 0, wx.EXPAND)
        vbox.Add(self.web_view, 1, wx.EXPAND)
        panel.SetSizer(vbox)
        
        # Cargar página inicial
        self.cargar_pagina_inicial()
    
    def crear_menu_barra(self):
        """Crear la barra de menú con las funcionalidades solicitadas."""
        menu_bar = wx.MenuBar()
        
        # Menú Archivo
        menu_archivo = wx.Menu()
        item_configuracion = menu_archivo.Append(wx.ID_ANY, "Configuración", "Abrir configuración")
        self.Bind(wx.EVT_MENU, self.abrir_configuracion, item_configuracion)
        menu_bar.Append(menu_archivo, "&Archivo")
        
        # Menú Marcadores
        menu_marcadores = wx.Menu()
        item_ver_marcadores = menu_marcadores.Append(wx.ID_ANY, "Ver marcadores", "Abrir la lista de marcadores")
        self.Bind(wx.EVT_MENU, self.ver_marcadores, item_ver_marcadores)
        menu_bar.Append(menu_marcadores, "&Marcadores")
        
        # Menú Historial
        menu_historial = wx.Menu()
        item_ver_historial = menu_historial.Append(wx.ID_ANY, "Ver historial\tCtrl+H", "Abrir el historial de navegación")
        self.Bind(wx.EVT_MENU, self.ver_historial, item_ver_historial)
        menu_bar.Append(menu_historial, "&Historial")
        
        # Menú Pestañas
        menu_pestanas = wx.Menu()
        item_nueva_pestana = menu_pestanas.Append(wx.ID_ANY, "Nueva pestaña", "Abrir una nueva pestaña")
        item_incognito = menu_pestanas.Append(wx.ID_ANY, "Nueva pestaña sin registros", "Abrir una pestaña de incógnito")
        item_nueva_ventana = menu_pestanas.Append(wx.ID_ANY, "Nueva ventana", "Abrir una nueva ventana")
        
        submenu_pestanas_abiertas = wx.Menu()
        menu_pestanas.AppendSubMenu(submenu_pestanas_abiertas, "Pestañas abiertas")
        
        self.Bind(wx.EVT_MENU, self.nueva_pestana, item_nueva_pestana)
        self.Bind(wx.EVT_MENU, self.nueva_pestana_incognito, item_incognito)
        self.Bind(wx.EVT_MENU, self.nueva_ventana, item_nueva_ventana)
        
        # Atajo de teclado para cambiar entre pestañas (Ctrl+Tab)
        self.Bind(wx.EVT_KEY_DOWN, self.cambiar_pestana)
        
        menu_bar.Append(menu_pestanas, "&Pestañas")
        
        self.SetMenuBar(menu_bar)
    
    def cargar_pagina_inicial(self):
        """Cargar la página de inicio predeterminada."""
        try:
            self.web_view.LoadURL(self.home_page)
            self.input_url.SetValue(self.home_page)
        except Exception as e:
            wx.MessageBox(f"No se pudo cargar la página inicial: {e}", "Error", wx.OK | wx.ICON_ERROR)
    
    def navegar_a_url(self, event):
        """Navegar a la URL ingresada por el usuario."""
        url = self.input_url.GetValue().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url  # Usar https como predeterminado
        
        if self.validar_url(url):
            try:
                self.web_view.LoadURL(url)
                self.input_url.SetValue(url)
            except Exception as e:
                wx.MessageBox(f"Hubo un error al cargar la URL: {e}", "Error de Carga", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("La URL ingresada no es válida. Por favor, verifica el formato.", "Error de URL", wx.OK | wx.ICON_ERROR)
    
    def validar_url(self, url):
        """Validar el formato de la URL."""
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    
    def recargar_pagina(self, event):
        """Recargar la página actual."""
        try:
            self.web_view.Reload()
        except Exception as e:
            wx.MessageBox(f"No se pudo recargar la página: {e}", "Error de Recarga", wx.OK | wx.ICON_ERROR)
    
    def abrir_configuracion(self, event):
        """Abrir el diálogo de configuración."""
        try:
            configuracion_dialog = ConfiguracionDialog(self)
            if configuracion_dialog.ShowModal() == wx.ID_OK:
                pass
            configuracion_dialog.Destroy()
        except Exception as e:
            wx.MessageBox(f"No se pudo abrir el diálogo de configuración: {e}", "Error", wx.OK | wx.ICON_ERROR)
    
    def ver_marcadores(self, event):
        """Abrir la lista de marcadores."""
        wx.MessageBox("Funcionalidad de marcadores no implementada.", "Marcadores", wx.OK | wx.ICON_INFORMATION)
    
    def ver_historial(self, event):
        """Abrir el historial de navegación."""
        wx.MessageBox("Funcionalidad de historial no implementada.", "Historial", wx.OK | wx.ICON_INFORMATION)
    
    def nueva_pestana(self, event):
        """Abrir una nueva pestaña."""
        wx.MessageBox("Funcionalidad de nueva pestaña no implementada.", "Nueva Pestaña", wx.OK | wx.ICON_INFORMATION)
    
    def nueva_pestana_incognito(self, event):
        """Abrir una nueva pestaña sin registros."""
        wx.MessageBox("Funcionalidad de pestaña de incógnito no implementada.", "Nueva Pestaña Sin Registros", wx.OK | wx.ICON_INFORMATION)
    
    def nueva_ventana(self, event):
        """Abrir una nueva ventana."""
        wx.MessageBox("Funcionalidad de nueva ventana no implementada.", "Nueva Ventana", wx.OK | wx.ICON_INFORMATION)
    
    def cambiar_pestana(self, event):
        """Cambiar entre pestañas abiertas con Ctrl+Tab."""
        wx.MessageBox("Funcionalidad de cambiar entre pestañas no implementada.", "Cambiar Pestaña", wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = wx.App(False)
    frame = NavegadorFrame(None)
    frame.Show()  # Mostrar la ventana principal del navegador
    app.MainLoop()