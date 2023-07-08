# Create the .env file to store variables and its values in the root of your GDrive.
from google.colab import drive
drive.mount('/content/drive')

with open('/content/drive/MyDrive/.env', 'w') as f:
    f.write('SPOTIPY_CLIENT_ID=YOUR_SPOTIPY_CLIENT_ID\n')
    f.write('SPOTIPY_CLIENT_SECRET=YOUR_SPOTIPY_CLIENT_SECRET\n')
    f.write('SPOTIPY_REDIRECT_URI=YOUR_SPOTIPY_REDIRECT_URI\n')