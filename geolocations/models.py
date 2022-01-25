from django.db import models


class Geolocation(models.Model):
    ip_address = models.CharField(verbose_name='Adres IP', max_length=39, unique=True)
    continent_name = models.CharField(verbose_name='Nazwa kontynentu', max_length=20, blank=True, default='')
    country_name = models.CharField(verbose_name='Nazwa kraju', max_length=56, blank=True, default='')
    region_name = models.CharField(verbose_name='Nazwa regionu', max_length=200, blank=True, default='')
    city = models.CharField(verbose_name='Miasto', max_length=200, blank=True, default='')
    zip = models.CharField(verbose_name='Kod pocztowy', max_length=10, blank=True, default='')
    latitude = models.DecimalField(
        verbose_name='Szerokość geograficzna',
        max_digits=17,
        decimal_places=14,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        verbose_name='Wysokość geograficzna',
        max_digits=17,
        decimal_places=14,
        blank=True,
        null=True,
    )
    languages = models.ManyToManyField(
        'Language',
        verbose_name='Język/Języki',
        related_name='related_geolocations',
        blank=True
    )

    class Meta:
        verbose_name = 'Geolokalizacja'
        verbose_name_plural = 'Geolokalizacje'

    def __str__(self):
        return self.ip_address


class Language(models.Model):
    code = models.CharField(verbose_name='Kod języka', max_length=3, blank=True, default='')
    name = models.CharField(verbose_name='Nazwa języka', max_length=60, blank=True, default='')
    native = models.CharField(verbose_name='Język rdzenny', max_length=60, blank=True, default='')

    class Meta:
        verbose_name = 'Język'
        verbose_name_plural = 'Języki'

    def __str__(self):
        return f'{self.name} [{self.native}, {self.code}]'
