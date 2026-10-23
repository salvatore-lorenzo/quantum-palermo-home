QUNIPA LOGO PACKAGE v1.1  (wordmark letters u n i a set in Audiowide)

QuniPa_MASTER_horizontal_color.svg   master vector (primary logo, full colour)
QuniPa_Logo_Guidelines.pdf           usage guidelines (clear space, sizes, colour, type, do/don't, draft-to-final notes)
COLOR_SPECIFICATIONS.txt             HEX / RGB / CMYK, typefaces, sizes
logos/<layout>/vector/               SVG, PDF, EPS (RGB, for screen/office use)
logos/<layout>/png/                  transparent PNGs, 3000-4000 px
logos/<layout>/print-cmyk/           CMYK PDF + EPS (full colour, grayscale, black)
web-icons/                           favicon.ico/.svg, PNG ladder 16-512, touch icon, social avatars
source/                              parametric build scripts (python3 build_logo.py) + fonts and OFL licences

Layouts: horizontal, horizontal-descriptor, stacked, emblem, emblem-compact, monogram, wordmark
Variants: color, color-on-dark, gray, gray-on-dark, black, white
File names: qunipa_<layout>_<variant>.<ext>   (CMYK files end _CMYK)
Files are trimmed to the artwork with a 0.5% hairline margin; that margin is NOT the clear space.
The descriptor text "RESEARCH GROUP" is a placeholder (edit in source/build_logo.py).
Rebuild: cd source && python3 build_logo.py && python3 build_icons.py (needs cairosvg, reportlab, fonttools, pillow).
