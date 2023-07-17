FROM python:3.9.15-slim
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/src/lib"
WORKDIR /usr/src/app

# install nodemon
RUN apt update
RUN apt install curl -y
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash
RUN apt install nodejs
RUN npm install -g npm@9.2.0
RUN npm install -g nodemon

# install pg_config
RUN apt install libpq-dev -y
RUN apt install build-essential -y

# upgrade pip
RUN python -m pip install --upgrade pip

# dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# run the script
CMD (chmod +x ./run.sh) && (./run.sh)