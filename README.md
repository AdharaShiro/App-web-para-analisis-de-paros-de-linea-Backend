----------------------------------------------------------**#Comandos de instalación**------------------------------------

--------------------------------------------------------------------**Python**--------------------------------------------
Para configurar el backend con Djago es necesario instalar varios paquetes necesario, principalmente se necesita de Python 
en el sistema https://www.python.org/< página oficial descarga el instalador adecuado a tus sistema operativo, asegundado 
de marcar la casilla de "Add Python to PATH' para utilizarpython de desde la línea de comandos.

python- venv env

Python

python--version

**Instalar pip para gestor de paquetes de Python y generalmente se vieen preeinstalado**

pip--version


php artisan passport:install

--------------------------------------------------------------------**Django**--------------------------------------------

Ahora si padamos a instalar el entorno virtual que es Django usando pip

pip install django

***Verifica la instalación de Django**

python-django-version


**Django REST framework: Para construir APIs RESTful.**

pip install djangorestframework

**Django coors headers para manejar solicitudes CORS**
pip install django-cors-headers

Drivers para MySQL 

pip install mysqlclient

pip install -r requirements.txt




---------------------------------------------------------------**Clonar repositorio**-------------------------------------


git clone https://github.com/usuario/nombre-del-repositorio.git

cd Backend

python- venv env

Activa el entorno virtual

cd Backend 

.\env\Scripts\activate

***Instañar dependecias**
Configura las variables de entorno necesarias para el proyecto. Puedes hacerlo creando un archivo .env en la raíz del proyecto.
en caso de ser nesesario uno nuevo Un ejemplo de cómo puede verse el archivo ejemplo :

DEBUG=True
SECRET_KEY=tu_secreto_aqui
DATABASE_URL=sqlite:///db.sqlite3 --- En caso de usar ese gestor de base de datos 


***Migraciones de la base de datos**
python manage.py migrate

vista 

![image](https://github.com/user-attachments/assets/46c31a07-eac0-4c1d-9798-137adb8048e7)


**En caso de tener pruebas de testeo**

python manage.py test

![image](https://github.com/user-attachments/assets/2fdc420e-d828-430d-ad3b-e44891533972)

