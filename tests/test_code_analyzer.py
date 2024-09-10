import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QPushButton

from main import CodeAnalyzerWindow, client
from sample_code import calculate_average, generate_random_numbers, print_results


# Fixture for QApplication
@pytest.fixture(scope="module")
def app(qapp):
    return qapp


# Fixture for CodeAnalyzerWindow
@pytest.fixture(scope="function")
def window(qtbot, mocker):
    # Mock the Anthropic client
    mock_response = mocker.Mock()
    mock_response.content = [mocker.Mock(text="Mocked analysis result")]
    mocker.patch.object(client.messages, "create", return_value=mock_response)
    window = CodeAnalyzerWindow()
    qtbot.addWidget(window)
    return window


def test_window_title(window):
    assert window.windowTitle() == "AI Code Analyzer"


def test_input_output_elements(window):
    assert window.code_input is not None
    assert window.result_output is not None
    assert window.result_output.isReadOnly()


def test_analyze_button(window):
    analyze_button = window.findChild(QPushButton, "")
    assert analyze_button is not None
    assert analyze_button.text() == "Analyze Code"


def test_empty_input(window):
    window.code_input.setPlainText("")
    analyze_button = window.findChild(QPushButton, "")
    QTest.mouseClick(analyze_button, Qt.LeftButton)
    assert window.result_output.toPlainText() == "Please enter some code to analyze."


def test_analyze_code(window):
    window.code_input.setPlainText("def test_function():\n    pass")
    analyze_button = window.findChild(QPushButton, "")
    QTest.mouseClick(analyze_button, Qt.LeftButton)

    # Give some time for the UI to update
    QTest.qWait(100)

    assert "Mocked analysis result" in window.result_output.toPlainText()


# Tests for sample_code.py functions
def test_calculate_average():
    numbers = [1, 2, 3, 4, 5]
    assert calculate_average(numbers) == 3.0


def test_calculate_average_empty_list():
    with pytest.raises(ZeroDivisionError):
        calculate_average([])


def test_generate_random_numbers():
    n = 5
    random_numbers = generate_random_numbers(n)
    assert len(random_numbers) == n
    assert all(1 <= num <= 100 for num in random_numbers)


def test_print_results(capsys):
    numbers = [1, 2, 3]
    average = 2.0
    print_results(numbers, average)
    captured = capsys.readouterr()
    assert "Numbers: [1, 2, 3]" in captured.out
    assert "Average: 2.0" in captured.out


if __name__ == "__main__":
    pytest.main(["-v", __file__])
