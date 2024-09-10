# AI Code Analyzer

AI Code Analyzer is a Python application that uses the Anthropic API to analyze Python code and provide suggestions for improvement. It features a user-friendly GUI built with PyQt5, including syntax highlighting for Python code.

## File Structure

.
├── main.py
├
└── requirements.txt

## Prerequisites

- Python 3.9 or higher
- Anthropic API key

## Installation

1. Clone this repository or download the `main.py` file.

2. Install the required dependencies:

3. Set up your Anthropic API key:
- Create a `.env` file in the same directory as `main.py`
- Add your Anthropic API key to the `.env` file:
  ```
  ANTHROPIC_API_KEY=your_api_key_here
  ```

## Usage

Run the application:

1. The application window will open.
2. Enter your Python code in the top text area.
3. Click the "Analyze Code" button.
4. The analysis results will appear in the bottom text area.

## Features

- Syntax highlighting for Python code
- Dark theme for comfortable coding
- Adjustable split view for input and output
- Status bar for feedback on analysis progress

## Dependencies

The main dependencies for this project are:

- PyQt5: For the graphical user interface
- anthropic: To interact with the Anthropic API
- python-dotenv: For loading environment variables

For a full list of dependencies, see `requirements.txt`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).