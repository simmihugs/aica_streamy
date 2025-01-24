# LLM Chat

Exploring a LLM chat, which scrolls when answer outgrows given space


# Table of Contents

1.  [Docker container local ohne .env testen](#org3d89c75)
    1.  [Erster Schritt](#orgae8556c)
        1.  [`compose.yml`](#orged6c96d)
        2.  [`Dockerfile`](#org9efa02c)
        3.  [`web.Dockerfile`](#org2288be3)
        4.  [`nginx.conf`](#orgf09b61f)
    2.  [Zweiter Schritt - Docker](#org30a1cbd)
        1.  [Docker installieren](#orgd298ddc)
        2.  [Docker local laufen lassen](#orga8f4691)
        3.  [Docker hub](#org3d8458f)
2.  [Docker container für akuellen stand von richtier App bauen](#orge539255)
3.  [Neues Vps - emails checken](#org0a5ff29)
4.  [Dockerhub ausprobieren](#orgce9163e)



<a id="org3d89c75"></a>

# DONE Docker container local ohne .env testen

Nach viel hin und her hat es geklappt. Hier ein recap wie es
geklappt hat.


<a id="orgae8556c"></a>

## Erster Schritt

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


<a id="orged6c96d"></a>

### `compose.yml`

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


<a id="org9efa02c"></a>

### `Dockerfile`

    FROM python:3.12
    
    
    ENV REDIS_URL=redis://redis PYTHONUNBUFFERED=1
    
    WORKDIR /app
    COPY . .
    
    RUN pip install -r requirements.txt
    
    
    ENTRYPOINT ["reflex", "run", "--env", "prod", "--backend-only", "--loglevel", "debug" ]


<a id="org2288be3"></a>

### `web.Dockerfile`

    FROM python:3.12 AS builder
    
    WORKDIR /app
    
    COPY . .
    RUN pip install -r requirements.txt
    RUN reflex export --frontend-only --no-zip
    
    FROM nginx
    
    COPY --from=builder /app/.web/_static /usr/share/nginx/html
    COPY ./nginx.conf /etc/nginx/conf.d/default.conf


<a id="orgf09b61f"></a>

### `nginx.conf`

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


<a id="org30a1cbd"></a>

## Zweiter Schritt - Docker


<a id="orgd298ddc"></a>

### Docker installieren

Details lasse ich aus


<a id="orga8f4691"></a>

### Docker local laufen lassen

Im repository mit den dateien muss man dann `docker` ausführen,
kann dabei auch gleich testen, ob es funzt.

    docker compose up 

Und im Browser dann auf `localhost:3000` gehen.


<a id="org3d8458f"></a>

### Docker hub

Die config erzeugt 3 docker images. Dazu nochmal das
`compose.yml` file

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

Wir haben `backend` das von `redis` abhängt. `frontend` das von
`backend` abhängt und `redis`. Das schöne an `redis` ist, dass
es ein generell der public bekanntes docker image ist, im
gegensatz zu den anderen beiden Komponenten.
Was man nun braucht um die app wo anders laufen zu lassen, ist
das image von `frontend` und `backend`.

Dazu habe ich viel rum versucht. Ich dachte man kann die einfach
hin und her kopieren - was vermutlich auch geht, aber das habe
ich nicht hinbekommen. Aber was geklappt hat ist, dass man
`frontend` und `backend` auf dockerhub pushed. Das ist so
ähnlich wie github nur für docker images.

Zusätzlich musste ich für Dockerhub einen account
erstellen. Achtung die images sind entweder public oder man kann
nur 1 image haben, weil dockerhub nur max. 1 private image pro
free account erlaubt. Das hat mich auch nochmal aufgehalten.

1.  build the images

        ╭[simmi@ccdev111] ~/Programs/api_button
        ╰─> docker compose build                                                                         ✨🐱🏍🎉😎
        ...
         ✔ Service backend   Built                                                                             4.9s
         ✔ Service frontend  Built                                                                             3.5s

2.  list the images

        ╭[simmi@ccdev111] ~/Programs/api_button
        ╰─> docker images                                                                                ✨🐱🏍🎉😎
        REPOSITORY                     TAG       IMAGE ID       CREATED             SIZE
        simmihugs/littel-website       latest    7efc514f0a62   21 minutes ago      192MB
        api_button_docker-backend      latest    319156ba5348   About an hour ago   3.76GB
        api_button_copy-frontend       latest    db9c72c989ff   22 hours ago        193MB
        api_button_copy-backend        latest    c7b9082b3301   22 hours ago        4.65GB
        simmihugs/api_button           latest    ea50a8220cfa   22 hours ago        4.65GB
        api_button-frontend            latest    47b3db5e4736   23 hours ago        193MB
        api_button                     v0.1      b52407596aa6   23 hours ago        2.2GB
        simmihugs/api_button/backend   v0.1      b52407596aa6   23 hours ago        2.2GB
        api_button-backend             latest    56fb4e7f5929   23 hours ago        2.2GB
        redis                          latest    691a00f92e2c   3 days ago          117MB

3.  tag the images

        ╭[simmi@ccdev111] ~/Programs/api_button
        ╰─> docker tag api_button-frontend:latest simmihugs/api_button-frontend:latest                   ✨🐱🏍🎉😎
        ╭[simmi@ccdev111] ~/Programs/api_button
        ╰─> docker tag api_button-backend:latest simmihugs/api_button-backend:latest                     ✨🐱🏍🎉😎
        ╭[simmi@ccdev111] ~/Programs/api_button

4.  push the images

        docker push simmihugs/api_button-backtend:latest
        docker push simmihugs/api_button-frontend:latest

5.  Docker image von Dockerhub laufen lassen

    Hierfür sind 3 Schritte nötig.
    
    1.  man muss auf dem anderen rechner wiederum docker installieren.
    2.  man muss die images von dockerhub pullen
    3.  man muss ein angepasstes `compose.yml` erzeugen
    
    Bzgl. dem 2. Schritt bin ich mir nicht ganz sicher, weil
    eigentlich müsste das compose.yml die images automatisch
    herunterladen und installieren, aber ich habe es gemacht. Test
    ob man die nicht selber pullen muss kommt noch. Das angepasste
    `compose.yml` sieht dann wiederum so aus
    
        services:
          backend:
            image: simmihugs/api_button-backend:latest
            ports:
             - 8000:8000
            depends_on:
             - redis
          frontend:
            image: simmihugs/api_button-frontend:latest
            ports:
              - 3000:80
            depends_on:
              - backend
          redis:
            image: redis
    
    Und um den bums dann laufen zu lassen macht man
    
        docker compose up


<a id="orge539255"></a>

# TODO Docker container für akuellen stand von richtier App bauen


<a id="org0a5ff29"></a>

# TODO Neues Vps - emails checken


<a id="orgce9163e"></a>

# TODO Dockerhub ausprobieren

