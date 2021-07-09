FROM python:3.9

LABEL maintainer="Marcelo Feitoza Parisi (marcelo@feitoza.com.br)"

# Copy Helpers
RUN mkdir -p /usr/src/app/helpers
COPY helpers/__init__.py /usr/src/app/helpers/
COPY helpers/database.py /usr/src/app/helpers/
COPY helpers/events.py /usr/src/app/helpers/
COPY helpers/globalholders.py /usr/src/app/helpers/
COPY helpers/kubeclient.py /usr/src/app/helpers/
COPY helpers/logutil.py /usr/src/app/helpers/
COPY helpers/services.py /usr/src/app/helpers/

# Copy Application
WORKDIR /usr/src/app
COPY kubernetes-lb-controller.py ./

# Install Deps
RUN pip install kubernetes
RUN pip install urllib3
RUN pip install pysqlite3
RUN pip install prettytable

CMD [ "python3", "-u", "./kubernetes-lb-controller.py" ]
