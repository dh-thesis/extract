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
- start the extraction:

```
./main
```

## Scripts

```
start extraction!
```

#### Contexts

- [src/data_ctx.py](./src/data_ctx.py)
- [src/data_ctx_mpis.py](./src/data_ctx_mpis.py)

#### Organizations

- [src/data_ous.py](./src/data_ous.py)
- [src/data_ous_mpis.py](./src/data_ous_mpis.py)

#### Persons

- [src/data_pers.py](./src/data_pers.py)

#### Items

- [src/data_items.py](./src/data_items.py)

#### Languages

- [src/data_lang.py](./src/data_lang.py)

#### Journals

- [src/data_jour.py](./src/data_jour.py)

#### Descriptions

- [src/data_desc.py](./src/data_desc.py)
