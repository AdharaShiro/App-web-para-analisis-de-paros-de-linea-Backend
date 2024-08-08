import json
from urllib import request
from venv import logger
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect,csrf_exempt 
from django.contrib.auth import  logout
from .reports.utils import generar_reporte_por_turno, generar_reporte_excel
from django.contrib.auth.models import User
from .models import Departamento, LoginUser, Subdepartamento, Usuario, Modelo,Linea,Descripciones,Turno,Paro,Produccion
from .serializers import DepartamentoSerializer, OsiladoraParoSerializer, OsiladoraProduccionSerializer, SlitterParoSerializer, SlitterProduccionSerializer, SubdepartamentoSerializer, UsuarioSerializer, ModeloSerializer, LineaSerializer,DescripcionSerializer,ParoSerializer,ProduccionSerializer
from django.http import JsonResponse
from .models import Usuario
from rest_framework.parsers import JSONParser

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_csrf_token(request): # Crea una respuesta JSON que contiene el token CSRF obtenido
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


def csrf_token_view(request): # se utiliza para obtener el token CSRF 
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('idUser')
            password = data.get('password')
            linea = data.get('lineName')  # Cambiado a lineName para coincidir con el nombre en el frontend

            if not user_id or not password or not linea:
                return JsonResponse({"message": "Número de empleado, contraseña y línea de producción son requeridos"}, status=400)

            try:
                user = Usuario.objects.get(idUser=user_id)
            except Usuario.DoesNotExist:
                return JsonResponse({"message": "Credenciales inválidas"}, status=401)

            if check_password(password, user.password):
                # Guardar la línea de producción en la sesión
                request.session['linea'] = linea
                print(f"Línea guardada en la sesión: {request.session['linea']}")  # Depuración
                token = get_token(request)
                return JsonResponse({"message": "Inicio de sesión exitoso", "token": token, "position": user.position}, status=200)
            else:
                return JsonResponse({"message": "Credenciales inválidas"}, status=401)
              
        except json.JSONDecodeError:
            return JsonResponse({"message": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Solo se permiten solicitudes POST"}, status=405)




@csrf_protect
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Cierre de sesión exitoso'}, status=200)
    return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_protect
def user_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'username': request.user.username}, status=200)
    return JsonResponse({'message': 'No autenticado'}, status=401)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
# Crea un nuevo usuario en la base de datos con los datos proporcionados

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            idUser = data.get('idUser')
            username = data.get('username')
            lastname = data.get('lastname')
            position = data.get('position')
            password = data.get('password')

            # Validación básica
            if not (username and lastname and position and password):
                return JsonResponse({'error': 'Todos los campos son requeridos'}, status=400)
                
               # Verificación de duplicados
            if Usuario.objects.filter(idUser=idUser).exists():
                return JsonResponse({'error': 'El ID de usuario ya está en uso'}, status=400)

            # Creación del usuario
            user = Usuario.objects.create(
                idUser=idUser,
                username=username,
                lastname=lastname,
                position=position,
                password=make_password(password)  # Hashea la contraseña antes de guardarla a la base de datos # Recuerda hashear la ión
            )

            return JsonResponse({'message': 'Usuario creado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

# Obtiene un usuario por su nombre de usuario
@csrf_protect
def get_user_by_username(username):
    return Usuario.objects.get(username=username)

@csrf_protect
# Obtiene todos los usuarios que tienen una posición específica
def get_users_by_position(position):
    return Usuario.objects.filter(position=position)


@csrf_exempt
def update_user(request):
    if request.method == 'PUT':
        try:
            # Recibir los datos del cuerpo de la solicitud PUT
            data = json.loads(request.body)
            current_id = data.get('currentIdUser')
            user = get_object_or_404(Usuario, idUser=current_id)

            new_idUser = data.get('idUser', user.idUser)
            new_username = data.get('username', user.username)
            new_lastname = data.get('lastname', user.lastname)
            new_position = data.get('position', user.position)
            new_password = data.get('password')

            # Verificar si new_idUser ya existe en otro usuario
            if new_idUser != user.idUser and Usuario.objects.filter(idUser=new_idUser).exclude(id=user.id).exists():
                return JsonResponse({'error': 'El ID de usuario ya está en uso.'}, status=400)
                
            user.idUser = new_idUser
            user.username = new_username
            user.lastname = new_lastname
            user.position = new_position

            if new_password:
                user.password = make_password(new_password)  # Hashear la nueva contraseña


            # Guardar el usuario si hubo cambios
            user.save()

            # Devolver una respuesta exitosa
            return JsonResponse({'message': f'Datos del usuario "{user.username}" actualizados correctamente.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Si no es una solicitud PUT, devolver un error de método no permitido
        return JsonResponse({'error': 'Método HTTP no permitido'}, status=405)



@csrf_exempt
def delete_user(request, id):
    if request.method == 'DELETE':
        try:
            # Verificar si el usuario existe
            user = Usuario.objects.get(idUser=id)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': f'El usuario con ID {id} no existe.'}, status=404)

        # Eliminar el usuario
        user.delete()

        # Devolver una respuesta exitosa
        return JsonResponse({'message': f'Usuario {user.username} {user.lastname} eliminado exitosamente.'}, status=200)
    else:
        return JsonResponse({"message": "Solo se permiten solicitudes DELETE"}, status=405)
    

# Obtiene la información de un usuario por su ID y la devuelve en formato JSON
@csrf_protect
def ListUser(request, user_id=None):
    if user_id is not None:  # Si se proporciona un user_id en la URL
        try:
            user = Usuario.objects.get(idUser = user_id)
            serializer = UsuarioSerializer(user)
            return JsonResponse(serializer.data)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no existe'}, status=404)
    else:  # Si no se proporciona user_id, devolver la lista de todos los usuarios+
        
        users = Usuario.objects.all()
        serializer = UsuarioSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Apartir de aqui empieza el crud de Modelos 


@csrf_exempt
def create_modelo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            idModelo = data.get('idModelo')
            nombre = data.get('nombre')

            if not idModelo or not nombre:
                return JsonResponse({'error': 'El ID de modelo y el nombre son requeridos'}, status=400)

            if Modelo.objects.filter(idModelo=idModelo).exists():
                return JsonResponse({'error': 'El ID de modelo ya está en uso.'}, status=400)

            modelo = Modelo.objects.create(idModelo=idModelo, nombre=nombre)
            return JsonResponse({'message': 'Modelo creado exitosamente', 'modelo': ModeloSerializer(modelo).data}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def update_modelo(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            current_idModelo = data.get('current_idModelo')
            modelo = get_object_or_404(Modelo, idModelo=current_idModelo)

            new_idModelo = data.get('idModelo', current_idModelo)
            new_nombre = data.get('nombre', modelo.nombre)

            if new_idModelo != current_idModelo:
                if Modelo.objects.filter(idModelo=new_idModelo).exclude(id=modelo.id).exists():
                    return JsonResponse({'error': 'El nuevo ID de modelo ya está en uso.'}, status=400)
                modelo.idModelo = new_idModelo

            if new_nombre != modelo.nombre:
                modelo.nombre = new_nombre

            modelo.save()
            return JsonResponse({'message': f'Modelo "{modelo.idModelo}" actualizado correctamente.', 'modelo': ModeloSerializer(modelo).data}, status=200)
        except Modelo.DoesNotExist:
            return JsonResponse({'error': f'El modelo con ID {current_idModelo} no existe.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def delete_modelo(request, id):
    if request.method == 'DELETE':
        try:
            modelo = Modelo.objects.get(idModelo=id)
            modelo.delete()
            return JsonResponse({'message': f'Modelo {id} eliminado exitosamente.'}, status=200)
        except Modelo.DoesNotExist:
            return JsonResponse({'error': f'El modelo con ID {id} no existe.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def list_modelos(request, idModelo=None):
    if request.method == 'GET':
        if idModelo:
            try:
                modelo = Modelo.objects.get(idModelo=idModelo)
                serializer = ModeloSerializer(modelo)
                return JsonResponse(serializer.data, status=200)
            except Modelo.DoesNotExist:
                return JsonResponse({'error': 'Modelo no encontrado'}, status=404)
        else:
            modelos = Modelo.objects.all()
            serializer = ModeloSerializer(modelos, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_protect
def get_modelo_by_username(nombre):
    try:
        modelo = Modelo.objects.get(nombre=nombre)
        return modelo
    except Modelo.DoesNotExist:
        return None


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Aqui empieza el crud de línea 

@csrf_exempt
def create_linea(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            idLinea = data.get('idLinea')
            linea = data.get('linea')

            if not (idLinea and linea):
                return JsonResponse({'error': 'Todos los campos son requeridos'}, status=400)

            nueva_linea = Linea.objects.create(
                idLinea=idLinea,
                linea=linea
            )

            return JsonResponse({'message': 'Linea creada exitosamente', 'linea': {'idLinea': nueva_linea.idLinea, 'linea': nueva_linea.linea}})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def update_linea(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            idLinea = data.get('idLinea')
            linea = get_object_or_404(Linea, idLinea=idLinea)

            linea.linea = data.get('linea', linea.linea)
            linea.save()

            return JsonResponse({'message': f'Linea "{linea.linea}" actualizada correctamente.', 'linea': {'idLinea': linea.idLinea, 'linea': linea.linea}})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método HTTP no permitido'}, status=405)

@csrf_exempt
def delete_linea(request, id):
    if request.method == 'DELETE':
        try:
            linea = Linea.objects.get(idLinea=id)
        except Linea.DoesNotExist:
            return JsonResponse({'error': f'La línea con ID {id} no existe.'}, status=404)

        linea.delete()
        return JsonResponse({'message': f'Linea {linea.linea} eliminada exitosamente.'}, status=200)
    else:
        return JsonResponse({"message": "Solo se permiten solicitudes DELETE"}, status=405)

@csrf_protect
def list_lineas(request, linea_id=None):
    if request.method == 'GET':
        if linea_id is not None:
            try:
                linea = Linea.objects.get(idLinea=linea_id)
                return JsonResponse({'idLinea': linea.idLinea, 'linea': linea.linea})
            except Linea.DoesNotExist:
                return JsonResponse({'error': 'Línea no existe'}, status=404)
        else:
            lineas = Linea.objects.all()
            lineas_list = [{'idLinea': l.idLinea, 'linea': l.linea} for l in lineas]
            return JsonResponse(lineas_list, safe=False)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Aqui empieza de descripciones 


@csrf_protect
def get_Descripcion_by_id(descripcion_id):
    try:
        descripcion_obj = Descripciones.objects.get(idDescripcion=descripcion_id) 
        return descripcion_obj
    except Descripciones.DoesNotExist:  
        return None
    
@csrf_exempt
def create_descripcion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            idDescripcion = data.get('idDescripcion')
            descripcion = data.get('Descripcion')

            if not (idDescripcion and descripcion):
                return JsonResponse({'error': 'Todos los campos son requeridos'}, status=400)

            nueva_descripcion = Descripciones.objects.create(
                idDescripcion=idDescripcion,
                Descripcion=descripcion
            )

            return JsonResponse({'message': 'Descripcion creada exitosamente', 'descripcion': {'idDescripcion': nueva_descripcion.idDescripcion, 'Descripcion': nueva_descripcion.Descripcion}})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


# Obtener una descripción por su ID
@csrf_protect
def get_descripcion_by_id(request, id):
    try:
        descripcion = Descripciones.objects.get(idDescripcion=id)
        return JsonResponse({'Descripcion': descripcion.Descripcion, 'idDescripcion': descripcion.idDescripcion})
    except Descripciones.DoesNotExist:
        return JsonResponse({'error': 'Descripción no encontrada'}, status=404)

# Obtener todas las descripciones
@csrf_protect
def get_all_descripciones(request):
    descripciones = Descripciones.objects.all()
    descripciones_list = [{'Descripcion': desc.Descripcion, 'idDescripcion': desc.idDescripcion} for desc in descripciones]
    return JsonResponse(descripciones_list, safe=False)

# Actualizar una descripción
@csrf_exempt
def update_descripcion(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            current_idDescripcion = data.get('current_idDescripcion')
            new_idDescripcion = data.get('new_idDescripcion')
            descripcion = get_object_or_404(Descripciones, idDescripcion=current_idDescripcion)

            descripcion.idDescripcion = new_idDescripcion
            descripcion.Descripcion = data.get('Descripcion', descripcion.Descripcion)
            descripcion.save()

            return JsonResponse({'message': f'Descripcion "{descripcion.Descripcion}" actualizada correctamente.', 'descripcion': {'idDescripcion': descripcion.idDescripcion, 'Descripcion': descripcion.Descripcion}})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método HTTP no permitido'}, status=405)


# Eliminar una descripción
@csrf_exempt
def delete_descripcion(request, id):
    if request.method == 'DELETE':
        try:
            descripcion = Descripciones.objects.get(idDescripcion=id)
        except Descripciones.DoesNotExist:
            return JsonResponse({'error': f'La descripcion con ID {id} no existe.'}, status=404)

        descripcion.delete()
        return JsonResponse({'message': f'Descripcion {descripcion.Descripcion} eliminada exitosamente.'}, status=200)
    else:
        return JsonResponse({"message": "Solo se permiten solicitudes DELETE"}, status=405)


# Lista de todas las descripciones
@csrf_protect
def list_descripciones(request, descripcion_id=None):
    if request.method == 'GET':
        if descripcion_id is not None:
            try:
                descripcion = Descripciones.objects.get(idDescripcion=descripcion_id)
                return JsonResponse({'idDescripcion': descripcion.idDescripcion, 'Descripcion': descripcion.Descripcion})
            except Descripciones.DoesNotExist:
                return JsonResponse({'error': 'Descripcion no existe'}, status=404)
        else:
            descripciones = Descripciones.objects.all()
            descripciones_list = [{'idDescripcion': d.idDescripcion, 'Descripcion': d.Descripcion} for d in descripciones]
            return JsonResponse(descripciones_list, safe=False)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Aqui empieza el crud de  departameto 

@csrf_exempt
def create_departamento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            idDepartamento = data.get('idDepartamento')
            departamento = data.get('departamento')

            if not (idDepartamento and departamento):
                return JsonResponse({'error': 'Todos los campos son requeridos'}, status=400)

            nuevo_departamento = Departamento.objects.create(
                idDepartamento=idDepartamento,
                departamento=departamento
            )

            return JsonResponse({'message': 'Departamento creado exitosamente', 'departamento': {'idDepartamento': nuevo_departamento.idDepartamento, 'departamento': nuevo_departamento.departamento}})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    

def get_departamento_by_id(request, id):
    try:
        departamento = Departamento.objects.get(idDepartamento=id)
        return JsonResponse({'idDepartamento': departamento.idDepartamento, 'departamento': departamento.departamento})
    except Departamento.DoesNotExist:
        return JsonResponse({'error': 'Departamento no encontrado'}, status=404)
    

@csrf_exempt
def update_departamento(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            idDepartamento = data.get('idDepartamento')
            departamento_nombre = data.get('departamento')

            departamento = get_object_or_404(Departamento, idDepartamento=idDepartamento)
            departamento.departamento = departamento_nombre
            departamento.save()

            return JsonResponse({'message': f'Departamento "{departamento.departamento}" actualizado correctamente.', 'departamento': {'idDepartamento': departamento.idDepartamento, 'departamento': departamento.departamento}})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método HTTP no permitido'}, status=405)


    
@csrf_protect
@csrf_exempt
def delete_departamento(request, id):
    if request.method == 'DELETE':
        try:
            departamento = Departamento.objects.get(idDepartamento=id)
            departamento.delete()
            return JsonResponse({'message': f'Departamento {departamento.departamento} eliminado exitosamente.'}, status=200)
        except Departamento.DoesNotExist:
            return JsonResponse({'error': f'El departamento con ID {id} no existe.'}, status=404)
    else:
        return JsonResponse({"message": "Solo se permiten solicitudes DELETE"}, status=405)

@csrf_protect
def list_departamentos(request, departamento_id=None):
    if request.method == 'GET':
        if departamento_id is not None:
            try:
                departamento = Departamento.objects.get(idDepartamento=departamento_id)
                return JsonResponse({'idDepartamento': departamento.idDepartamento, 'departamento': departamento.departamento})
            except Departamento.DoesNotExist:
                return JsonResponse({'error': 'Departamento no existe'}, status=404)
        else:
            departamentos = Departamento.objects.all()
            departamentos_list = [{'idDepartamento': d.idDepartamento, 'departamento': d.departamento} for d in departamentos]
            return JsonResponse(departamentos_list, safe=False)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#Aqui empieza el crud de subdepartamento
@csrf_protect
def create_subdepartamento(request, subdepartamento_nombre, departamento_id):
    try:
        departamento = Departamento.objects.get(idDepartamento=departamento_id)
    except Departamento.DoesNotExist:
        return JsonResponse({'error': f'El departamento con ID {departamento_id} no existe.'}, status=404)

    nuevo_subdepartamento = Subdepartamento(subdepartamento=subdepartamento_nombre, departamento=departamento)
    nuevo_subdepartamento.save()

    return HttpResponse(f"Subdepartamento creado: {subdepartamento_nombre}")

# Obtener un subdepartamento por su ID
@csrf_protect
def get_subdepartamento_by_id(subdepartamento_id):
    try:
        subdepartamento = Subdepartamento.objects.get(idSub=subdepartamento_id)
        serializer = SubdepartamentoSerializer(subdepartamento)
        return JsonResponse(serializer.data)
    except Subdepartamento.DoesNotExist:
        return JsonResponse({'error': f'El subdepartamento con ID {subdepartamento_id} no existe.'}, status=404)

# Actualizar un subdepartamento
@csrf_protect
def update_subdepartamento(request, subdepartamento_id, departamento_id, nuevo_nombre):
    try:
        subdepartamento = Subdepartamento.objects.get(idSub=subdepartamento_id)
    except Subdepartamento.DoesNotExist:
        return JsonResponse({'error': f'El subdepartamento con ID {subdepartamento_id} no existe.'}, status=404)

    if not nuevo_nombre:
        return JsonResponse({'error': 'El nuevo nombre del subdepartamento no puede estar vacío.'}, status=400)

    try:
        nuevo_departamento = Departamento.objects.get(idDepartamento=departamento_id)
    except Departamento.DoesNotExist:
        return JsonResponse({'error': f'El departamento con ID {departamento_id} no existe.'}, status=404)

    subdepartamento.subdepartamento = nuevo_nombre
    subdepartamento.departamento = nuevo_departamento
    subdepartamento.save()

    return JsonResponse({'message': f'Subdepartamento con ID {subdepartamento_id} actualizado a "{nuevo_nombre}" correctamente.'})

# Eliminar un subdepartamento
@csrf_protect
def delete_subdepartamento(request, subdepartamento_id):
    try:
        subdepartamento = Subdepartamento.objects.get(idSub=subdepartamento_id)
    except Subdepartamento.DoesNotExist:
        return JsonResponse({'error': f'El subdepartamento con ID {subdepartamento_id} no existe.'}, status=404)

    try:
        subdepartamento.delete()
        return JsonResponse({'message': f'Subdepartamento con ID {subdepartamento_id} eliminado correctamente.'})
    except Exception as e:
        return JsonResponse({'error': f'Error al eliminar el subdepartamento: {str(e)}'}, status=500)
    

# Listar todos los subdepartamentos
@csrf_protect
def list_subdepartamentos(request):
    subdepartamentos = Subdepartamento.objects.all()
    serializer = SubdepartamentoSerializer(subdepartamentos, many=True)
    return JsonResponse(serializer.data, safe=False)


#--------------------------------------------------------------------------------
#Aquí empiza donde se obtienen los datos de la produccion y de los paros. 



@csrf_protect
def list_producciones(request):
    if request.method == 'GET':
        producciones = Produccion.objects.all()
        serializer = ProduccionSerializer(producciones, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_protect
def list_paros(request):
    if request.method == 'GET':
        paros = Paro.objects.all()
        serializer = ParoSerializer(paros, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def create_produccion(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['linea'] = request.session.get('linea')  # Obtener la línea de la sesión
        serializer = ProduccionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    
@csrf_exempt
def create_paro(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ParoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@csrf_exempt
def update_produccion(request, id):
    if request.method == 'PUT':
        produccion = get_object_or_404(Produccion, pk=id)
        data = JSONParser().parse(request)
        serializer = ProduccionSerializer(produccion, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def update_paro(request, id):
    if request.method == 'PUT':
        paro = get_object_or_404(Paro, pk=id)
        data = JSONParser().parse(request)
        serializer = ParoSerializer(paro, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def delete_produccion(request, id):
    if request.method == 'DELETE':
        produccion = get_object_or_404(Produccion, pk=id)
        produccion.delete()
        return JsonResponse({'message': 'Producción eliminada'}, status=204)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def delete_paro(request, id):
    if request.method == 'DELETE':
        paro = get_object_or_404(Paro, pk=id)
        paro.delete()
        return JsonResponse({'message': 'Paro eliminado'}, status=204)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
#---------------------------------------------------------------------------------------------------
    
@csrf_exempt
def create_slitter_produccion(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SlitterProduccionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def create_slitter_paro(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SlitterParoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Vistas de osiladora para crear paros y formularios 

@csrf_exempt
def create_osiladora_produccion(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OsiladoraProduccionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def create_osiladora_paro(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OsiladoraParoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Vistas para lo que genera los reportes 

@csrf_protect
def generar_reporte_pdf(request, turno):
    linea = request.session.get('linea')  # Obtener la línea de producción de la sesión
    if not linea:
        return JsonResponse({"message": "Línea de producción no encontrada en la sesión"}, status=400)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{turno}_{linea}.pdf"'
    generar_reporte_por_turno(response, [turno], linea)
    return response

@csrf_protect
def generar_reporte_excel_view(request, turno):
    linea = request.session.get('linea')  # Obtener la línea de producción de la sesión
    if not linea:
        return JsonResponse({"message": "Línea de producción no encontrada en la sesión"}, status=400)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="reporte_{turno}_{linea}.xlsx"'
    generar_reporte_excel([turno], linea)
    return response