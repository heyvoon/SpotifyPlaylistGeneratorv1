# Create the .env file to store variables and its values
with open('.env', 'w') as f:
    f.write('SPOTIPY_CLIENT_ID=d055a21d7a5847698a0c510ec8fbc716\n')
    f.write('SPOTIPY_CLIENT_SECRET=e5a7a130a7a2427d91c059356464ef62\n')
    f.write('SPOTIPY_REDIRECT_URI=https://colab.research.google.com/drive/1QbQ3WhGDdgZVlLL6Uof8ezvNc9VbpdGX\n')
print("The .env file has been created.")