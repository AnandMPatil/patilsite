from django.db import models

class Category(models.Model) :
    name = models.CharField(max_length=128)
    site = models.ManyToManyField('Site',through='Manytomany')

    def __str__(self) :
        return self.name

class States(models.Model) :
    name = models.CharField(max_length=128)
    site = models.ManyToManyField('Site',through='Manytomany')

    def __str__(self) :
        return self.name

class Region(models.Model) :
    name = models.CharField(max_length=128)
    site = models.ManyToManyField('Site',through='Manytomany')

    def __str__(self) :
        return self.name

class Iso(models.Model) :
    name = models.CharField(max_length=128)
    #sites = models.ManyToManyField('Site',through='Manytomany')

    def __str__(self) :
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    justification = models.TextField()
    year = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    area_hectares = models.FloatField()
    '''category = models.ManyToManyField('Category',through='Manytomany')
    states = models.ManyToManyField('States',through='Manytomany')
    region = models.ManyToManyField('Region',through='Manytomany')'''
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)

    def __str__(self) :
        return self.name

class Manytomany(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    states = models.ForeignKey(States, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)