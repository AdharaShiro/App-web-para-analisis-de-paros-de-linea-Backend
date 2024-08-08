# serializers.py Aquí, UsuarioSerializer convierte los objetos Usuario en representaciones JSON y viceversa. 
 #API RESTful, los datos generalmente se envían y reciben en formato JSON o XML a través de solicitudes HTTP
#Envia datos a travez de una red  en formato json, valida datos de entrada 

from django.contrib.auth import authenticate # type: ignore
from rest_framework import serializers # type: ignore
from .models import OsiladoraParo, OsiladoraProduccion, SlitterParo, SlitterProduccion, Usuario, Modelo, Linea,Descripciones, Departamento, Subdepartamento,Turno,Produccion,Paro

class LoginFormSerializer(serializers.Serializer):
    Nombre = serializers.CharField()
    Linea = serializers.CharField()
    date = serializers.DateField()
    turno = serializers.CharField()
    password1 = serializers.CharField()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['idUser', 'username', 'lastname', 'position', 'password']


class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = ['idModelo', 'nombre']
        

class LineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linea
        fields = ['idLinea', 'linea']

class DescripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descripciones
        fields = ['idDescripcion', 'Descripcion']

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['idDepartamento', 'departamento']
        
class SubdepartamentoSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)

    class Meta:
        model = Subdepartamento
        fields = ['idSub', 'subdepartamento', 'departamento', 'departamento_nombre']

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ['idTurno', 'Turno', 'hora_inicio', 'hora_fin']

class ProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produccion
        fields = '__all__'

class ParoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paro
        fields = '__all__'

class SlitterProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlitterProduccion
        fields = '__all__'

class SlitterParoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlitterParo
        fields = '__all__'

class OsiladoraProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OsiladoraProduccion
        fields = '__all__'

class OsiladoraParoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OsiladoraParo
        fields = '__all__'