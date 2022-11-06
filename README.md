# Wazy
Wazy is a bot based on Telegram bot that allows checking travel times using Waze.


## Features
- Check current route travel time.
- Set interval for route travel time checks.
- Get waze navigation url that opens in the application.
- Set maximum travel time and get warning is the travel time exceeds the maximum.
- Configure default rout.
- Configure list of routes.
- Configure addresse.
- Rest API to integrate with other applications/systems.


## Components and Frameworks used in Certi
* [Loguru](https://pypi.org/project/loguru/) For logging.
* [FastAPI](https://github.com/tiangolo/fastapi) For REST API.
* [WazeRouteCalculator](https://github.com/kovacsbalu/WazeRouteCalculator) For interacting with Waze.
* [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/) For the Bot.
* [schedule](https://pypi.org/project/schedule/) For scheduling route checks.


## Installation
Before we can start working with Wazy, we need to create a new telegram bot. 

### Create Telegram bot
How to Create a New Bot for Telegram
Open [Telegram messenger](https://web.telegram.org/), sign in to your account or create a new one.

 Enter @Botfather in the search tab and choose this bot (Official Telegram bots have a blue checkmark beside their name.)

[![@Botfather](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")

Click “Start” to activate BotFather bot.

[![@start](https://github.com/t0mer/voicy/blob/main/screenshots/scr2-min.png?raw=true "@start")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@start")

In response, you receive a list of commands to manage bots.
Choose or type the /newbot command and send it.

[![@newbot](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")


Choose a name for your bot — your subscribers will see it in the conversation. And choose a username for your bot — the bot can be found by its username in searches. The username must be unique and end with the word “bot.”

[![@username](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")


After you choose a suitable name for your bot — the bot is created. You will receive a message with a link to your bot t.me/<bot_username>, recommendations to set up a profile picture, description, and a list of commands to manage your new bot.

[![@bot_username](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")



### Docker

Certi is a docker based application that can be installed using docker compose:
```
version: "3.6"
services:
  wazy:
    image: techblog/wazy
    container_name: wazy
    restart: always
    ports:
      - "8081:8081"
    environment:
      - LOG_LEVEL=DEBUG
    volumes:
      - ./wazy:/app/config
```

### Environment
* LOG_LEVEL - Optional valuse are: DEBUG (default), INFO, ERROR

### Volumes
In order to adapt Wazy to the needs of the user, several things must be defined such as addresses, routes and Telegram API key. Inside the config folder there is a file called config.ini where you can define the necessary parameters for the bot to work.

### Ports
In order to enable integration with other systems, Wazy is also accessible via Rest API. In order to allow access, the port must be defined in the docker-compose file. The default port is 8081.


## Wazy configuration
Wazy can be easily using the config.ini file. by default this file is empty and created on first system start. you can also copy the following content and to new file inside the config folder prior to the containr startup.

```
[Telegram]
bot.token=
bot.allowedid=
bot.welcome.message=Hi, my name is Voicy
bot.enabled=False

[WAZE]
route.avoid_toll_roads=False
route.avoid_subscription_roads=False
route.region=IL
route.start_address=
route.end_address=
route.max_duration=20
routes=['work2home','home2work']
address=['home','work','school','parents']

[work2home]
route.avoid_toll_roads=False
route.avoid_subscription_roads=False
route.start_address=
route.end_address=
rout.max_duration=20

[home2work]
route.avoid_toll_roads=False
route.avoid_subscription_roads=False
route.start_address=
route.end_address=
rout.max_duration=20

[ADRESSES]
address.home=
address.work=
address.parents=
address.school=
```

### Sections:
* Telegram:
    * bot.token: Bot token generated in installation section.
    * bot.welcome.message: Bot welcome message when clicking the start command.
    * bot.enabled: Enables or Disables the bot. default is set to disabled.

* Waze:
    * route.avoid_toll_roads: When true, the waze route calculator will avoid toll roads.
    * route.avoid_subscription_roads: same as above but for subscription roads.
    * route.start_address & route.end_address: setting the default toute to check.
    * routes: List of routes that can be monitored.
    * address: List of addresses that can be set as start and end for routes.

* work2home and home2work - example of pre-configured routes:
* ADDRESSES: Pre-configured addresses that can be set as route start and end points.

## Rest API
As I mentioned, working with Wazy is also possible using the Rest API. API documentation can be found by adding /docs to the server address. For example http://wazy:8081/docs.

[![Wazy rest API](https://github.com/t0mer/Wazy/blob/main/screenshots/wazy.png?raw=true "Wazy rest API")](https://github.com/t0mer/Wazy/blob/main/screenshots/wazy.png?raw=true "Wazy rest API")


