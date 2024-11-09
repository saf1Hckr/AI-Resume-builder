# import markdown
# from fpdf import FPDF
# import pdfkit  # or use weasyprint as an alternative
#
# # Function to read the .txt file and convert markdown to HTML
# def convert_markdown_to_html(file_path):
#     with open(file_path, 'r') as file:
#         markdown_text = file.read()
#     html_content = markdown.markdown(markdown_text)
#     return html_content
#
# # Function to convert HTML to PDF using pdfkit
# def convert_html_to_pdf(html_content, output_pdf):
#     # Use pdfkit to convert HTML to PDF
#     pdfkit.from_string(html_content, output_pdf)
#
# # Main function to read .txt file, convert it, and generate PDF
# def markdown_to_pdf(input_txt, output_pdf):
#     html_content = convert_markdown_to_html(input_txt)
#     convert_html_to_pdf(html_content, output_pdf)
#     print(f"PDF generated successfully and saved as {output_pdf}")
#
# # Input and Output paths
# input_txt = "hk99.md"  # Your Markdown file (could be a .txt file with Markdown content)
# output_pdf = "Error404.pdf"  # Desired output PDF file
#
# # Convert Markdown file to PDF
# markdown_to_pdf(input_txt, output_pdf)

# import markdown
# import pdfkit
#
# def convert_markdown_to_html(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         markdown_text = file.read()
#     html_content = markdown.markdown(markdown_text)
#     return html_content
#
# def convert_html_to_pdf(html_content, output_pdf):
#     # Configure options to ensure UTF-8 encoding and compatible font handling
#     options = {
#         'encoding': 'UTF-8',
#         'no-outline': None,
#     }
#     pdfkit.from_string(html_content, output_pdf, options=options)
#
# # Main function
# input_txt = "hk99.md"
# output_pdf = "CorrectedOutput.pdf"
# html_content = convert_markdown_to_html(input_txt)
# convert_html_to_pdf(html_content, output_pdf)
# print(f"PDF generated successfully and saved as {output_pdf}")

import markdown
import pdfkit

# CSS styling to format PDF output
css = """
body {
    font-size: 12px;
    font-family: Arial, sans-serif;
    line-height: 1.5; /* Increases readability */
}

ul, li {
    margin: 0;
    padding-left: 1em;
    list-style-type: disc;
}

li {
    margin-bottom: 10px; /* Adds space between list items */
    text-indent: -1em; /* Ensures bullet points align properly */
}

ul ul {
    list-style-type: disc; /* Keeps nested lists as bullet points */
    padding-left: 1.5em; /* Adds indentation for nested lists */
}
"""


# Convert Markdown to HTML
def convert_markdown_to_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_text = file.read()
    html_content = markdown.markdown(markdown_text)
    return f"<style>{css}</style>{html_content}"

# Convert HTML to PDF
def convert_html_to_pdf(html_content, output_pdf):
    options = {
        'encoding': 'UTF-8',
        'page-size': 'Letter',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm'
    }
    pdfkit.from_string(html_content, output_pdf, options=options)

# File paths
input_txt = "rialhk10.md"                   # "hk99.md"
output_pdf = "fk10.pdf"                     # "cv100.pdf"

html_content = convert_markdown_to_html(input_txt)
convert_html_to_pdf(html_content, output_pdf)
print(f"PDF generated successfully and saved as {output_pdf}")



