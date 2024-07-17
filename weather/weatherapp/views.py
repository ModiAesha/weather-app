from django.shortcuts import render,HttpResponse
import requests
#from .forms import CityForm
#from . models import City
from datetime import datetime, timezone, timedelta
import json

# Create your views here.

def index(request):
    if request.method == "POST":
        city = str(request.POST.get('city'))

        # Enter your "openweathermap.org" API_KEY below
        api_key = "4f4f6c18157823e4fd72fb471585c904"
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        data = requests.get(url).json()

        try:
            if data['cod'] == '404':
                return HttpResponse('{"status": "notfound"}')
            else:
                city_name = data['name']
                country = data.get('sys').get('country', '-')
                ts = data['dt']
                tzone = data['timezone']
                date_time = datetime.fromtimestamp(ts, tz=timezone(timedelta(seconds=tzone))).strftime('%Y-%m-%d')
                temp = int(data['main']['temp'])
                temp_F = format((temp*1.8)+32, '.1f')
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                feels_like = int(data['main']['feels_like'])
                wind = format(data['wind']['speed']*3.6, '.1f')
                visibility = format(data['visibility']/1000, '.2f') 
               

                context = {'status': 'success', 'city': city_name, 'country': country, 'date_time':date_time, 'temp': temp, 'temp_F': temp_F, 'description': description, 'humidity': humidity, 'feels_like': feels_like, 'wind': wind, 'visibility': visibility}
                return HttpResponse(json.dumps(context))
        except:
            return HttpResponse('{"status": "error"}')
            

    return render(request, 'index.html')

# Create your views here.
'''   
def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=39d9180805cd53e7837b932150ba8306'

    #city = 'Ahemdabad'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()
    
    cities = City.objects.all() #return all the cities in the database

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    weather = {}
    try:
      weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
    }
    except KeyError:
    # Handle the error case, for example:
         print(f"Error: API response missing 'main' key for city: {city}")

    weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data}

    return render(request, 'index.html', context) #returns the index.html template'''