# LLM Chat

Exploring a LLM chat, which scrolls when answer outgrows given space

# Table of Contents

1.  [Docker](#org876099e)
    1.  [Docker installieren](#orgf359557)
    2.  [Docker Benutzung](#org53a5a3e)
        1.  [build images](#org4d4e77f)
        2.  [list images](#org3a73a90)
        3.  [tar images](#orgd4541c5)
        4.  [copy tars to server](#org49244d7)
        5.  [install images](#org1b613f8)
        6.  [create compose file & run](#orga49def7)

# Docker

## Docker installieren

Siehe [docks.docker.com](https://docs.docker.com/engine/install/ubuntu/)

## Docker Benutzung

### build images

    ╭[simmi@pc] ~
    ╰─> docker compose build

### list images

    ╭[simmi@pc] ~
    ╰─> docker images
    REPOSITORY            TAG       IMAGE ID       CREATED        SIZE
    api_button-frontend   latest    c3c9d4ffb514   24 hours ago   193MB
    api_button-backend    latest    9e69618a287d   24 hours ago   2.2GB
    ╭[simmi@pc] ~
    ╰─>    

### tar images

    docker save api_button-frontend:latest > api_button-frontend.tar
    docker save api_button-backend:latest > api_button-backend.tar       

### copy tars to server

    scp api_button-frontend.tar api_button-backend.tar <USER>@<SERVER>:~<DIR>/.
    ssh <USER>@<SERVER>

### install images

    docker load -i api_button-frontend.tar
    docker load -i api_button-backend.tar

### create compose file & run

1.  create `compose.yml`

        services:
          backend:
            image: api_button-frontend:latest
            ports:
             - 8000:8000
            depends_on:
             - redis
          frontend:
            image: api_button-frontend:latest
            ports:
              - 3000:80
            depends_on:
              - backend
          redis:
            image: redis

2.  run

        docker compose up
        # or
        docker compose up -d # d means detatched === in the background

