# hatvp-api

hatvp-api is a project to give an access to the lobbying activities from:

https://www.hatvp.fr/le-repertoire/#open-data-repertoire

https://www.infogreffe.fr/entreprise-societe/833718653-storengy-920117B109630000.html?typeProduitOnglet=EXTRAIT&afficherretour=false

## Requirements

- git
- python >= 3.10
- pip
- a database service (postgreSQL recommended)

## How to

1. Clone repository

```sh
$ git clone https://github.com/aboutofpluto/hatvp-api.git
$ cd hatvp-api
```

2. Create virtual environment and install dependencies:

```sh
$ virtualenv -ppython3.10 venv-hatvp
$ source venv-hatvp/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
```

3. Get a copy of the "Vues séparées" files:

```sh
$ wget https://www.hatvp.fr/agora/opendata/csv/Vues_Separees_CSV.zip
$ unzip Vues_Separees_CSV.zip hatvp/
$ mv hatvp/Vues_Separees hatvp/data
```

4. Configure django:

```sh
$ cp lobbyapi/local_settings.py.sample lobbyapi/local_settings.py
```

Edit the DATABASE section to connect to your database service.
See https://docs.djangoproject.com/en/5.2/ref/databases/ for more information

5. Import data:

```sh
$ python manage.py migrate
$ python manage.py import
```


6. Run server

```sh
$ python manage.py createsuperuser
$ python manage.py runserver
```

Then
- connect to localhost:8000/admin
- log in as superuser
- browse!
