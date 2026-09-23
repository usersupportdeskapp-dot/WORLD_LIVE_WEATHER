from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(title="World Live Weather API", version="2.0")

CODES={0:"Clear Sky",1:"Mainly Clear",2:"Partly Cloudy",3:"Overcast",45:"Fog",48:"Rime Fog",
51:"Light Drizzle",53:"Moderate Drizzle",55:"Dense Drizzle",56:"Freezing Drizzle",57:"Freezing Drizzle",
61:"Slight Rain",63:"Moderate Rain",65:"Heavy Rain",66:"Freezing Rain",67:"Freezing Rain",
71:"Slight Snow",73:"Moderate Snow",75:"Heavy Snow",77:"Snow Grains",80:"Rain Showers",81:"Rain Showers",
82:"Heavy Rain Showers",85:"Snow Showers",86:"Heavy Snow Showers",95:"Thunderstorm",96:"Thunderstorm with Hail",99:"Thunderstorm with Hail"}

@app.get("/",response_class=HTMLResponse)
def home():
    return open("templates/index.html",encoding="utf-8").read()

@app.get("/api/search")
def search(q:str=Query(...,min_length=2)):
    r=requests.get("https://geocoding-api.open-meteo.com/v1/search",
        params={"name":q,"count":10,"language":"en","format":"json"},timeout=15)
    r.raise_for_status()
    return {"results":[{"id":x.get("id"),"name":x.get("name"),"country":x.get("country"),
        "country_code":x.get("country_code"),"admin1":x.get("admin1",""),
        "latitude":x.get("latitude"),"longitude":x.get("longitude"),
        "timezone":x.get("timezone")} for x in r.json().get("results",[])]}

@app.get("/api/weather")
def weather(latitude:float,longitude:float,name:str="Selected location",country:str=""):
    p={"latitude":latitude,"longitude":longitude,
       "current":["temperature_2m","relative_humidity_2m","apparent_temperature","weather_code",
                  "wind_speed_10m","wind_direction_10m","wind_gusts_10m","precipitation","cloud_cover"],
       "daily":["temperature_2m_max","temperature_2m_min","precipitation_probability_max","weather_code"],
       "forecast_days":7,"timezone":"auto"}
    r=requests.get("https://api.open-meteo.com/v1/forecast",params=p,timeout=15); r.raise_for_status()
    d=r.json(); c=d["current"]
    return {"location":{"name":name,"country":country},"current":{
        "temperature":c.get("temperature_2m"),"humidity":c.get("relative_humidity_2m"),
        "feels_like":c.get("apparent_temperature"),"weather_code":c.get("weather_code"),
        "condition":CODES.get(c.get("weather_code"),"Unknown"),"wind_speed":c.get("wind_speed_10m"),
        "wind_direction":c.get("wind_direction_10m"),"wind_gusts":c.get("wind_gusts_10m"),
        "precipitation":c.get("precipitation"),"cloud_cover":c.get("cloud_cover"),"time":c.get("time")},
        "daily":d.get("daily",{}),"timezone":d.get("timezone")}
