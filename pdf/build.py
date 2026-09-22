#!/usr/bin/env python3
"""Build PDF snapshots for volumes whose issues are all closed and content proven.

Usage: python3 build.py
Generates per-page PDFs plus a merged complete-volume PDF in this directory.
Only volumes that pass the qualification check (see README.md) are built.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp_print import html_to_pdf
from pypdf import PdfWriter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDFDIR = os.path.dirname(os.path.abspath(__file__))

# Qualified volumes: (slug, [(pdf_name, html_relpath), ...]) in merge order.
VOLUMES = {
    "volume-0": [
        ("volume-0-overview", "vol0/index.html"),
        ("volume-0-book20", "book20/index.html"),
        ("volume-0-book21", "book21/index.html"),
        ("volume-0-book22", "book22/index.html"),
    ],
}

def main():
    for slug, pages in VOLUMES.items():
        print(f"== {slug} ==")
        made = []
        for pdf_name, rel in pages:
            src = os.path.join(REPO, rel)
            dst = os.path.join(PDFDIR, pdf_name + ".pdf")
            size = html_to_pdf(src, dst)
            made.append(dst)
            print(f"  {pdf_name}.pdf  {size} bytes  <- {rel}")
        merged = os.path.join(PDFDIR, slug + "-complete.pdf")
        merger = PdfWriter()
        for p in made:
            merger.append(p)
        merger.write(merged)
        merger.close()
        print(f"  {slug}-complete.pdf  {os.path.getsize(merged)} bytes (merged)")

if __name__ == "__main__":
    main()
