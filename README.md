# LLM Chat

Exploring an LLM chat, which scrolls when the answer outgrows the given space

# Table of Contents

1. [Docker](#docker)
   1. [Installing Docker](#installing-docker)
   2. [Using Docker](#using-docker)
      1. [Build images](#build-images)
      2. [List images](#list-images)
      3. [Tar images](#tar-images)
      4. [Copy tars to server](#copy-tars-to-server)
      5. [Install images](#install-images)
      6. [Create compose file & run](#create-compose-file--run)

# Docker

## Installing Docker

See [docs.docker.com](https://docs.docker.com/engine/install/ubuntu/)

## Using Docker

### Preparations
Erst mussten für das Repository eine Reihe von dateien erstellt werden

    compose.yml
    Dockerfile
    web.Dockerfile
    nginx.conf

An diesen dateien musste ich erstaunlicherweise nichts ändern,
keinen app namen eintragen oder ähnliches.

File hierachie

    {app_name}
    ├── .web
    ├── assets
    ├── {app_name}
    │   ├── __init__.py
    │   └── {app_name}.py
    ├── compose.yml
    ├── Dockerfile
    ├── nginx.conf
    ├── web.Dockerfile
    └── rxconfig.py

Im detail sehen die so aus

#### `compose.yml`

    services:
      backend:
        build:
          dockerfile: Dockerfile
        ports:
         - 8000:8000
        depends_on:
         - redis
      frontend:
        build:
          dockerfile: web.Dockerfile
        ports:
          - 3000:80
        depends_on:
          - backend
      redis:
        image: redis

#### `Dockerfile`

    FROM python:3.12
    
    
    ENV REDIS_URL=redis://redis PYTHONUNBUFFERED=1
    
    WORKDIR /app
    COPY . .
    
    RUN pip install -r requirements.txt
    
    
    ENTRYPOINT ["reflex", "run", "--env", "prod", "--backend-only", "--loglevel", "debug" ]

#### `web.Dockerfile`

    FROM python:3.12 AS builder
    
    WORKDIR /app
    
    COPY . .
    RUN pip install -r requirements.txt
    RUN reflex export --frontend-only --no-zip
    
    FROM nginx
    
    COPY --from=builder /app/.web/_static /usr/share/nginx/html
    COPY ./nginx.conf /etc/nginx/conf.d/default.conf

#### `nginx.conf`

    server { 
     listen 80;
     listen  [::]:80;
     server_name frontend;
    
    
     error_page   404  /404.html;
    
     location /_event {
        proxy_set_header   Connection "upgrade";
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
     }
    
     location /ping {
        proxy_pass http://backend:8000;
     }
    
     location /_upload {
        proxy_pass http://backend:8000;
     }
    
     location / {
       # This would be the directory where your Reflex app's static files are stored at
       root /usr/share/nginx/html;
     }
    
    }

### Build images

```
╭[simmi@pc] ~
╰─> docker compose build
```

### List images

```
╭[simmi@pc] ~
╰─> docker images
REPOSITORY               TAG       IMAGE ID       CREATED        SIZE
aica_streamy-frontend    latest    c3c9d4ffb514   24 hours ago   193MB
aica_streamy-backend     latest    9e69618a287d   24 hours ago   2.2GB
╭[simmi@pc] ~
╰─>    
```

### Tar images

```
docker save aica_streamy-frontend:latest > aica_streamy-frontend.tar
docker save aica_streamy-backend:latest > aica_streamy-backend.tar       
```

### Copy tars to server

```
scp aica_streamy-frontend.tar aica_streamy-backend.tar <USER>@<SERVER>:~<DIR>/.
ssh <USER>@<SERVER>
```

### Install images

```
docker load -i aica_streamy-frontend.tar
docker load -i aica_streamy-backend.tar
```

### Create compose file & run

1. Create `compose.yml`

```yaml
services:
  backend:
    image: aica_streamy-frontend:latest
    ports:
     - 8000:8000
    depends_on:
     - redis
  frontend:
    image: aica_streamy-frontend:latest
    ports:
      - 3000:80
    depends_on:
      - backend
  redis:
    image: redis
```

2. Run

```
docker compose up
# or
docker compose up -d # d means detached === in the background
```
