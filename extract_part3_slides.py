import fitz
import os

pdf_path = "materials/slides/Part 3.pdf"
out_dir = "materials/images/part3_slides"

os.makedirs(out_dir, exist_ok=True)
doc = fitz.open(pdf_path)

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    pix.save(os.path.join(out_dir, f"p3_slide_{(i+1):02d}.png"))
    
print(f"Extracted {len(doc)} slides")
