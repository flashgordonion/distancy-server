FROM python:3

WORKDIR /user/app/

COPY . .

RUN pip install --no-cache-dir -r /user/app/requirements.txt

EXPOSE 8000

RUN chmod u+x /user/app/startup.sh
CMD ["/user/app/startup.sh"]
