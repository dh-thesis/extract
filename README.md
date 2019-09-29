# Data Extraction

Prerequisites:

- [retrieve publication data](https://github.com/dh-thesis/retrieve)
- [crawl metadata of Max Planck Institutes](https://github.com/dh-thesis/crawl)

Set Up:

```
git clone https://github.com/dh-thesis/extract.git
cd extract/
virtualenv -p python3 --no-site-packages env
source env/bin/activate
pip install -r requirements.txt
deactivate
```

Start the extraction:

```
./main
```
