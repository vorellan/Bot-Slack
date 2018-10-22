from django.db import models
from django.utils import timezone

class Cliente(models.Model):

    id = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=50)


class Menu(models.Model):

    opcion1 = models.CharField(max_length=200)
    opcion2 = models.CharField(max_length=200)
    opcion3 = models.CharField(max_length=200)
    opcion4 = models.CharField(max_length=200)
    fecha = models.DateTimeField()


class Agenda(models.Model):

    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    opcion = models.IntegerField(null=False)
    especificacion = models.CharField(max_length=500)

