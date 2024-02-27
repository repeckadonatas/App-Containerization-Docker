## ***Workflow using Docker***

1. Develop your app.


2. Create a `docker-compose.yaml` file. Set it up to pull images needed for the app to run from Docker Hub.


3. Create a `Dockerfile`. It **must be named ***Dockerfile*** for it to work properly**. Place this file in a root directory of the app.


4. Commit your project to a VCS (`Git` for example).


5. Build an **Image** and store it in a Docker Repository.
   * log into a repository using `docker login`
   * push an Image using `docker push`


6. Now an Image of your app can be downloaded from a Docker Repository into another machine. Once an Images is run, it will download the necessary images of services needed to run the app from Docker Hub.

   * to pull an **Image** from **PRIVATE** repository, the target machine (i.e. development server) needs to login to that repository first (`docker login`)

   * execute `docker-compose` to create containers specified in a YAML file. This file must be available on the target machine first.


        
