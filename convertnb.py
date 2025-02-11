
from nbconvert import PDFExporter, LatexExporter, WebPDFExporter, HTMLExporter
import nbformat

# Load the notebook
with open('./public/notebooks/Chapter_4_Communities.ipynb') as f:
    notebook_content = nbformat.read(f, as_version=4)

# Convert
# exporter = LatexExporter(template_file='custom_template.tpl')
exporter = LatexExporter()
data, resources = exporter.from_notebook_node(notebook_content)

# Save the PDF to a file
with open('./public/textbook.tex', 'wb') as f:
    f.write(str.encode(data))

with open('./public/textbook.tex', 'wb') as f:
    f.write(str.encode(data))

