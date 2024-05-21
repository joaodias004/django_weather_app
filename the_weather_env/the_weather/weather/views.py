from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

from django.shortcuts import render, get_object_or_404, redirect

def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    city.delete()
    return redirect('index')

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=4ad71bf77fea6b62d9aa2203c9cb22da'

    cities = City.objects.all() #return all the cities in the database

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
        
    form = CityForm()
    
    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        
        weather = {
            'city' : city,
            'temperature' : round((city_weather['main']['temp'] - 32) * 5/9),
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) #returns the index.html template