#!/usr/bin/env python3
"""
Example usage of the nameplate generator as a Python module.
"""

from generate_nameplates import NameplateGenerator

# Example 1: Basic usage
names = [
    "Иванов Иван Иванович",
    "Петрова Мария Сергеевна",
    "Смирнов Дмитрий Александрович"
]

generator = NameplateGenerator(
    logo_path="examples/sample_logo.png",
    font_path="examples/sample_font.ttf",
    output_path="my_nameplates.pdf"
)

generator.generate(names)
print("Generated nameplates successfully!")

# Example 2: Reading from file and using default output name
from generate_nameplates import read_names_from_file

names = read_names_from_file("examples/sample_names.txt")
generator = NameplateGenerator(
    logo_path="examples/sample_logo.png",
    font_path="examples/sample_font.ttf"
)
generator.generate(names)
print("Generated nameplates from file successfully!")
