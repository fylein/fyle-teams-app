# fyle-teams-app #

* Download and install Docker desktop for Mac from [here.](https://www.docker.com/products/docker-desktop)

* Download and install ngrok for Mac from [here](https://ngrok.com/download)

* Once ngrok is installed, run the below command to start ngrok tunnel
    ```
    ngrok http 8000
    ```

* This will spin up a ngrok tunnel with a host name that will proxy slack's API calls to our local server.

## Creating a new Teams Dev app for local development ##
1. Get or create your microsoft account - ask from abhishek/jatin (portal access), Or sign up as a developer account.
2. Sign-in to teams desktop client, Or can also use to ms teams in browser.
4. In Developer Portal, go to Tools > Bot Management > New Bot.
5. Give a name to the bot (Fyle Dev Bot).
6. Inside the bot, go to Configure. Add the Bot endpoint address -> <YOUR_NGROK_URL>/teams/events.
7. Copy the "bot id".
8. Go to Client Secrets > Add a client secret for your bot. Copy the "bot secret" somewhere safe.
9. In Developer Portal, go to Apps. Create your own new app as "Fyle Dev" (can give a name of your choice).
10. In the newly created app, fill the mandatory fields and save changes.
11. Go to App Features > Bot > Identify your bot > Select an existing bot. Select the scope as Personal. 
12. Add these bot commands - "Link Fyle Account", and "Unlink Fyle Account".
13. Inside the app, under Configure, go to Basic Information. Copy "App ID"
14. Get .env creds file from anyone from Team Slack. 
15. Inside .env file, update the TEAMS_APP_ID, TEAMS_BOT_ID, TEAMS_BOT_PASSWORD, TEAMS_SERVICE_BASE_URL (add ngrok url here) according to your local app creds.

## Installing the Teams Dev app on your Microsoft Teams account ## 
16. To install the app, go to Developer Portal, navigate to the 'Apps' menu and identify the app the you just created. Select 'Download app package' from the options menu.
    - A .zip file with the name of your app should start downloading.
17. Now, navigate to the 'Apps' page in the teams sidebar, go to 'Manage Apps' and Upload the .zip file that you just downloaded using the 'Upload an app' button and choosing 'Upload a customized app'.

## Local Development ##

## Prerequisites ##

* Create an .env file in the root directory with the following entries:

    ```
    SECRET_KEY=fakedjangosecretkey
    FYLE_CLIENT_ID=fakefyleclientid
    FYLE_CLIENT_SECRET=fakefyleclientsecret
    FYLE_APP_URL=fakefyleappurl
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

### Commonly faced issues ###
* If you face an error like `psycopg2.errors.UndefinedTable: relation "users" does not exist` while starting the server,
  * Uninstall your Teams Dev app by right clicking on your app from the sidebar and selecting 'Uninstall'.
  * Reinstall the app by following the steps given [here](#installing-the-teams-dev-app-on-your-microsoft-teams-account)
