# Drones Example
Basic REST Api example to manage transportation for drones made using Django Framework. Including technology as:
* Celery and Redis for automated tasks.
* Django Rest Framework to build REST APIs using Django.
* PostgreSQL as database system.
* Docker and Docker Compose for development and deployment.

## To run the REST API with Docker and Docker Compose
***
Run on the terminal command on the root directory of the project `docker-compose up --build -d` or `docker-compose up --build -d` or `docker compose up --build -d` depending of your docker and docker compose installation. 

You can access to API swagger schema on [http://localhost:8005/api/docs/swagger/](http://localhost:8005/api/docs/swagger/).
You can also access to a basic admin application of Django on [http://localhost:8005/admin/](http://localhost:8005/admin/). A default superuser was created with **username:** admin and **password:** admin. You can use that user to log in on admin and to obtain a JWT token to use the API.

**Important!!!** The endpoint for drones, medications and loads managments require a authenticated user, you can use 

## Importants endpoints
***
To see more check swagger api on [http://localhost:8005/api/docs/swagger/](http://localhost:8005/api/docs/swagger/)