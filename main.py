import re
from pdfminer.high_level import extract_pages, extract_text

text = extract_text("invoicesample.pdf")
# print(text)

pattern = re.compile(r"[a-zA-Z]+,{1}\s{1}")

matches = pattern.findall(text)

# print(matches)
