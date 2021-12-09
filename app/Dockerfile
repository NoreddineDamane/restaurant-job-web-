FROM python:3.7

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
#RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org tensorflow
#RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org opencv-python
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY app.py /app
CMD python app.py
