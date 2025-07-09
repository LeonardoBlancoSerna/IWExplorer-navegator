import wx


class HistorialDialog(wx.Dialog):
    def __init__(self, parent):
        super(HistorialDialog, self).__init__(parent, title="Historial", size=(400, 300))
        
        self.historial = []  # Lista del historial (puedes cargarla desde un archivo o base de datos)
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del diálogo de historial."""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Lista de historial
        self.lista_historial = wx.ListBox(self, choices=self.historial, style=wx.LB_SINGLE)
        vbox.Add(self.lista_historial, 1, wx.EXPAND | wx.ALL, 5)
        
        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_eliminar = wx.Button(self, label="Eliminar")
        self.btn_visitar = wx.Button(self, label="Visitar")
        
        hbox.Add(self.btn_eliminar, 0, wx.ALL, 5)
        hbox.Add(self.btn_visitar, 0, wx.ALL, 5)
        
        vbox.Add(hbox, 0, wx.ALIGN_CENTER)
        
        self.SetSizer(vbox)
        
        # Conectar eventos
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_historial)
        self.btn_visitar.Bind(wx.EVT_BUTTON, self.visitar_historial)
    
    def eliminar_historial(self, event):
        """Eliminar la entrada seleccionada del historial."""
        seleccion = self.lista_historial.GetSelection()
        if seleccion != wx.NOT_FOUND:
            self.historial.pop(seleccion)
            self.lista_historial.Delete(seleccion)
    
    def visitar_historial(self, event):
        """Visitar la entrada seleccionada del historial."""
        seleccion = self.lista_historial.GetSelection()
        if seleccion != wx.NOT_FOUND:
            url = self.historial[seleccion]
            wx.MessageBox(f"Visitar: {url}\n(Implementar navegación en la ventana principal)", "Visitar Historial", wx.OK | wx.ICON_INFORMATION)