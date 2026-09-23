WORLD LIVE WEATHER
Run: venv\Scripts\activate.bat
Then: pip install -r requirements.txt
Then: uvicorn main:app --reload
Open: http://127.0.0.1:8000

Search any city worldwide. The app uses Open-Meteo geocoding to find coordinates and its global forecast API for current/7-day weather.
