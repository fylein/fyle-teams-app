# fyle-teams-app #

* Download and install Docker desktop for Mac from [here.](https://www.docker.com/products/docker-desktop)

* Download and install ngrok for Mac from [here](https://ngrok.com/download)

* Once ngrok is installed, run the below command to start ngrok tunnel
    ```
    ngrok http 8000
    ```

* This will spin up a ngrok tunnel with a host name that will proxy slack's API calls to our local server.

TODO
## Teams app configuration ##


## Local Development ##

## Prerequisites ##

* Create an .env file in the root directory with the following entries:

    ```
    SECRET_KEY=fakedjangosecretkey
    FYLE_CLIENT_ID=fakefyleclientid
    FYLE_CLIENT_SECRET=fakefyleclientsecret
    FYLE_ACCOUNTS_URL=fakefyleaccounturl
    FYLE_BRANCHIO_BASE_URI=fakefylebranchiobaseuri
    TEAMS_APP_ID=faketeamsappid
    TEAMS_BOT_ID=faketeamsbotid
    TEAMS_BOT_PASSWORD=faketeamsapppassowrd
    TEAMS_SERVICE_BASE_URL=aketeamsservicebaseurl
    FYLE_TEAMS_APP_SEGMENT_KEY=fakesegmentkey
    ALLOWED_HOSTS=fakeallowedhosts
    DB_NAME=teams_db
    DB_USER=teams_user
    DB_PASSWORD=teams12345
    DB_HOST=database
    DB_PORT=5432
    ```

### Bringing up via Docker Compose ###

* For a fresh setup run to build images for services
    ```
    docker-compose build
    ```

* Now run to start services
    ```
    docker-compose up
    ```

* No need to build again to run the services, server will automatically restart if there are changes in codebase.

* If any changes are made in `requirements.txt` you'll need to rebuild images
    ```
    docker-compose build
    
    docker-compose up
    ```

* If you want to build and start service in one shot

    ```
    docker-compose up --build
    ```


### Connecting to PostgreSQL DB container ###

* Ensure that you have services up and running. Then run the following command to connect to the PostgreSQL DB.
    ```
    PGPASSWORD=teams12345 psql -h localhost -U teams_user teams_db
    ```