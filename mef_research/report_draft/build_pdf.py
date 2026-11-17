"""Render the rough-draft report HTML to PDF with PyMuPDF."""
from pathlib import Path

import fitz

HERE = Path(__file__).parent
html = (HERE / "jamali_mef_report_draft.html").read_text(encoding="utf-8")
out = HERE / "jamali_mef_report_draft.pdf"

story = fitz.Story(html=html)
writer = fitz.DocumentWriter(str(out))
page = fitz.paper_rect("a4")
content = page + (50, 50, -50, -50)

more = True
while more:
    dev = writer.begin_page(page)
    more, _ = story.place(content)
    story.draw(dev)
    writer.end_page()
writer.close()

doc = fitz.open(out)
for i, p in enumerate(doc, 1):
    p.insert_text((page.width - 90, page.height - 25), f"Page {i} of {len(doc)}", fontsize=8, color=(0.4, 0.4, 0.4))
    p.insert_text((50, page.height - 25), "ROUGH DRAFT - Jamali MEF readiness", fontsize=8, color=(0.4, 0.4, 0.4))
doc.saveIncr()
print(out, len(doc), "pages")
