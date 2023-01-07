# discord-music-bot
A Discord bot that plays music.

# Before Running...
## Get your credentials ready and setup your environment file
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
           ...
```

### Add all passwords and tokens in the empty *.env* file

The bot supports running in *development mode* or *production mode*.

*Development mode* is for testing the bot out with an alternate account token.

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

If you configured your *.env* file correctly, then it should look something like this:
```
RUN_MODE=prod

DISCORD_TOKEN_DEV=alternate_discord_bot_token_goes_here
DISCORD_TOKEN_PROD=discord_bot_token_goes_here

POSTGRES_USER=place_username_here
POSTGRES_PASSWORD=place_password_here
POSTGRES_DB=place_database_name_here

PGADMIN_DEFAULT_EMAIL=my_actual_email_address@email.com
PGADMIN_DEFAULT_PASSWORD=place_password_here
```

## Next you need to obtain your cookie file from YouTube for use in the bot
One easy way to obtain your cookie file from YouTube, is to use a Chrome extention to do it for you.

*NOTE: I have no association with the author of the extension and can not vouch 100% it wont do something nefarius. You've been warned.*
```
https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid
```

Once installed, go to YouTube and click on the extension:
![image](https://user-images.githubusercontent.com/507320/211168636-95c8c197-e1c6-4528-8b0c-ea2bbb0cce65.png)

Then export the cookies to a text file, like so:
![image](https://user-images.githubusercontent.com/507320/211168666-b7d40b87-2056-4d30-a4a3-d7e0a9d4df38.png)
Finally, save the *youtube.com_cookies.txt* file to your desktop:
![image](https://user-images.githubusercontent.com/507320/211168782-46a092b0-8ad5-4e39-bde7-95832f7ec490.png)

You will need to move this *youtube.com_cookies.txt* file into your bot directory.

Create a new folder called *cookies* under the *app* directory of your bot folder and move your *youtube.com_cookies.txt* file to that new directory, like so:

```
discord-music-bot/
      ├── ...
      ├── docker-compose.yml
      ├── Dockerfile
      ├── requirements.txt
      ├── .env
      └── app/
            ├── cookies/
            |      └── youtube.com_cookies.txt <---- [PLACE FILE HERE]
           ...
```

After, you have done these things, you are ready to run the bot in a Docker container.

# Run The Bot

Once you have setup the bot like detailed in the section before, next open a terminal to the root directory of your bot (*i.e. discord-music-bot/*).

Then simply run the command:

```
docker-compose up
```

Your bot will start the build process, if this is your first time runnig the bot, then it will log into Discord and be ready to accept commands.
