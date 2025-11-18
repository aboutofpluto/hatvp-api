import csv, os, zipfile
import urllib.request
from shutil import rmtree
from datetime import datetime

from django.db import models
from django.core.management.base import BaseCommand, CommandError

from hatvp.models import GeneralInformation, Affiliation, Director, Associate
from hatvp.models import Client, Level, Period, Activity, Domain, Field
from hatvp.models import TypeAction, Action, Beneficiary, Decision, Target, Observation

class Command(BaseCommand):
    help = 'Import HATVP data from models and CSV files'

    def import_csv(self, cls):
        ''' 
        From a hatvp model, reads a csv file and find data using
        introspection. The trick is the use of 'verbose_name' as
        the name of the column to retrieve in the file
        '''
        with open(cls.__source__, "rU") as src:
            print("Importing '{}' ".format(cls._meta.object_name), end='')
            reader = csv.reader(src, delimiter=';', quotechar='"')
            header = next(reader)
            cols = {}
            # get column indexes for each column name
            # makes it easy to find data from names
            for pos, label in enumerate(header):
                cols[label] = pos

            cnt = 0
            for row in reader:
                #print(row) # debug

                # prepare a dict for 'update_or_create'
                defaults = {}

                # parse all fields from the model and set them
                for field in cls._meta.fields:
                    # if the field is an AutoField, it is not found
                    # in the CSV file, so ignore it (auto increment)
                    if isinstance(field, models.AutoField):
                        defaults["id"] = None
                        continue
                    # get value in the CSV file
                    value = row[cols[field.verbose_name]]
                    if value:
                        # if the field is a date time, try to
                        # parse it according to the 'manually'
                        # detected formats
                        if isinstance(field, models.DateTimeField):
                            try:
                                defaults[field.attname] = datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
                            except ValueError: # strptime raises a ValueError
                                defaults[field.attname] = datetime.strptime(value, "%Y-%m-%d")
                        # else, simply set the field
                        else:
                            if hasattr(field, "max_length"):
                                defaults[field.attname] = value[:field.max_length]
                            else:
                                defaults[field.attname] = value
                # update or create an instance
                try:
                    cls.objects.update_or_create(defaults, pk=defaults["id"])
                except:
                    print("failure")
                    continue
                cnt += 1
                if cnt % 100:
                    print(".", end='', flush=True)
            print("done {} records".format(cnt))


    def download_and_unzip(self):
        print("Downloading latest HATVP data ... ", )
        local_filename, headers = urllib.request.urlretrieve('https://www.hatvp.fr/agora/opendata/csv/Vues_Separees_CSV.zip')
        print("done")

        print("Unzipping ... ", )
        zip_ref = zipfile.ZipFile(local_filename, 'r')
        zip_ref.extractall('.')
        zip_ref.close()
        print("done")

        print("Cleaning and moving ... ", )
        rmtree("hatvp/data")
        os.rename("Vues séparées", "hatvp/data")
        print("done")


    def handle(self, *args, **options):
        '''
        import data in the correct order
        '''
#        self.download_and_unzip()
        # self.import_csv(GeneralInformation)
        # self.import_csv(Director)
        # self.import_csv(Associate)
        # self.import_csv(Client)
        # self.import_csv(Affiliation)
        # self.import_csv(Level)
        # self.import_csv(Period)
        # self.import_csv(Activity)
        # self.import_csv(Domain)
        # self.import_csv(Field)
        # self.import_csv(Action)
        # self.import_csv(TypeAction)
        # self.import_csv(Beneficiary)
        self.import_csv(Decision)
        self.import_csv(Target)
        self.import_csv(Observation)
