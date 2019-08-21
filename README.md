# Publication Data Extraction

Set Up:

```
git clone https://github.com/dh-thesis/extract.git
cd extract/
virtualenv -p python3 --no-site-packages env
source env/bin/activate
pip install -r requirements.txt
deactivate
```

- [retrieve publication data](https://github.com/dh-thesis/retrieve)
- [crawl metadata of Max Planck Institutes](https://github.com/dh-thesis/crawl)
- start the extraction:

```
./main
```

## Scripts

```
start extraction!
```

#### Organizations

The following scripts are used to find child nodes of organizational units in MPG.PuRe as well as child nodes associated to Max Planck Institutes.

- [src/data_ous.py](./src/data_ous.py)
- [src/data_ous_mpis.py](./src/data_ous_mpis.py)

#### Descriptions

The following script is used to find research domains (`category`) and research areas (`tag`) of Max Planck Institutes given on the website of the Max Planck Society.

- [src/data_desc.py](./src/data_desc.py)

#### Persons

The following script is used to find persons associated to organizational units in MPG.PuRe.

- [src/data_pers.py](./src/data_pers.py)

#### Contexts

The following scripts are used to find contexts of organizational units in MPG.PuRe as well as contexts associated to Max Planck Institutes.

- [src/data_ctx.py](./src/data_ctx.py)
- [src/data_ctx_mpis.py](./src/data_ctx_mpis.py)

#### Items

The following script is used to collect informations about publications, their authors, associated organizational units, publication sources, et cetera.

- [src/data_items.py](./src/data_items.py)

#### Languages

The following script is used to collect informations about languages of publications in MPG.PuRe.

- [src/data_lang.py](./src/data_lang.py)

#### Journals

The following script is used to collect informations about journals in MPG.PuRe.

- [src/data_jour.py](./src/data_jour.py)
