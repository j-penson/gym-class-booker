FROM python:3.7

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update && apt-get install -y google-chrome-stable

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

ENV PORT 8080
EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-t", "120", "main:app"]

