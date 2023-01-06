# discord-music-bot
A Discord bot that plays music.


# **Installation Requirements (Native System)**

Bot requires Python 3.8.

Install Python dependecies:

```
pip install -r requirements.txt
```

Make sure to add an environment variable with your Discord token called:

```
DISCORD_TOKEN
```

Run bot with command:

```
python app/main.py
```



# **Installation Requirements (Docker)**

Add a *.env* file to the root directory that contains your Discord token.

```
DISCORD_TOKEN=your_discord_token_goes_here
```

Then run in Docker (Docker Compose) by entering the command:
```
docker-compose up
```
