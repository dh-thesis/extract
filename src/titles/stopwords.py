import os

dirname, filename = os.path.split(os.path.abspath(__file__))
resources = os.path.join(dirname, 'resources/')


def read_wordlist(fpath):
    with open(fpath, 'r') as fp:
        return [line.strip() for line in fp.readlines()]


def get_wordslist(fname):
    path = os.path.join(resources, fname)
    return read_wordlist(path)


def get_smart(fname='smart--stopwords-en.txt'):
    return get_wordslist(fname)


def get_edit(fname='editorial--stopwords-en.txt'):
    return get_wordslist(fname)


def get_stopwords(words='smart'):
    if words == 'smart':
        stop = get_smart()
        stop.extend(get_edit())
        return stop
    else:
        print("implement me!")
        return []
