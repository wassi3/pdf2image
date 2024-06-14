# pdf2image.py

pdf2image.py is a Python script that extracts images from PDF files and stores them in a subfolder named after the PDF file. It uses `pdfimages` (from Poppler-utils) and ImageMagick's `convert` tool for processing.

## Features

- Extracts images from PDF files.
- Stores extracted images in a subfolder named after the PDF file.
- Supports merging images with masks using various composition modes.

## Requirements

- Python 3.x
- `Pillow` library
- `pdfimages` from Poppler-utils
- ImageMagick

## Installation

1. **Install Python**:
   Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install Pillow**:
   Install the Pillow library using pip:
   ```bash
   pip install Pillow

## Execution

- git clone (this repo)
- cd (this repo)
- python pdf2image.py path/to/your/pdf/file.pdf

