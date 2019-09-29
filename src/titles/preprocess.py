import re
import string

from .stopwords import get_stopwords

stop = get_stopwords('smart')

tags = re.compile(r"<.*?>")
# nums = re.compile(r"\b[\d]+\b")
punct = re.compile('[%s—]' % re.escape(string.punctuation))
chars = re.compile('[^%s]' % re.escape(string.printable))

def clean(title):
    title = title.strip()
    title = title.lower()
    title = tags.sub("",title)
    # title = nums.sub("",title)
    title = punct.sub(" ",title).strip()
    title = remove_numbers(title)
    title = remove_stopwords(title)
    title = remove_nonascii(title)
    title = remove_short(title)
    title = title.replace("\n", " ")
    title = title.replace("\r", " ")
    title = re.sub(' +', ' ', title)
    title = title.strip()
    return title

def remove_stopwords(title):
    return " ".join([word for word in title.split() if word not in stop])

def remove_short(title):
    return " ".join([word for word in title.split() if len(word) > 2])

def remove_nonascii(title):
    return " ".join([word for word in title.split() if word == chars.sub(" ",word)])

def remove_numbers(title):
    return " ".join([word for word in title.split() if not has_number(word)])

def has_number(word):
    return any(i.isdigit() for i in word)
