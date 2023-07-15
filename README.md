### 取得Discord Bot App 證書

首先，將你所拿到的機器人資訊填入至 `config.py` 檔案中. 你會需要 Token (`DISCORD_TOKEN`), client ID (`DISCORD_CLIENT_ID`), client secret (`DISCORD_CLIENT_SECRET`). 還有 redirect URI (`DISCORD_REDIRECT_URI`) 以及一個隨機產生的UUID值 (`COOKIE_SECRET`) 
他們在檔案中看起來會像這樣:

```
DISCORD_CLIENT_ID: <your OAuth2 client Id>
DISCORD_CLIENT_SECRET: <your OAuth2 client secret>
DISCORD_TOKEN: <your bot token>
DISCORD_REDIRECT_URI: https://<your-project-url>/discord-oauth-callback
COOKIE_SECRET: <random generated UUID> - already created
```

對於UUID的產生 (`COOKIE_SECRET`), 我們使用以下代碼:

```
uuid.uuid4().hex
```

### Running your app

當你將證書填入完之後，執行以下檔案:

```
python main.py
```

再來，只需一次，你必須在另一個視窗中執行此檔案用於註冊:

```
python register.py
```
