# Create the .env file to store variables and its values in the root of your GDrive.
from google.colab import drive
drive.mount('/content/drive')

with open('/content/drive/MyDrive/.env', 'w') as f:
    f.write('SPOTIPY_CLIENT_ID=\n')
    f.write('SPOTIPY_CLIENT_SECRET=\n')
    f.write('SPOTIPY_REDIRECT_URI=https://colab.research.google.com/drive/1QbQ3WhGDdgZVlLL6Uof8ezvNc9VbpdGX\n')