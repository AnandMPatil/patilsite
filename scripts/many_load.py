#from django.test import TestCase
import csv
from unesco.models import Category, States, Region, Iso, Site, Manytomany


def run():
    fhand = open('scripts/whc.csv')
    reader = csv.reader(fhand)
    next(reader) # Advance past the header

    Site.objects.all().delete()
    Category.objects.all().delete()
    States.objects.all().delete()
    Region.objects.all().delete()
    Iso.objects.all().delete()
    Manytomany.objects.all().delete()

    for row in reader:
        i, created = Iso.objects.get_or_create(name=row[10])
        i.save()
        if row[6] == '' : row[6] = 0
        si, created = Site.objects.get_or_create(name=row[0],description=row[1],justification=row[2],year=row[3],longitude=row[4],latitude=row[5],area_hectares=row[6],iso=i)
        si.save()
        print(si.id)
        c, created = Category.objects.get_or_create(name=row[7])
        c.save()
        st, created = States.objects.get_or_create(name=row[8])
        st.save()
        r, created = Region.objects.get_or_create(name=row[9])
        r.save()
        mm = Manytomany(site=si,category=c,states=st,region=r,iso=i)
        mm.save()