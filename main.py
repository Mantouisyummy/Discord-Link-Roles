import uuid
from modules.discord import discord
from modules.storage import storage
from flask import Flask, make_response, redirect, request



app = Flask(__name__)
app.secret_key = b"random bytes representing flask secret key"
state = str(uuid.uuid4())


@app.route('/')
def hello_world():
    return redirect('/linked-roles')

@app.route('/linked-roles', methods = ['POST', 'GET'])
@app.route('/verified-role', methods = ['POST', 'GET'])
def verified_role():
    res = make_response()
    url = discord.get_oauth_url()
    res.set_cookie('clientState', state)
    return redirect(url)


@app.route('/discord-oauth-callback', methods = ['POST', 'GET'])
def discord_oauth_callback():

    code = request.args['code']

    tokens = discord.get_oauth_tokens(code)


    me_data = discord.get_user_data(tokens['access_token'])
    user_id = me_data['user']['id']
    storage.store_discord_tokens(user_id, tokens)


    update_metadata(user_id)

    return '認證成功!. 請回到Discord查看已連結身分組'


def update_metadata(user_id):
    tokens = storage.get_discord_tokens(user_id)
    metadata = {}
    try:
        #這裡是設定用戶的metadata (可以自己改)
        metadata = {
            'cookieseaten': 3000,
            'allergictonuts': False,
            'firstbaking': '2023-07-14',
        }
    except Exception as e:
        print('Error fetching external data:' + e)

    discord.push_metadata(user_id, tokens, metadata)

if __name__ == '__main__':
    app.run() 
