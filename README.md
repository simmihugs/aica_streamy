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
