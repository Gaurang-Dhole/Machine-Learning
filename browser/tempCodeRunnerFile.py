import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QToolBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Simple Web Browser")
        self.setGeometry(100, 100, 1024, 768)

        # Create a QWebEngineView widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        # Create a URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Create a toolbar
        toolbar = QToolBar()
        toolbar.addWidget(self.url_bar)
        self.addToolBar(toolbar)

        # Set the central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.browser)
        self.setCentralWidget(central_widget)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())