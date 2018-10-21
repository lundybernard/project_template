FROM python:3.4-alpine
ADD . /opt/project
WORKDIR /opt/project
RUN pip install -r requirements.txt

# install the module
RUN python setup.py develop
# Run unittests, fails the build on failing tests
RUN python -m unittest discover project.tests -p '*_test.py'

# Use project cli to start the service
CMD ["project", "start"]
