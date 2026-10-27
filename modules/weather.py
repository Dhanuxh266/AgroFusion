import requests

def get_weather(city, api_key):
    if not city or not api_key:
        return {'ok':False,'error':'Enter a city and OpenWeatherMap API key.'}
    try:
        r=requests.get('https://api.openweathermap.org/data/2.5/weather',params={'q':city,'appid':api_key,'units':'metric'},timeout=8)
        data=r.json()
        if r.status_code != 200: return {'ok':False,'error':data.get('message','Weather request failed.')}
        return {'ok':True,'temperature':data['main']['temp'],'humidity':data['main']['humidity'],
                'rainfall':data.get('rain',{}).get('1h',0),'description':data['weather'][0]['description']}
    except requests.RequestException:
        return {'ok':False,'error':'Could not reach the weather service. Enter weather values manually.'}
