This repository contains Django/Wagtail application code we will deploy to AWS ECS.

# PostgreSQL on AWS

Launch a new PostgreSQL database in RDS by running the enclosed ```aws/django-rds``` CloudFormation template. Name your stack ```django-rds```. Refer to the CloudFormation output for PostgreSQL server hostname.

# Django/Wagtail

## Installation

Install the Python packages related to Django and Wagtail, then create a new Wagtail application.

```
pip install wagtail
wagtail start app
```
We are going to load our settings from a ```.env``` file rather than hard-coading them into the settings .py file(s) so that settings are not committed to our source code repository. This also makes it very easy to use different ```.env``` files to switch between dev and prod environments.

Install the ```django-dotenv``` Python module

```
pip install django-dotenv
```

Add the following line to your ```requirements.txt``` file

```
django-dotenv==1.4.2
```

We must add the following lines to ```manage.py```. Refer to ```django-dotenv``` [instructions](https://github.com/jpadilla/django-dotenv) for correct placement.

```
import dotenv
    dotenv.read_dotenv()
    from django.core.management import execute_from_command_line
```

We must add the following lines to ```app/wsgi.py```. Refer to ```django-dotenv``` [instructions](https://github.com/jpadilla/django-dotenv) for correct placement.

```
import dotenv
dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
```

Replace the ```DEBUG``` and ```SECRET_KEY``` lines in your ```app/settings/dev.py``` file with the following lines:

```
DEBUG = os.environ["DEBUG"]
SECRET_KEY = os.environ["SECRET_KEY"]
```

Add the following lines to your ```.env``` file:

```
DEBUG=True
SECRET_KEY="you-need-to-configure-a-custom-secret-key"
```

*Note: Be sure to configure a custom secret key above!*

Install the Python module required for PostgreSQL database backend.

```
pip install psycopg2
```

Add the following line to your ```requirements.txt``` file
```
psycopg2==2.7.5
```

Add the following lines in your ```app/settings/dev.py``` file:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["DATABASE_NAME"],
        'USER': os.environ["DATABASE_USER"],
	    'PASSWORD': os.environ["DATABASE_PASSWORD"],
	    'HOST': os.environ["DATABASE_HOST"],
	'PORT': '5432',
    }
}
```

Add the following lines to your ```.env``` file:

```
DATABASE_HOST=django-demo.a1b2c3d4e5f6.us-east-1.rds.amazonaws.com
DATABASE_NAME=django
DATABASE_USER=django
DATABASE_PASSWORD=password
```

*Note: If you used the "django-rds" AWS CloudFormation template to launch your PostgreSQL server, refer to the hostname shown in the CloudFormation output.*

Run Django/Wagtail in Docker Container

```
./docker/up.sh
```

*Note: The first time you start the Docker Container, you will have to wait for Docker to download all of the necessary files and build the container image. The first time the container starts, you will have to wait for Django/Wagtail to create all of the PostgreSQL tables. This is normal, and should only happen the first time.*

Shell into Docker Container and create a super user for Django/Wagtail

```
./docker/bash.sh
./manage.py createsuperuser
exit
```

Need to view Docker Container Logs?

```
./docker/logs.sh
```

Need to shutdown Docker Container?

```
./docker/down.sh
```

**Do not continue until your Django/Wagtail app is running correctly!** You should be able to use your local web browser to view the app on [localhost:8000](http://localhost:8000).

# Docker Registry

## Create Registry

Create a Docker Registry, referred to as an Elastic Container Registry (ECR) on AWS, by running the enclosed ```aws/django-ecr``` CloudFormation template. Name your stack ```django-ecr```. 

Refer to the CloudFormation stack output for your registry URI. Edit your ```docker/push.sh``` script and configure the URI.

## Publish Container Image

Run the following command to push your local Docker Container image to your hosted Docker Registry on AWS:

```
./docker/push.sh
```

**Do not continue until you have finished pushing your container image.**

# Elastic Container Service (ECS)

We are ready to launch your Django/Wagtail application on AWS ECS!

Run the enclosed ```aws/django-ecs``` CloudFormation template. Name your stack ```django-ecs```. 

Choose the SSH key pair, the VPC, and the Subnet(s) to use when launching your APP. If you do not already have a Key Pair, create a new Key Pair in the "Key Pairs" menu under EC2 in the AWS Console. You can use this key pair to access the servers that are running your Docker Containers if you need to troubleshoot a problem. The first time you launch the stack, leave the App Service Count set to zero (0).

As long as the stack builds without errors, go ahead and update the stack and increase the App Service Count to two (2) so that your Django/Wagtail app will run on two containers. AWS will automatically load balance traffic between the two containers.
