import uuid
import time
import json

import config

from requests.compat import urlencode
from requests import post, put, get
from modules.storage import storage


# Code specific to communicating with the Discord API.

# The following methods all facilitate OAuth2 communication with Discord.
# See https://discord.com/developers/docs/topics/oauth2 for more details.

# Generate the url which the user will be directed to in order to approve the
# bot, and see the list of requested scopes.


class discord():
    def get_oauth_url():
        state = str(uuid.uuid4())

        url = 'https://discord.com/api/oauth2/authorize'
        params = {
            'client_id': config.DISCORD_CLIENT_ID,
            'redirect_uri': config.DISCORD_REDIRECT_URI,
            'response_type': 'code',
            'state': state,
            'scope': 'role_connections.write identify',
            'prompt': 'consent',
        }
        return f'{url}?{urlencode(params)}'



    def get_oauth_tokens(code):
        url = 'https://discord.com/api/v10/oauth2/token'
        body = {
            'client_id': config.DISCORD_CLIENT_ID,
            'client_secret': config.DISCORD_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': config.DISCORD_REDIRECT_URI,
        }

        response = post(url, data=body)
        if response.ok:
            data = response.json()
            return data
        else:
            raise Exception(f'Error fetching OAuth tokens: [{response.status_code}] {response.text}')


    def get_access_token(user_id, tokens):
        if (int(time.time()) > int(tokens['expires_in'])):
            url = 'https://discord.com/api/v10/oauth2/token'
            body = {
                'client_id': config.DISCORD_CLIENT_ID,
                'client_secret': config.DISCORD_CLIENT_SECRET,
                'grant_type': 'refresh_token',
                'refresh_token': tokens['refresh_token'],
            }
            response = post(url, data=body)
            if response.ok:
                tokens = response.json()
                tokens['access_token'] = tokens['access_token']
                tokens['expires_at'] = time.time() + tokens['expires_in']
                storage.store_discord_tokens(user_id, tokens)
                return tokens['access_token']
            else:
                raise Exception(f'Error refreshing access token: [{response.status_code}] {response.text}')
        return tokens['access_token']

    def get_user_data(tokens):
        url = 'https://discord.com/api/v10/oauth2/@me'
        headers = {
            'Authorization': f'Bearer {tokens}',
        }
        response = get(url, headers=headers)
        if response.ok:
            data = response.json()
            return data
        else:
            raise Exception(f'Error fetching user data: [{response.status_code}] {response.text}')

    def push_metadata(user_id, tokens, metadata):
        url = f'https://discord.com/api/v10/users/@me/applications/{config.DISCORD_CLIENT_ID}/role-connection'
        access_token = discord.get_access_token(user_id, tokens)
        body = {
            #這裡是改連結時顯示的名稱
            'platform_name': 'Example Linked Role Discord Bot',
            'metadata': metadata,
        }
        response = put(url, data=json.dumps(body), headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        })
        if not response.ok:
            raise Exception(f'Error pushing discord metadata: [{response.status_code}] {response.text}')

    def get_metadata(user_id, tokens):
        # GET/PUT /users/@me/applications/:id/role-connection
        url = f'https://discord.com/api/v10/users/@me/applications/{config.DISCORD_CLIENT_ID}/role-connection'
        access_token = discord.get_access_token(user_id, tokens)
        response = get(url, headers={'Authorization': f'Bearer {access_token}'})
        if response.ok:
            data = response.json()
            return data
        else:
            raise Exception(f'Error getting discord metadata: [{response.status_code}] {response.text}')
