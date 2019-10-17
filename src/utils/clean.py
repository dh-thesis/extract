import re

def clean_title(title):
    title = title.strip()
    title = title.replace("\n", " ")
    title = title.replace("\r", " ")
    title = title.replace(",", " ")
    title = title.replace('"', "")
    title = re.sub(r"<.*?>", "", title)  # html tags (e.g. <sub>, </sub>, ...)
    title = re.sub(r"([^\sa-zA-Z]+)?\$.+?\$-?([^\sa-zA-Z]+)?", " ", title) # math expressions
    title = re.sub(r"[^\S]\\[^\s]+", "", title) # latex commands (e.g. \bold)
    title = re.sub(r"[^\s]+\\[^\s]+", "", title) # latex special characters
    title = re.sub(r"\s+", " ", title) # multiple whitespaces
    title.strip()
    return title
