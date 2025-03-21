# File System Simulator

A Python-based file system simulator that supports basic operations like creating directories, creating and modifying files, reading file content, and more.

## Features
- Create directories (`mkdir`)
- Create or overwrite files (`touch`)
- Write to files (`write`)
- Read file content (`read`)
- Delete files or directories (`del`)
- List directory contents (`ls`)
- Print the current working directory (`pwd`)
- Get the size of a file or directory (`size`)

## Requirements
- Python 3.8 or higher

## Installation

### Windows
1. Clone the repository:
   ```bash
   git clone https://github.com/sivan-gzt/file-system-simulator/
   ```

### macOS
1. Clone the repository:
   ```bash
   git clone https://github.com/sivan-gzt/file-system-simulator/
   ```

## Running the Simulator
1. Navigate to the project directory:
   ```bash
   cd file-system-simulator
   ```
2. Run the simulator:
   ```bash
   python .
   ```
   On macOS, you may need to use `python3` instead:
   ```bash
   python3 .
   ```

## Running Tests
To ensure the simulator works as expected, you can run the test suite using Python's built-in `unittest` module:

1. Navigate to the `tests` directory:
   ```bash
   cd file-system-simulator/tests
   ```
2. Run all tests:
   ```bash
   python -m unittest discover
   ```
   On macOS, you may need to use `python3`:
   ```bash
   python3 -m unittest discover
   ```

3. Alternatively, run a specific test file:
   ```bash
   python -m unittest test_directory.py
   ```
   Or for macOS:
   ```bash
   python3 -m unittest test_directory.py
   ```


