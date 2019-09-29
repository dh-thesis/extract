import re

def clean_title(title):
    title = title.strip()
    title = title.replace("\n", " ")
    title = title.replace("\r", " ")
    title = title.replace(",", " ")
    title = title.replace('"', "")
    title = title.replace("<sup>", "")
    title = title.replace("</sup>", "")
    title = title.replace("</sub>", "")
    title = title.replace("<sub>", "")
    title = re.sub(' +', ' ', title)
    return title
