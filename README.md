
# pText

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Corpus Coverage : 97.0%](https://img.shields.io/badge/corpus%20coverage-97.0%25-green)]()
[![Text Extraction : 87.9%](https://img.shields.io/badge/text%20extraction-87.9%25-orange)]()
[![Public Method Documentation : 100%](https://img.shields.io/badge/public%20method%20documentation-100%25-green)]()


pText is a library for creating and manipulating PDF files in python.

## 0. About pText

pText is a pure python library to read, write and manipulate PDF documents. It represents a PDF document as a JSON-like datastructure of nested lists, dictionaries and primitives (numbers, string, booleans, etc)

This is currently a one-man project, so the focus will always be to support those use-cases that are more common in favor of those that are rare.

## 1. About the Examples

Most examples double as tests, you can find them in the 'tests' directory.  
They include; 
- reading a PDF and extracting meta-information
- changing meta-information  
- extracting text from a PDF
- extracting images from a PDF
- changing images in a PDF
- adding annotations (notes, links, etc) to a PDF
- adding text to a PDF
- adding tables to a PDF
- adding lists to a PDF
- using a layout
 and much more
 
### 1.1 Hello World

To give you an immediate idea of the way `pText` works, this is the classic `Hello World` example, in `pText`:

```python
from pathlib import Path

from ptext.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.text.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

# create an empty Document
pdf = Document()

# add an empty Page
page = Page()
pdf.append_page(page)

# use a PageLayout (SingleColumnLayout in this case)
layout = SingleColumnLayout(page)

# add a Paragraph object
layout.add(Paragraph("Hello World!"))

# store the PDF
with open(Path("output.pdf"), "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, pdf)
```
 
## 2. License

pText is dual licensed as AGPL/Commercial software.

AGPL is a free/open source software license.
This doesn't mean the software is [gratis](https://en.wikipedia.org/wiki/Gratis_versus_libre)!

Buying a license is mandatory as soon as you develop commercial activities distributing the pText software inside your product or deploying it on a network without disclosing the source code of your own applications under the AGPL license. 
These activities include:

- offering paid services to customers as an ASP
- serving PDFs on the fly in the cloud or in a web application
- shipping pText with a closed source product

Contact sales for more info.

## 3. Acknowledgements

I would like to thank the following people, for their contributions/advice with regards to developing `pText`:
- Benoît Lagae
- Michael Klink
