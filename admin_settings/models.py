from django.db import models

# Modelo de Country
class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Countries'

#Modelo de lenguaje
class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Languages'