import sys
from PyQt5.QtCore import QUrl, QSettings
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QVBoxLayout, 
                            QWidget, QToolBar, QAction, QComboBox, QStyle)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("YourCompany", "WebBrowser")
        self.search_engines = {
            "Google": "https://www.google.com/search?q=",
            "DuckDuckGo": "https://duckduckgo.com/?q=",
            "Bing": "https://www.bing.com/search?q=",
            "Yahoo": "https://search.yahoo.com/search?p="
        }
        
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        # Window setup
        self.setWindowTitle("Aesthetic Browser")
        self.setGeometry(100, 100, 1280, 800)
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView)))

        # Dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QToolBar {
                background-color: #3c3f41;
                border: none;
                padding: 4px;
            }
            QLineEdit {
                background-color: #4e5254;
                color: #ffffff;
                border: 2px solid #5d6061;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 14px;
            }
            QComboBox {
                background-color: #4e5254;
                color: #ffffff;
                border: 2px solid #5d6061;
                border-radius: 12px;
                padding: 3px 10px;
                min-width: 120px;
            }
            QComboBox QAbstractItemView {
                background-color: #4e5254;
                color: #ffffff;
                selection-background-color: #5d6061;
            }
            QPushButton {
                background-color: #4e5254;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #5d6061;
            }
        """)

        # Web view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.urlChanged.connect(self.update_url_bar)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Search engine selector
        self.search_engine_box = QComboBox()
        self.search_engine_box.addItems(self.search_engines.keys())
        self.search_engine_box.currentIndexChanged.connect(self.save_settings)

        # Navigation toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Navigation buttons
        back_btn = QAction(QIcon(self.style().standardIcon(QStyle.SP_ArrowBack)), "Back", self)
        back_btn.triggered.connect(self.browser.back)
        toolbar.addAction(back_btn)

        forward_btn = QAction(QIcon(self.style().standardIcon(QStyle.SP_ArrowForward)), "Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_btn)

        reload_btn = QAction(QIcon(self.style().standardIcon(QStyle.SP_BrowserReload)), "Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        toolbar.addAction(reload_btn)

        toolbar.addWidget(self.search_engine_box)
        toolbar.addWidget(self.url_bar)

        # Main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)
        self.setCentralWidget(central_widget)

    def navigate_to_url(self):
        input_text = self.url_bar.text()
        search_engine = self.search_engine_box.currentText()
        search_url = self.search_engines[search_engine]

        # Check if input is a valid URL
        if '.' in input_text and ' ' not in input_text:
            if not input_text.startswith(('http://', 'https://')):
                url = QUrl("http://" + input_text)
            else:
                url = QUrl(input_text)
        else:
            # Treat as search query
            query = input_text.replace(' ', '+')
            url = QUrl(search_url + query)

        self.browser.setUrl(url)

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def save_settings(self):
        self.settings.setValue("search_engine", self.search_engine_box.currentIndex())

    def load_settings(self):
        engine_index = self.settings.value("search_engine", 0, type=int)
        self.search_engine_box.setCurrentIndex(engine_index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())