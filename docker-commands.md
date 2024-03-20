## ***Basic Docker functions:***

- `docker pull <image>:<image-version>`  <-- downloads an image of the app from docker
- 

- `docker run <image>:<image-version>`     <-- pulls an image and starts the container (virtual environment).
                                            This makes an image run in a container


- `docker ps`  <-- lists current running containers and related info


- `docker ps -a`  <-- lists all containers (running and stopped)


- `docker ps -a | grep <your-image-name>`  <-- useful to find a specific Image or container among many


- `docker images`  <-- list images


- `docker start <container-ID/container-name>`    <-- start a stopped container


- `docker stop <container-ID/container-name>`     <-- stop a running container


- `docker run -d -p 0000:0000 --name cont-name <image>:<image-version>`    <-- `-d` for *detached mode*, `-p` for *port*.
                                                                            _Detached mode_ allows to continue using
                                                                            the terminal window.
                                                                            _Host side_ ports must be always unique,
                                                                            while _container side_ ports can remain the same
                                                                            while using the same image regardless of its version.


-       docker run -e ... \
                   -e ... \
        <image>:<image-version>    <-- here `-e` option allows to set environment variables if needed.


- `docker run --net <network-name> <image>:<image-version>`   <-- `--net` allows to create a network.
                                                            Network lets multiple images communicate with one another
                                                            inside a container.



- `docker exec -it <container-id> /bin/bash or /bin/sh`    <-- to go inside a container; `-it` means *interactive terminal*
                                                            `/bin/bash` or `/bin/sh` is needed to have a working terminal


- `docker logs <container-id/container-name>`      <-- to see the logs of the container. Great for troubleshooting.
  - `docker logs <container-id/container-name> | tail`     <-- Here `tail` shows only the end of log file. 


- `docker rm <container-id>`    <-- to remove a container.


- `docker rmi <your-image-id>`    <-- to remove an Image.


## ***Docker Compose file***

**[DOCS](https://docs.docker.com/compose/gettingstarted/)**

Docker Compose file allows to set all configuration parameters in a single file to make *Docker* set up easier. 

Docker compose takes care of the network, so no need to specify it in a file.

Example:

    version: '3'  
    services:  
        <service-name>:  
            image: <image>:<image-version>  
            ports:  
            - 0000:0000
            environment:
            - <environmental-variables>
            ...
        <service-name-2>:  
            image: <image-2>:<image-version>  
            ports:  
            - 0000:0000
            ...

*Using Docker services from a Docker compose file:*

- `docker compose -f <file-name.yaml> up`     <-- to start the containers specified in the file


- `docker compose -f <file-name.yaml> down`     <-- to stop the containers and remove them and the network

For the app to use your own app Image, modify the YAML file to contain the following:  

    version: '3'  
        services:  
            <your-image-name>:  
                image: <image-repository-name>/<your-image-name>:<TAG>

If there are problems running `docker-compose.yaml` file with .env variables:

- `docker compose -f <file-name.yaml> --env-file <path/to/envfile/.env> up`

## ***Dockerfile***

**[DOCS](https://docs.docker.com/reference/dockerfile/#cmd)**

Dockerfile allows to build a **Docker Image** from your own application. Dockerfile itself acts as a blueprint to build a **Docker Image** that would include artifacts (files, scripts) we specified.

    FROM <image>:<image-version>
    
    ENV <environmental-variable-1=variable-1>      
        <environmental-variable-2=variable-2>
        ...

    RUN mkdir -p <container-directory>      <-- option -p allows to create nested directories

    COPY <source> <container-directory>
    COPY . <container-directory>        <-- copy current folder files to <container-directory>

    CMD ["param1", "param2"]        <-- specifies intended commands for the image.

**Notes:**

> **For variables:**  
> It is better to define variables in a more secure way (like in .env file) and then reference them in ENV;
> 
> **For RUN:**  
> RUN command houses Linux commands to execute while creating container using Dockerfile.  
> Can have multiple RUN commands.
> 
> **For CMD:**  
> CMD is an **entrypoint** command. Parameters in CMD are the defaults for an executing container  
> (i.e. start app with these parameters: ...).  
> Only one CMD command can be used; if multiple CMD commands exist, **only the last one** will be executed.

## ***Building Docker Image using Dockerfile***

To build a Docker Image after setting up a Dockerfile:  

`docker build -t <app-image-name>:<TAG> .`    <- `-t` option allows to TAG an image.
                                                `.` here is a location of a Dockerfile  
                                                (current directory of an app where the Dockerfile is contained).

To push Docker Image to DockerHub:

`docker push <your-user-name>/<app-image-name>:<TAG>`

**Note:**

Whenever the **Dockerfile** is adjusted, the **Image** ___MUST___ be rebuilt, because the old Image cannot be overridden.


## ***Using Docker Volumes to keep data after removing/restarting the Docker container (data persistence)***

**[DOCS](https://docs.docker.com/storage/volumes/)**

To keep data, the container's virtual file system is connected to host's file system, so that the files saved in a
container get copied over to the host's side.

**3 Volume Types exist:**

1. `docker run -v <host-directory>:<container-directory>`   <-- this is called '__Host Volume__'. You decide where on the host
                                                                file system the reference is made

example:  
`docker run -v /home/mount/data:/var/lib/mysql/data`


2. `docker run -v <container-directory>`   <-- this is called '__Anonymous Volume__'. For each container a folder is generated  
                                            that gets mounted (automatically by Docker)  
                                            You need to know the path to the folder on the host file system.

example:  
`docker run -v /var/lib/mysql/data`


3. `docker run -v <name>:<container-directory>`   <-- this is called '__Named Volume__'. An improvement on Anonymous Volumes.  
                                                    You specify a name for a folder on the host system.  
                                                    This name is a reference for a container file system.  
                                                    No need to know the path to the folder on the host file system.  
                                                    **Should be used in production!!!**

example:  
`docker run -v name:/var/lib/mysql/data`

`docker run -v name:/var/lib/postgresql/data`


* Volumes in Docker compose example:


    version: '3'  
    services:  
        mongodb:  
            image: mongo  
            ports:  
            -27017:27017  
            volumes:  
            - db-data:/var/lib/mysql/data  

    volumes:  
        db-data  
            driver: local   <-- means that data will be stored locally  


* Docker Volume Locations (`driver: local`)

**Windows:** `C:\ProgramData\docker\volumes\<named-volume or anonymous-volume-reference-hash>\_data`

**Mac/Linux:** `/var/lib/docker/volumes/<named-volume or anonymous-volume-reference-hash>/_data`


**Note:**
\
If there are issues in creating a database:

- Make sure to first use `docker compose down` command;
- Run `docker volume ls` to check on existing volumes;
- Run `docker volume rm <volume-name>` to remove a volume that is causing issues;
- Run `docker compose up` command again to recreate a database.

If an application needs to be able to share files between multiple replicas,  
create volumes with a driver that supports writing files to an external storage system like NFS or Amazon S3.

More info on that **[here](https://docs.docker.com/storage/volumes/#share-data-between-machines)**.

For data **[backup](https://docs.docker.com/storage/volumes/#back-up-restore-or-migrate-data-volumes)**.
#
