# Create the .env file to store variables and its values
with open('.env', 'w') as f:
    f.write('SPOTIPY_CLIENT_ID=d055a21d7a5847698a0c510ec8fbc716\n')
    f.write('SPOTIPY_CLIENT_SECRET=YOUR_SPOTIPY_CLIENT_SECRET\n')
    f.write('SPOTIPY_REDIRECT_URI=YOUR_SPOTIPY_REDIRECT_URI\n')
print("The .env file has been created.")