# telegram_bill-splitting-calculator-bot
This project is used for creating a telegram bot for the purposes of spilting a bill between a group of people. This telegram bot can be deploy to Heroku and makes use of webhooks for communicating with the telegram API.

## Local Setup
Instructions for setting up and running locally. 
*Note: The commands state here are meant for windows, use the appropriate commands for other OSs.*

### Prerequisite
1. Download and install the latest version of python
2. Create your bot using botfather on telegram and get the access token
3. Download [ngrok](https://ngrok.com/download)
    -   you can place the .exe file in the same working directory of this project

### Configuring The Access Token
Go into configs/config.cfg and paste your token
```
[creds]
token = <ADD ACCESS TOKEN HERE>
```

Next, run the following command to install the necessary python libs to handle the API request and responds 
```
pip install requests bottle
```
*Note: you can also python [virtualenv](https://docs.python.org/3/tutorial/venv.html) which will enable you to create multiple virtual python environments*

### Setting up the Webhook for telegram API
1. We need to start ngrok and get the **https** public IP address that will be forwarding to our localhost server. Run the following command in the directory of ngrok.exe. 
```
ngrok http 5000
```
Copy the *https* public IP address from the output and keep ngrok running. This IP addressed are randomly assigned and they change each time we start and stop ngrok hence we need to maybe need to repeat the set up for the webhook everytime it changes.

2. Next, simple go to your browser and in the input bar enter this
 ```
 https://api.telegram.org/bot<Your Bot Accees Token>/setWebHook?url=https://<Public IP address from ngrok>. 
 ```
 If successfully setup there should be an response with a ok message.

*Note: you can check the status of your webhook with https://api.telegram.org/bot[Your Bot Accees Token]/getWebHookInfo*

### Running the Bot Locally
Finally, we can now run our bot locally. Simple go to the program directory and enter the following command
```
python server.py
```

## Deploying on Heroku

### Prerequisite
1. Have git installed
2. Create a free Heroku account and download and install Heroku cli

### Creating a Heroku web app and setting up of Webhook
1. in your terminal in the same directory as the project, enter the following command
    ```
    heroku login
    ```
    This will log you into your heroku account which will be used for deploying the bot.

2. Next run the follwing command to create the app
    ```
    heroku create 
    ```
    Copy the the https link to your web app from the output.
    *Note: you can use "heroku create <App Name>" to create an app with a given name. Otherwise it will be randomly generated.*
    
3. In your browser, enter the following link to set the Webhook for the bot.
    ```
    https://api.telegram.org/bot<Your Bot Accees Token>/setWebHook?url=https://<your Heroku Web App address>
    ```

### Deploying bot to Heroku
In server.py, the comment for localhost config and remove the commentted for the heroku config as shown below.
```
#app.run(host="localhost", port="5000") ## Used for running locally
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) ## used for running on Heroku
```

Finally, in your terminal in the same directory as the project, enter the following command
```
git commit -m "update to server"
heroku git:remote -a <YourAppName>
git push heroku master
```

If you have not created  your local git repo yet then first run the commands below instead
```
git init
git add .
git commit -m "first commit"
heroku git:remote -a <YourAppName>
git push heroku master
```

Once the finally command has executed, you can head over to your telegram bot and start chatting with it!
*Note: you can use "heroku logs" command in the terminal to view the application logs.*

##### Small notes on how heroku works
1. Heroku will read requirements.txt and installed the libs which are required to execute the program. 
2. It will use Procfile identify the process type and to execute the subsequent command. 