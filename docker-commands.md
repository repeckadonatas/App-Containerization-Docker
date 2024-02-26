## ***Basic Docker functions:***

`docker pull <app-name>:<app-version>`  <-- downloads an image of the app from docker

`docker run <app-name>:<app-version>`     <-- run joins pull and start functions into the same function

`docker ps`  <-- lists current running containers

`docker ps -a`  <-- lists all containers (running and stopped)

`docker images`  <-- check images

`docker start <app-ID/app-name>`

`docker stop <app-ID/app-name>`

`docker run -d -p 0000:0000 --name app-name <image>:<image-version>`    <-- `-d` for 'detached mode', `-p` for 'port'

`docker exec -it <container-id> /bin/bash or /bin/sh`    <-- to go inside a container; `-it` means 'interactive terminal'



## ***Docker Compose file***



## ***Dockerfile***



## ***Using Docker Volumes to keep data after removing/restarting the Docker container (data persistence)***

To keep data, the container's virtual file system is connected to host's file system, so that the files saved in a
container get copied over to the host's side.

3 Volume Types exist:

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
####
volumes:  
    db-data  
        driver: local   <-- means that data will be stored locally  


* Docker Volume Locations (driver: local)

**Windows:** C:\ProgramData\docker\volumes\<named-volume or anonymous-volume-reference-hash>\_data
**Mac/Linux:** /var/lib/docker/volumes/<named-volume or anonymous-volume-reference-hash>/_data


## ***Workflow using Docker***
