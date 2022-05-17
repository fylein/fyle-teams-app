# fyle-teams-app #

* Download and install Docker desktop for Mac from [here.](https://www.docker.com/products/docker-desktop)

* Download and install ngrok for Mac from [here](https://ngrok.com/download)

* Once ngrok is installed, run the below command to start ngrok tunnel
    ```
    ngrok http 8000
    ```

* This will spin up a ngrok tunnel with a host name that will proxy slack's API calls to our local server.

## Creating new Teams Dev app for local development ##
1. Get or create your microsoft account - ask from abhishek/jatin (portal access), Or sign up as a developer account
2. Sign in to teams desktop client/go to browser teams....
3. In the teams app store, add the "Developer Portal" and "App Studio" (deprecated but still can be useful)
4. Create your own new app in the "Developer Portal" (Ex - Fyle Dev Jatin)
5. In the newly created app, fill the mandatory fields and save changes
6. Copy "App ID"
7. Go to Developer Portal > Tools > Bot Management > Create a new bot
8. Go to Configure. Add endpoint url (ngrok url/teams/events)
9. Go to Client Secrets. Create a new client secret and save it somewhere safe in local. Copy bot client secretBot ID.
10. Go to App Studio > Capabilities > Bots. Connect existing bot. Set scope as Personal.
11. Get .env creds file from anyone from Team Slack. Update the teams app id, bot id, ... according to your own creds.
12. Go to Teams App store. Install App Studio .
13. Inside this app studio, go to your dev app. Go to Test and distribute. Click on Add .

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

* Ensure that you have services up and running. Then, run the following command to go into interactive-shell of the database service container.
    ```
    docker-compose exec database bash
    ```
    
* And then run the following command to connect to the PostgreSQL DB.
    ```
    PGPASSWORD=teams12345 psql -h localhost -U teams_user teams_db
    ```
