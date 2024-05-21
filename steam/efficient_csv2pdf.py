import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from tqdm import tqdm
import time

# Function to create PDF from a batch of data
def create_pdf(batch_data, batch_number):
    print(f"Creating PDF for batch {batch_number}")
    doc = SimpleDocTemplate(f'/Users/maniksinghsarmaal/Downloads/Frameworks/Scrapy/Advanced_Scrapy/steam/steam_bestsellers_batch_{batch_number}.pdf', pagesize=letter)
    elements = []

    for entry in batch_data:
        headline = Paragraph(entry['game_name'], headline_style)
        elements.append(headline)
        elements.append(Spacer(1, 12))  # Add vertical spacing

        # Commenting out the image part to test the speed
        # img_url = entry['img_url']
        # try:
        #     img = Image(img_url, width=1.5*inch, height=1.5*inch)  # Adjust image size as needed
        #     elements.append(img)
        #     elements.append(Spacer(1, 12))
        # except Exception as e:
        #     print(f"Error loading image: {img_url} - {e}")

        game_url = f"<a href='{entry['game_url']}'>{entry['game_url']}</a>"
        url_paragraph = Paragraph(game_url, content_style)
        elements.append(url_paragraph)
        elements.append(Spacer(1, 12))  # Add vertical spacing

        release_date = Paragraph(f"Release Date: {entry['release_date']}", content_style)
        elements.append(release_date)
        elements.append(Spacer(1, 12))  # Add vertical spacing

        final_price = Paragraph(f"Price: {entry['final_price']}", content_style)
        elements.append(final_price)
        elements.append(Spacer(1, 12))  # Add vertical spacing

        reviews_summary = Paragraph(f"Reviews: {entry['reviews_summary']}", content_style)
        elements.append(reviews_summary)
        elements.append(Spacer(1, 24))  # Add more spacing between entries

    doc.build(elements)
    print(f"Completed PDF for batch {batch_number}")

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

# Process data in batches
batch_size = 1000  # Reduce the batch size
start_time = time.time()
for i in tqdm(range(0, len(data), batch_size), desc="Processing batches"):
    batch_data = data[i:i + batch_size]
    create_pdf(batch_data, i // batch_size)

# Calculate total time taken
end_time = time.time()
print(f"Total time taken: {end_time - start_time} seconds")
