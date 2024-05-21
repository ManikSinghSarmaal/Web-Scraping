from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import json

# Load the JSON file
with open('bizznews.json', 'r') as f:
    data = json.load(f)

# Convert the JSON data to a list of lists for the table
table_data = [["Headline", "Content", "Author", "Date", "Source URL", "Source Name"]]
for article in data:
    table_data.append([
        article["headline"],
        article["content"],
        article["author"],
        article["date"],
        article["source_url"],
        article["source_name"]
    ])

# Create a PDF document
pdf_filename = "output.pdf"
pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
table = Table(table_data)

# Define table style
table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
])

# Apply table style
table.setStyle(table_style)

# Get the width of each column dynamically
column_widths = [max([len(str(row[i])) for row in table_data]) * 12 for i in range(len(table_data[0]))]
table._argW = column_widths

# Add the table to the PDF document
pdf.build([table])

print(f"PDF generated successfully: {pdf_filename}")
