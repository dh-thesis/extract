import re

latex = re.compile(r"\\bold|\\widehat|\\overline|\\times|\\sqrt|\\log|\\rightarrow|\\vert|\\Bbb")

def clean_title(title):
    title = title.strip()
    title = title.replace("\n", " ")
    title = title.replace("\r", " ")
    title = title.replace(",", " ")
    title = title.replace('"', "")
    title = latex.sub("", title)
    title = re.sub(r"<.*?>", "", title)  # html tags (e.g. <sub>, </sub>, ...)
    title = re.sub(r"\s+", " ", title) # multiple whitespaces
    title.strip()
    return title
