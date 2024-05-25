import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineScript, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QIcon

class WebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def featurePermissionRequested(self, securityOrigin, feature):
        if feature in {QWebEnginePage.MediaAudioCapture, QWebEnginePage.MediaVideoCapture, QWebEnginePage.MediaAudioVideoCapture}:
            self.setFeaturePermission(securityOrigin, feature, QWebEnginePage.PermissionGrantedByUser)
        else:
            super().featurePermissionRequested(securityOrigin, feature)

class YouTubeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Desktop")
        self.setGeometry(100, 100, 800, 600)

        # Configurar el ícono de la aplicación
        self.setWindowIcon(QIcon("icon.ico"))  # Reemplaza con la ruta a tu archivo de ícono

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Configurar la página web personalizada con permisos
        self.web_page = WebEnginePage(self.web_view)
        self.web_view.setPage(self.web_page)

        # Desactivar la aplicación de los estilos específicos de YouTube
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)

        # Conectar el evento de carga de la página para inyectar JavaScript
        self.web_view.page().loadFinished.connect(self.eliminar_elementos)

        # Crear un objeto QUrl con la URL de YouTube
        url = QUrl("https://www.youtube.com")

        # Cargar la URL
        self.web_view.load(url)

        # Iniciar un temporizador para buscar y eliminar repetidamente los elementos
        self.timer = QTimer()
        self.timer.timeout.connect(self.eliminar_elementos)
        self.timer.start(5000)  # Ejecutar cada 5 segundos

    def eliminar_elementos(self):
        # Inyectar JavaScript para eliminar los elementos del DOM, deshabilitar la selección de texto
        # y desactivar el menú contextual del botón derecho del mouse
        js_code = """
        // Eliminar el botón de "Acceder"
        var accederButton = document.querySelector("yt-button-shape a[aria-label='Acceder']");
        if (accederButton) {
            accederButton.parentNode.removeChild(accederButton);
        }
        // Eliminar el div con el icono
        var divElement = document.querySelector("yt-icon-shape div");
        if (divElement) {
            divElement.parentNode.removeChild(divElement);
        }
        // Eliminar el botón de guía
        var guideButton = document.querySelector("yt-icon-button#guide-button");
        if (guideButton) {
            guideButton.parentNode.removeChild(guideButton);
        }
        // Eliminar el botón de configuración
        var configButton = document.querySelector("yt-icon-button[aria-label='Configuración']");
        if (configButton) {
            configButton.parentNode.removeChild(configButton);
        }

        // Deshabilitar la selección de texto en toda la página
        document.body.style.userSelect = 'none';

        // Desactivar el menú contextual del botón derecho del mouse
        window.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        });
        """
        self.web_view.page().runJavaScript(js_code)

def main():
    app = QApplication(sys.argv)
    window = YouTubeApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
