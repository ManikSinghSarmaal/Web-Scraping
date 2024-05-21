import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Parse CSV data
data = []
with open('/Users/maniksinghsarmaal/Downloads/Frameworks/Scrapy/Advanced_Scrapy/steam/steam/steam_best_sellers.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

# Set up PDF document and styles
styles = getSampleStyleSheet()
headline_style = styles['Heading1']
content_style = styles['BodyText']
content_style.wordWrap = 'CJK'  # Enable word wrapping for content

doc = SimpleDocTemplate('/Users/maniksinghsarmaal/Downloads/Frameworks/Scrapy/Advanced_Scrapy/steam/steam_bestsellers_ALL.pdf', pagesize=letter)
elements = []

# Add content to the PDF
for entry in data:
    # Add game name as the headline
    headline = Paragraph(entry['game_name'], headline_style)
    elements.append(headline)
    elements.append(Spacer(1, 12))  # Add vertical spacing

    # Add game image
    img_url = entry['img_url']
    img_link = f"<a href='{img_url}' color='blue'>{img_url}</a>"
    img_paragraph = Paragraph(img_link, content_style)
    elements.append(img_paragraph)
    elements.append(Spacer(1, 12))  # Add vertical spacing

    # Add game URL
    game_url = f"<a href='{entry['game_url']}'>{entry['game_url']}</a>"
    url_paragraph = Paragraph(game_url, content_style)
    elements.append(url_paragraph)
    elements.append(Spacer(1, 12))  # Add vertical spacing

    # Add release date
    release_date = Paragraph(f"Release Date: {entry['release_date']}", content_style)
    elements.append(release_date)
    elements.append(Spacer(1, 12))  # Add vertical spacing

    # Add final price
    final_price = Paragraph(f"Price: {entry['final_price']}", content_style)
    elements.append(final_price)
    elements.append(Spacer(1, 12))  # Add vertical spacing

    # Add review summary
    reviews_summary = Paragraph(f"Reviews: {entry['reviews_summary']}", content_style)
    elements.append(reviews_summary)
    elements.append(Spacer(1, 24))  # Add more spacing between entries

# Build the PDF
doc.build(elements)
