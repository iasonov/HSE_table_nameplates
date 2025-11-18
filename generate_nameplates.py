#!/usr/bin/env python3
"""
Generator of table nameplates for meetings.
Creates printable PDF with foldable nameplates (A4, folded along long side).
Each nameplate shows the name on both sides and includes a logo.
"""

import argparse
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image


class NameplateGenerator:
    """Generator for creating printable table nameplates."""
    
    def __init__(self, logo_path, font_path, output_path="nameplates.pdf"):
        """
        Initialize the nameplate generator.
        
        Args:
            logo_path: Path to the logo image file
            font_path: Path to the TTF font file
            output_path: Path for the output PDF file
        """
        self.logo_path = logo_path
        self.font_path = font_path
        self.output_path = output_path
        
        # A4 dimensions in points (1 point = 1/72 inch)
        self.page_width, self.page_height = A4
        
        # When folded along the long side, each half is page_height / 2
        self.fold_line = self.page_height / 2
        
        # Logo size (in mm, converted to points)
        self.logo_size = 30 * mm
        
        # Font sizes
        self.font_size_large = 48
        self.font_size_medium = 36
        
        # Register custom font
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('CustomFont', font_path))
            self.font_name = 'CustomFont'
        else:
            print(f"Warning: Font file '{font_path}' not found. Using default Helvetica.")
            self.font_name = 'Helvetica'
    
    def _draw_logo(self, c, x, y, width, height):
        """Draw logo at specified position."""
        if os.path.exists(self.logo_path):
            try:
                c.drawImage(self.logo_path, x, y, width=width, height=height, 
                           preserveAspectRatio=True, mask='auto')
            except Exception as e:
                print(f"Warning: Could not load logo: {e}")
        else:
            print(f"Warning: Logo file '{self.logo_path}' not found.")
    
    def _draw_name(self, c, name, x, y, rotation=0):
        """
        Draw name at specified position with optional rotation.
        
        Args:
            c: Canvas object
            name: Name to draw
            x: X coordinate
            y: Y coordinate
            rotation: Rotation angle in degrees (0 or 180)
        """
        c.saveState()
        
        # Determine font size based on name length
        if len(name) > 30:
            font_size = self.font_size_medium
        else:
            font_size = self.font_size_large
        
        c.setFont(self.font_name, font_size)
        
        # Calculate text width for centering
        text_width = c.stringWidth(name, self.font_name, font_size)
        
        if rotation == 180:
            # For the bottom half (upside down when folded)
            c.translate(x, y)
            c.rotate(rotation)
            c.drawString(-text_width / 2, 0, name)
        else:
            # For the top half (normal orientation)
            c.drawString(x - text_width / 2, y, name)
        
        c.restoreState()
    
    def generate(self, names):
        """
        Generate PDF with nameplates for the given list of names.
        
        Args:
            names: List of names (strings)
        """
        c = canvas.Canvas(self.output_path, pagesize=A4)
        
        for name in names:
            # Top half (visible when folded, right-side up)
            # Logo in top-left corner
            logo_margin = 10 * mm
            self._draw_logo(c, logo_margin, 
                          self.fold_line + logo_margin,
                          self.logo_size, self.logo_size)
            
            # Name centered in top half
            name_y = self.fold_line + (self.page_height - self.fold_line) / 2
            self._draw_name(c, name, self.page_width / 2, name_y)
            
            # Bottom half (visible when folded, upside down - will be right-side up on other side)
            # Logo in bottom-right corner (which will be top-left when flipped)
            logo_x = self.page_width - logo_margin - self.logo_size
            logo_y = self.fold_line - logo_margin - self.logo_size
            self._draw_logo(c, logo_x, logo_y, self.logo_size, self.logo_size)
            
            # Name centered in bottom half, rotated 180 degrees
            name_y_bottom = self.fold_line / 2
            self._draw_name(c, name, self.page_width / 2, name_y_bottom, rotation=180)
            
            # Draw fold line (optional, for debugging)
            # c.setDash(3, 3)
            # c.line(0, self.fold_line, self.page_width, self.fold_line)
            
            # Start new page for next name
            c.showPage()
        
        c.save()
        print(f"Generated nameplates PDF: {self.output_path}")
        print(f"Total pages: {len(names)}")


def read_names_from_file(file_path):
    """
    Read names from a text file (one name per line).
    
    Args:
        file_path: Path to the text file
        
    Returns:
        List of names
    """
    names = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                names.append(line)
    return names


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Generate printable table nameplates for meetings'
    )
    parser.add_argument(
        'names_file',
        help='Path to text file with names (one per line)'
    )
    parser.add_argument(
        'logo',
        help='Path to logo image file (PNG, JPG, etc.)'
    )
    parser.add_argument(
        'font',
        help='Path to TTF font file'
    )
    parser.add_argument(
        '-o', '--output',
        default='nameplates.pdf',
        help='Output PDF file path (default: nameplates.pdf)'
    )
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.names_file):
        print(f"Error: Names file '{args.names_file}' not found.")
        return 1
    
    if not os.path.exists(args.logo):
        print(f"Error: Logo file '{args.logo}' not found.")
        return 1
    
    if not os.path.exists(args.font):
        print(f"Error: Font file '{args.font}' not found.")
        return 1
    
    # Read names from file
    names = read_names_from_file(args.names_file)
    
    if not names:
        print("Error: No names found in the input file.")
        return 1
    
    print(f"Loaded {len(names)} names from {args.names_file}")
    
    # Generate nameplates
    generator = NameplateGenerator(args.logo, args.font, args.output)
    generator.generate(names)
    
    return 0


if __name__ == '__main__':
    exit(main())
