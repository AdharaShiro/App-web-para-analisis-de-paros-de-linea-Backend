import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password


class LoginUser(models.Model):
    nombre = models.CharField(max_length=50)
    password = models.CharField(max_length=255) 

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre



class Usuario(models.Model):
    idUser = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    position = models.CharField(max_length=20)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return f"{self.username} {self.lastname}"

#self  es una referencia al propio objeto de la clase
#raw_password es un parámetro del método set_password. 
# Es la contraseña sin encriptar que el usuario proporciona.

class Modelo(models.Model):
    idModelo = models.CharField(max_length=100, primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.idModelo

class Turno(models.Model):
    idTurno = models.AutoField(primary_key=True)
    Turno = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f'{self.Turno}: {self.hora_inicio} - {self.hora_fin}'
    

class Linea(models.Model):
    idLinea = models.CharField(max_length=100, primary_key=True)
    linea = models.CharField(max_length=100)

    def __str__(self):
        return self.linea



    
class Descripciones(models.Model):
    Descripcion = models.CharField(max_length=100)
    idDescripcion= models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.Descripcion


class Departamento(models.Model):
    idDepartamento = models.CharField(max_length=100, primary_key=True)
    departamento = models.CharField(max_length=100)

    def __str__(self):
        return self.departamento

class Subdepartamento(models.Model):
    idSub = models.CharField(max_length=100, primary_key=True)
    subdepartamento = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='subdepartamentos')

    def __str__(self):
        return f"{self.subdepartamento}"
  
class Produccion(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE) #Forzosamente es el id del modelo 
    fecha = models.DateField(default=datetime.date.today)  
    tiempo_inicio = models.TimeField()
    tiempo_fin = models.TimeField()
    golpes = models.IntegerField()
    pieza_por_golpe = models.IntegerField()
    piezas_ok = models.IntegerField()
    turno = models.CharField(max_length=20, choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Nocturno', 'Nocturno')])  
    linea = models.CharField(max_length=50, null=True, blank=True)  


class Paro(models.Model):
    departamento = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    observaciones = models.TextField(default='Sin observaciones')  # Proveer un valor por defe
    duracion = models.IntegerField(default=0)
    turno = models.CharField(max_length=20, choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Nocturno', 'Nocturno')])  
    linea = models.CharField(max_length=50, null=True, blank=True)  # Nuevo campo para la línea de producción


    def __str__(self):
        return f"{self.departamento} - {self.descripcion}"



class SlitterProduccion(models.Model):
    modelo = models.CharField(max_length=100)  # Almacena el nombre del modelo
    fecha = models.DateField(default=datetime.date.today)
    tiempo_inicio = models.TimeField()
    tiempo_fin = models.TimeField()
    kilos_ok = models.IntegerField()
    cintas = models.IntegerField()
    master_coils = models.IntegerField()
    hmc = models.IntegerField()
    gw = models.IntegerField()
    ancho = models.IntegerField()
    turno = models.CharField(max_length=20, choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Nocturno', 'Nocturno')])

class SlitterParo(models.Model):
    departamento = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    observaciones = models.TextField(default='Sin observaciones')
    duracion = models.IntegerField(default=0)
    turno = models.CharField(max_length=20, choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Nocturno', 'Nocturno')])

    def __str__(self):
        return f"{self.departamento} - {self.descripcion}"
    


    
class OsiladoraProduccion(models.Model):
    modelo = models.CharField(max_length=100)  # Almacena el nombre del modelo
    fecha = models.DateField(default=datetime.date.today)
    tiempo_inicio = models.TimeField()
    tiempo_fin = models.TimeField()
    kilos_ok = models.IntegerField()
    cintas = models.IntegerField()
    rollo_osilados = models.IntegerField()
    turno = models.CharField(max_length=20, choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Nocturno', 'Nocturno')])

class OsiladoraParo(models.Model):
    departamento = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    observaciones = models.TextField(default='Sin observaciones')
    duracion = models.IntegerField(default=0)
    turno = models.CharField(max_length=20, choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Nocturno', 'Nocturno')])

    def __str__(self):
        return f"{self.departamento} - {self.descripcion}"
