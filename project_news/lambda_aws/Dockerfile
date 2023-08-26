FROM public.ecr.aws/lambda/python:3.9

WORKDIR /app

COPY requirements.txt  .

RUN python -m pip install --user -r requirements.txt

COPY . .

CMD [ "pars_into_db.handler" ]