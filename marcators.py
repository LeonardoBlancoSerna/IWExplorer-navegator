import wx


class MarcadoresDialog(wx.Dialog):
    def __init__(self, parent):
        super(MarcadoresDialog, self).__init__(parent, title="Marcadores", size=(400, 300))
        
        self.marcadores = []  # Lista de marcadores (puedes cargarla desde un archivo o base de datos)
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del diálogo de marcadores."""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Lista de marcadores
        self.lista_marcadores = wx.ListBox(self, choices=self.marcadores, style=wx.LB_SINGLE)
        vbox.Add(self.lista_marcadores, 1, wx.EXPAND | wx.ALL, 5)
        
        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_agregar = wx.Button(self, label="Agregar")
        self.btn_eliminar = wx.Button(self, label="Eliminar")
        self.btn_visitar = wx.Button(self, label="Visitar")
        
        hbox.Add(self.btn_agregar, 0, wx.ALL, 5)
        hbox.Add(self.btn_eliminar, 0, wx.ALL, 5)
        hbox.Add(self.btn_visitar, 0, wx.ALL, 5)
        
        vbox.Add(hbox, 0, wx.ALIGN_CENTER)
        
        self.SetSizer(vbox)
        
        # Conectar eventos
        self.btn_agregar.Bind(wx.EVT_BUTTON, self.agregar_marcador)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_marcador)
        self.btn_visitar.Bind(wx.EVT_BUTTON, self.visitar_marcador)
    
    def agregar_marcador(self, event):
        """Agregar un nuevo marcador."""
        dlg = wx.TextEntryDialog(self, "Ingresa la URL del marcador:", "Agregar Marcador")
        if dlg.ShowModal() == wx.ID_OK:
            url = dlg.GetValue().strip()
            if url and url not in self.marcadores:
                self.marcadores.append(url)
                self.lista_marcadores.Append(url)
        dlg.Destroy()
    
    def eliminar_marcador(self, event):
        """Eliminar el marcador seleccionado."""
        seleccion = self.lista_marcadores.GetSelection()
        if seleccion != wx.NOT_FOUND:
            self.marcadores.pop(seleccion)
            self.lista_marcadores.Delete(seleccion)
    
    def visitar_marcador(self, event):
        """Visitar el marcador seleccionado."""
        seleccion = self.lista_marcadores.GetSelection()
        if seleccion != wx.NOT_FOUND:
            url = self.marcadores[seleccion]
            wx.MessageBox(f"Visitar: {url}\n(Implementar navegación en la ventana principal)", "Visitar Marcador", wx.OK | wx.ICON_INFORMATION)