import requests
import json
import config 


url = f'https://discord.com/api/v10/applications/{config.DISCORD_CLIENT_ID}/role-connections/metadata'
# 類型: 數字小於或等於指定值:1, 
# 數字大於或等於指定值:2, 
# 數字等於指定值:3, 
# 數字不等於指定值:4, 
# 日期小於或等於指定值:5, 
# 日期大於或等於指定值:6, 
# 布林值等於指定值:7, 
# 布林值不等於指定值:8
body = [
  {
    'key': 'cookieseaten', #指定的key (填入於main.py 中的49~52行)
    'name': 'Cookies Eaten',
    'description': 'Cookies Eaten Greater Than',
    'type': 2,
  },
  {
    'key': 'allergictonuts',
    'name': 'Allergic To Nuts',
    'description': 'Is Allergic To Nuts',
    'type': 7,
  },
  {
    'key': 'bakingsince',
    'name': 'Baking Since',
    'description': 'Days since baking their first cookie',
    'type': 6,
  },
]

response = requests.put(url, data=json.dumps(body), headers={
  'Content-Type': 'application/json',
  'Authorization': f'Bot {config.DISCORD_TOKEN}',
})
if response.ok:
  data = response.json()
  print(data)
else:
  data = response.text
  print(data)