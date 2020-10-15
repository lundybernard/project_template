# project template
example python microservice project

[![Build Status](https://travis-ci.org/lundybernard/project_template.svg?branch=master)](https://travis-ci.org/lundybernard/project_template)

## Installation
install in developer mode from source

```
python setup.py develop
```

## Run Functional tests

### Manually
start the web server on local host

```
project start
```

run tests against the web server

```
python -m unittest functional_tests/service_test.py
pytest functional_tests/service_test.py
```

### Run the service and tests via CLI
Install the package

```
python setup.py install
python setup.py develop
```

start webserver with cli

```
project start
```

Run functional tests

```
project test service
pytest functional_tests/service_test.py
```

### Run Container tests
to validate the docker container works properly, and docker-compose works

#### Manual Test
Run the container with docker-compose and test it with functional_tests

```
docker-compose build
docker-compose up
pytest functional_tests/service_test.py
```

#### Automatic test
container_test will run docker-compose before each test case,
and execute the test against the running container

```
python -m unittest container_tests/container_test.py
pytest container_tests/container_test.py

```

CLI

```
project run_container_tests
```


## rebuild local containers
sometimes necessary if container tests are failing
```
docker-compose down --rmi local
docker-compose build
```


### Kubernetes deployment example:
1. install Microk8s
```
sudo snap install microk8s --classic
microk8s.start
```

2. Start a local Docker Registry
```
docker run -p 5001:5001 registry
```

3. Tag and Push the image to your docker registry
```
docker build -t project-app ./
docker tag project-app localhost:5001/project-app
docker push localhost:5001/project-app
```

4. Run the application and ingress
```
microk8s.kubectl apply -f k8/ingress.yml
microk8s.kubectl apply -f k8/project-app-deployment.yml
```

5. enable ingress
```
microk8s.enable ingress
```
and verify
```
microk8s.kubectl get all -A
```

6. expose the application
```
microk8s.kubectl expose deployment project-app --type=LoadBalancer --port=8080
```

7. test the endpoint
```
curl -kL https://127.0.0.1/project-app
```
