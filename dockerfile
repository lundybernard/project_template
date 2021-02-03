FROM python:3.8-alpine
ADD . /opt/bat
WORKDIR /opt/bat

RUN pip install -r requirements.txt

# Run unittests, fails the build on failing tests
RUN python -m unittest discover bat.tests -p '*_test.py'
# install the module
RUN python setup.py install

# when called with docker run, execute the bat command with arguments
# EX: docker run bat --help
ENTRYPOINT ["bat"]
# Use bat cli to start the service
CMD ["start"]
