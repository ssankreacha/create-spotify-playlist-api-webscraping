1. Setup
- Ensure you have the required libraries installed by running:
requests, beautifulsoup, spotipy

2. Spotify API Credentials
- Create a Spotify Developer App: Spotify Developer Dashboard
- Set up environment variables for your credentials:
SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET
USERNAME
REDIRECT_URL

3. Authentication
- The code handles OAuth2 login and will create a token.txt file after the first login. 
- Ensure token.txt is ignored in .gitignore for security.
- Once the code is run, you will be asked to login to Spotify, then REDIRECTED to a webpage > Paste this URL into
Python console.

4. Run the Code
- Input the desired date (format: YYYY-MM-DD).
- The script will retrieve the top 100 songs from Billboard for that date and create a Spotify playlist.

5. Important Notes
- Do not share sensitive credentials.
- Modify playlist details as per your preference.
