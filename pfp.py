import requests

# Replace with your bot token and user ID
BOT_TOKEN = 'BOT_TOKEN'
USER_ID = 1234567890

headers = {
    'Authorization': f'Bot {BOT_TOKEN}',
}

response = requests.get(f'https://discord.com/api/v10/users/{USER_ID}', headers=headers)

if response.status_code == 200:
    user_data = response.json()
    avatar_hash = user_data.get('avatar')

    if avatar_hash:
        avatar_url = f'https://cdn.discordapp.com/avatars/{USER_ID}/{avatar_hash}.png?size=128'
        print(f"User's Avatar URL: {avatar_url}")
    else:
        print("User does not have a custom avatar.")
else:
    print("Failed to retrieve user data:", response.status_code)
