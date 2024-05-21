import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Parse CSV data
data = []
with open('/Users/maniksinghsarmaal/Downloads/Frameworks/Scrapy/inshorts_scrapy/inshort_business/inshort_business/20May2024.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

# Set up PDF document and styles
styles = getSampleStyleSheet()
headline_style = styles['Heading1']
content_style = styles['BodyText']
content_style.wordWrap = 'CJK'  # Enable word wrapping for content

doc = SimpleDocTemplate('20May2024_BigDATA.pdf', pagesize=letter)
elements = []

# Add content to the PDF
for entry in data:
    headline = Paragraph(entry['headline'], headline_style)
    elements.append(headline)
    elements.append(Spacer(1, 12))  # Add vertical spacing

    content = Paragraph(entry['content'], content_style)
    elements.append(content)
    elements.append(Spacer(1, 24))  # Add more spacing between entries

# Build the PDF
doc.multiBuild(elements)