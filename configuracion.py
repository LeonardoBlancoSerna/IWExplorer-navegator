import wx
from urllib.parse import urlparse


class ConfiguracionDialog(wx.Dialog):
    def __init__(self, parent):
        super(ConfiguracionDialog, self).__init__(parent, title="Configuración", size=(400, 300))
        
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """Inicializar la interfaz del diálogo de configuración."""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Campo para configurar la página de inicio
        hbox_home = wx.BoxSizer(wx.HORIZONTAL)
        lbl_home = wx.StaticText(self, label="Página de inicio:")
        self.input_home = wx.TextCtrl(self)
        self.input_home.SetValue(self.parent.home_page)
        hbox_home.Add(lbl_home, 1, wx.ALL | wx.EXPAND, 5)
        hbox_home.Add(self.input_home, 2, wx.ALL | wx.EXPAND, 5)

        # Opciones de permisos
        permissions_box = wx.StaticBox(self, label="Permisos")
        permissions_sizer = wx.StaticBoxSizer(permissions_box, wx.VERTICAL)

        self.checkbox_microphone = wx.CheckBox(self, label="Acceso a Micrófono")
        self.checkbox_camera = wx.CheckBox(self, label="Acceso a Cámara")
        self.checkbox_notifications = wx.CheckBox(self, label="Notificaciones")

        permissions_sizer.Add(self.checkbox_microphone, 0, wx.ALL, 5)
        permissions_sizer.Add(self.checkbox_camera, 0, wx.ALL, 5)
        permissions_sizer.Add(self.checkbox_notifications, 0, wx.ALL, 5)

        # Botones para guardar y cerrar
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_guardar = wx.Button(self, label="Guardar")
        self.btn_cancelar = wx.Button(self, label="Cancelar")
        self.btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_configuracion)
        self.btn_cancelar.Bind(wx.EVT_BUTTON, self.cerrar_dialogo)
        hbox_buttons.Add(self.btn_guardar, 1, wx.ALL | wx.EXPAND, 5)
        hbox_buttons.Add(self.btn_cancelar, 1, wx.ALL | wx.EXPAND, 5)
        
        # Agregar todo al layout principal
        vbox.Add(hbox_home, 0, wx.ALL | wx.EXPAND, 10)
        vbox.Add(permissions_sizer, 0, wx.ALL | wx.EXPAND, 10)
        vbox.Add(hbox_buttons, 0, wx.ALL | wx.EXPAND, 10)
        
        self.SetSizer(vbox)
    
    def validar_url(self, url):
        """Validar que la URL ingresada tenga un formato válido."""
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    
    def guardar_configuracion(self, event):
        """Guardar la configuración."""
        nueva_pagina = self.input_home.GetValue().strip()
        
        # Validar la URL antes de guardarla
        if not self.validar_url(nueva_pagina):
            wx.MessageBox(
                "La URL ingresada no es válida. Por favor, verifica el formato.",
                "Error de URL",
                wx.OK | wx.ICON_ERROR,
            )
            return
        
        # Guardar la configuración en el objeto principal
        self.parent.home_page = nueva_pagina
        self.parent.allow_microphone = self.checkbox_microphone.GetValue()
        self.parent.allow_camera = self.checkbox_camera.GetValue()
        self.parent.allow_notifications = self.checkbox_notifications.GetValue()

        wx.MessageBox(
            "La configuración se guardó correctamente.",
            "Confirmación",
            wx.OK | wx.ICON_INFORMATION,
        )
        self.EndModal(wx.ID_OK)
    
    def cerrar_dialogo(self, event):
        """Cerrar el diálogo de configuración."""
        self.EndModal(wx.ID_CANCEL)