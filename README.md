# HSE Table Nameplates Generator

Generator of table nameplates for meetings, printed on A4 paper.

## Description

This Python script generates printable PDF files with foldable table nameplates. Each A4 sheet contains a nameplate that can be folded along the long side to create a double-sided standing name tag for meetings and conferences.

## Features

- **Foldable Design**: Each sheet is designed to be folded along the horizontal center line
- **Double-sided Names**: Name appears on both sides when folded (readable from both directions)
- **Custom Logo**: Logo image placed in the corner of each nameplate
- **Custom Font**: Support for custom TTF fonts (important for Cyrillic and other non-Latin scripts)
- **Batch Processing**: Process multiple names at once
- **PDF Output**: Ready-to-print PDF format

## Requirements

- Python 3.6+
- Pillow (for image handling)
- ReportLab (for PDF generation)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/iasonov/HSE_table_nameplates.git
cd HSE_table_nameplates
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python generate_nameplates.py <names_file> <logo_image> <font_file> [-o output.pdf]
```

### Arguments

- `names_file`: Path to a text file containing names (one name per line)
- `logo_image`: Path to the logo image file (PNG, JPG, etc.)
- `font_file`: Path to a TTF font file
- `-o, --output`: (Optional) Output PDF file path (default: `nameplates.pdf`)

### Example

```bash
python generate_nameplates.py examples/sample_names.txt examples/sample_logo.png examples/sample_font.ttf -o my_nameplates.pdf
```

### Input File Format

The names file should be a plain text file with one name per line:

```
Иванов Иван Иванович
Петрова Мария Сергеевна
Сидоров Алексей Дмитриевич
```

## How It Works

1. **Layout**: Each A4 page (210mm × 297mm) is divided horizontally in half
2. **Top Half**: Contains the name and logo (visible when standing upright)
3. **Bottom Half**: Contains the name (rotated 180°) and logo (will be visible from the other side when folded)
4. **Folding**: Fold the paper along the long side (horizontal center line) to create a standing nameplate

```
┌─────────────────────────────┐
│  LOGO      NAME             │  ← Top (front when folded)
├─────────────────────────────┤  ← Fold line
│             NAME      LOGO  │  ← Bottom (back when folded, upside-down)
└─────────────────────────────┘
```

## Sample Files

The `examples/` directory contains sample files to help you get started:

- `sample_names.txt`: Example list of names
- `sample_logo.png`: Example logo image
- `sample_font.ttf`: Example TrueType font (Liberation Sans Bold)

## Tips

- **Font Selection**: Choose a TTF font that supports the characters in your names (e.g., Cyrillic for Russian names)
- **Logo Size**: The logo is automatically resized to 30mm × 30mm while preserving aspect ratio
- **Name Length**: Font size automatically adjusts for longer names
- **Printing**: Print the PDF at actual size (100% scale, no fit-to-page) for correct dimensions

## Customization

You can customize the script by modifying these parameters in the `NameplateGenerator` class:

- `logo_size`: Size of the logo (default: 30mm)
- `font_size_large`: Font size for normal names (default: 48pt)
- `font_size_medium`: Font size for long names (default: 36pt)

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
