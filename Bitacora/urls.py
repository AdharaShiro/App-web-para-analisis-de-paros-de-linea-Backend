"""
URL configuration for Bitacora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [

   path('api/csrf-token/',views.get_csrf_token),

#Ruta del login  

    path('api/login/', views.login_user, name='login_user'),
    path('api/logout/', views.logout_view, name='logout_view'),
    path('api/user/', views.user_view, name='user_view'),
    path('api/csrf-token/', views.csrf_token_view, name='csrf_token_view'),# Nueva URL para obtener el token CSRF
   

#Ruta de Usuarios
    path('api/usuarios/', views.ListUser, name='api-usuarios'),  # URL para listar todos los usuarios
    path('api/users/<int:user_id>/', views.ListUser, name='user-list'),  # URL para obtener un usuario por su ID
    path('api/user-management/by_position/<str:position>/', views.get_users_by_position, name='get_users_by_position'),  # URL para obtener usuarios por posición
    path('api/user-management/create/', views.create_user, name='create_user'), #URL para crear un usuario
    path('api/user-management/update/', views.update_user, name='update_user'),
    path('api/user-management/delete/<int:id>/', views.delete_user, name='delete_user'),# URL para eliminar un usuario


    #Ruta de Modelos
    path('api/modelos/', views.list_modelos, name='list_modelos'),  # Lista todos los modelos
    path('api/modelos/create/', views.create_modelo, name='create_modelo'),  # Crea un nuevo modelo
    path('api/modelos/<int:model_id>/', views.list_modelos, name='list_modelo'),  # Lista un modelo específico
    path('api/modelos/update/', views.update_modelo, name='update_modelo'),  # Actualiza un modelo existente
    path('api/modelos/delete/<str:id>/', views.delete_modelo, name='delete_modelo'),  # 


    #Rutas para  líneas

    path('api/lineas/', views.list_lineas, name='list_lineas'),
    path('api/lineas/create/', views.create_linea, name='create_linea'),
    path('api/lineas/update/', views.update_linea, name='update_linea'),
    path('api/lineas/delete/<str:id>/', views.delete_linea, name='delete_linea'),



    #Ruta para descripciones 
    path('api/list_descripciones/', views.list_descripciones, name='list_descripciones'),
    path('api/descripcion/create/', views.create_descripcion, name='create_descripcion'),
    path('api/descripcion/<int:id>/', views.get_descripcion_by_id, name='get_descripcion_by_id'),
    path('api/descripcion/update/', views.update_descripcion, name='update_descripcion'),
    path('api/descripcion/delete/<str:id>/', views.delete_descripcion, name='delete_descripcion'),
    


    #Ruta para Departamentos
    path('api/list_departamentos/', views.list_departamentos, name='list_departamentos'),
    path('api/departamento/create/', views.create_departamento, name='create_departamento'),
    path('api/departamento/<str:id>/', views.get_departamento_by_id, name='get_departamento_by_id'),
    path('api/departamento/update/', views.update_departamento, name='update_departamento'),
    path('api/departamento/delete/<str:id>/', views.delete_departamento, name='delete_departamento'),



    #Ruta de Subdepartamentos 
    path('api/subdepartamentos/', views.list_subdepartamentos, name='list_subdepartamentos'),
    path('api/subdepartamentos/create/<str:subdepartamento_nombre>/<int:departamento_id>/', views.create_subdepartamento, name='create_subdepartamento'),
    path('api/subdepartamentos/<int:subdepartamento_id>/', views.get_subdepartamento_by_id, name='get_subdepartamento_by_id'),
    path('api/subdepartamentos/update/<int:subdepartamento_id>/<int:departamento_id>/<str:nuevo_nombre>/', views.update_subdepartamento, name='update_subdepartamento'),
    path('api/subdepartamentos/<int:subdepartamento_id>/delete/', views.delete_subdepartamento, name='delete_subdepartamento'),
   
    #Rutas para producción y paros 
    path('api/list_producciones/', views.list_producciones, name='list_producciones'),
    path('api/list_paros/', views.list_paros, name='list_paros'),
    path('api/produccion/create/', views.create_produccion, name='create_produccion'),
    path('api/paro/create/', views.create_paro, name='create_paro'),
    path('api/produccion/update/<int:id>/', views.update_produccion, name='update_produccion'),
    path('api/paro/update/<int:id>/', views.update_paro, name='update_paro'),
    path('api/produccion/delete/<int:id>/', views.delete_produccion, name='delete_produccion'),
    path('api/paro/delete/<int:id>/', views.delete_paro, name='delete_paro'),

    #Rutas que crean produccion y paros de línea en slitter
    path('api/slitter_produccion/create/', views.create_slitter_produccion, name='create_slitter_produccion'),
    path('api/slitter_paro/create/', views.create_slitter_paro, name='create_slitter_paro'),

    #Rutas que crean produccion y paros de linea en osiladora urlpatterns = [
    path('api/osiladora_produccion/create/', views.create_osiladora_produccion, name='create_osiladora_produccion'),
    path('api/osiladora_paro/create/', views.create_osiladora_paro, name='create_osiladora_paro'),


  #Rutas que generan los reportes    
  
]





