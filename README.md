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

**Important!!!** The endpoint for drones, medications and loads managments require a authenticated user, you can use the endpoint [http://localhost:8005/api/token/](http://localhost:8005/api/token/) to get a valid JWT token

## Drone's battery history log
***
A history log of the drone's batteries is save on the database and in a log file you can the database log on django admin in [localhost:8005/admin/base/dronestatuslog](localhost:8005/admin/base/dronestatuslog). Log is updated each minute for all the drones.

## Testing
***
Unit tests were added to test the API's endpoints, you can run the tests with command: 

`docker exec -it drones_api  python manage.py test`

## Importants endpoints
***
* [http://localhost:8005/api/token/](http://localhost:8005/api/token/) to get a valid JWT token
* [http://localhost:8005/drones/](http://localhost:8005/drones/) POST to add a drone
* [http://localhost:8005/drones/available_for_loading/](http://localhost:8005/drones/available_for_loading/) GET to to list all drone available for loading
* [http://localhost:8005/drones/{id}/load_addition/](http://localhost:8005/drones/{id}/load_addition/) PATCH to add load to a drone
* [http://localhost:8005/drones/{id}/load/](http://localhost:8005/drones/{id}/load/) GET to list all the medications loaded on a drone
* [http://localhost:8005/drones/{id}/battery/](http://localhost:8005/drones/{id}/battery/) GET to get the battery of a drone

To see more check swagger api on [http://localhost:8005/api/docs/swagger/](http://localhost:8005/api/docs/swagger/)