import sys
import os
from anthropic import Anthropic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTextEdit, QStatusBar, QSplitter)
from PyQt5.QtGui import QFont, QColor, QPalette, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import Qt, QRegExp


from dotenv import load_dotenv

load_dotenv()


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

client = Anthropic(api_key=ANTHROPIC_API_KEY)

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlightingRules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FF7043"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ["def", "class", "for", "while", "if", "elif", "else", "try", "except", "import", "from", "as"]
        for word in keywords:
            self.highlightingRules.append((QRegExp("\\b" + word + "\\b"), keyword_format))

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#42A5F5"))
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"), function_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#66BB6A"))
        self.highlightingRules.append((QRegExp("\".*\""), string_format))
        self.highlightingRules.append((QRegExp("'.*'"), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#78909C"))
        self.highlightingRules.append((QRegExp("#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

class CodeAnalyzerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Code Analyzer")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #263238;
            }
            QLabel {
                color: #ECEFF1;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #00BCD4;
                color: white;
                border: none;
                padding: 5px 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #00ACC1;
            }
            QTextEdit {
                background-color: #37474F;
                color: #ECEFF1;
                border: 1px solid #546E7A;
                border-radius: 3px;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
        """)

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)

        # Input section
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)
        
        input_label = QLabel("Enter Python code:")
        self.code_input = QTextEdit()
        self.highlighter = PythonHighlighter(self.code_input.document())
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.code_input)

        # Button
        analyze_button = QPushButton("Analyze Code")
        analyze_button.clicked.connect(self.analyze_code)
        input_layout.addWidget(analyze_button)

        splitter.addWidget(input_widget)

        # Output section
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)

        output_label = QLabel("Analysis Results:")
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.result_output)

        splitter.addWidget(output_widget)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def analyze_code(self):
        code = self.code_input.toPlainText().strip()
        if not code:
            self.result_output.setPlainText("Please enter some code to analyze.")
            return

        self.statusBar.showMessage("Analyzing code...")
        try:
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0,
                system="You are a helpful assistant that analyzes Python code.",
                messages=[
                    {
                        "role": "user", 
                        "content": f"Analyze this Python code and provide suggestions for improvement:\n\n{code}"
                    }
                ]
            )
            analysis = response.content[0].text
            self.result_output.setPlainText(analysis)
            self.statusBar.showMessage("Analysis complete", 3000)
        except Exception as e:
            self.result_output.setPlainText(f"An error occurred: {str(e)}")
            self.statusBar.showMessage("Error occurred during analysis", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeAnalyzerWindow()
    window.show()
    sys.exit(app.exec_())