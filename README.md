# discord-music-bot
A Discord bot that plays music.

# Before Running...
### Obtain your bot token from:
```
https://discord.com/developers/applications
```
### Select your created application and obtain or regenerate your bot token from the "Bot" section:
![image](https://user-images.githubusercontent.com/507320/211165467-1eecb619-b8c3-4999-9dd3-4c09f1fe9b59.png)

### Create a *.env* file
When creating an empty *.env* file make sure not forget to add the DOT in the filename.

![image](https://user-images.githubusercontent.com/507320/211166034-b306ae5b-cea6-4097-84cc-29cc2032e8d0.png)

Place the *.env* file in the root of the bot folder.

```
discord-music-bot/
      ├── ...
      ├── docker-compose.yml
      ├── Dockerfile
      ├── requirements.txt
      ├── .env <---- [PLACE FILE HERE]
      └── app/
            ├── ...
            | 
           ...
```

### Add all passwords and tokens in the empty *.env* file

The bot supports running in *development mode* or *production mode*.

*Development mode* if for testing the bot out with an alternate account token.

*Production mode* is for running the bot normally with the main account token.

Add two entries in the empty *.env* file called *DISCORD_TOKEN_DEV* and *DISCORD_TOKEN_PROD* like so:

```
DISCORD_TOKEN_DEV=alternate_discord_bot_token_goes_here
DISCORD_TOKEN_PROD=discord_bot_token_goes_here
```

If you only care about running the bot normally, then leave the *DISCORD_TOKEN_DEV* entry blank, like so:

```
DISCORD_TOKEN_DEV=
DISCORD_TOKEN_PROD=discord_bot_token_goes_here
```

Next add another entry to the *.env* file called *RUN_MODE* and set it's value to *prod* if running in *production mode*, like so:

```
RUN_MODE=prod
```

If running bot in *development mode*, set *RUN_MODE* to *dev*, like so:

```
RUN_MODE=dev
```

Next add some default credentials for the Postgress database, like so:
```
POSTGRES_USER=place_username_here
POSTGRES_PASSWORD=place_password_here
POSTGRES_DB=place_database_name_here
```

Finally, add default credentials for the PGAdmin website, like so:
```
PGADMIN_DEFAULT_EMAIL=my_actual_email_address@email.com
PGADMIN_DEFAULT_PASSWORD=place_password_here
```
