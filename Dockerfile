FROM python:buster
RUN apt-get update && apt-get install -y libdbus-glib-1-dev libgirepository1.0-dev
RUN pip3 install dbus-python glib PyQt5 gobject PyGObject
COPY gatt-cts-server.py /
ENTRYPOINT ["python", "/gatt-cts-server.py"] 
