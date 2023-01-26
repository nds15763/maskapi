FROM python:3.9
WORKDIR /maskapi

COPY ./requirements.txt /maskapi/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /maskapi/requirements.txt

COPY ./app /maskapi/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]