from flask import Blueprint, render_template,request, jsonify
from flask_login import login_required, current_user
import requests,json
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/', methods=['POST'])
@login_required
def weather():
    city = request.form.get('city')
    apikey = "f8688fed4fda89bce7d8714768eb4989"
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + apikey
    resp = requests.get(url)
    resp = resp.json()
    #dic = json.loads(resp)
    if("main" in resp):

      temp = str(round(float(resp["main"]["temp"]) - 273.15,2)) +" °C"
      humid = str(resp["main"]["humidity"]) + " %"
      pressure = str(resp["main"]["pressure"]) + " mmHG"
      speed = str(resp["wind"]["speed"]) + " m/s"
      country = str(resp["sys"]["country"]) 
      return render_template('index.html', city=city,temp=temp, humid = humid, pressure=pressure, speed = speed,country=country,error="no")
    else:
       return render_template('index.html', city=city,error="yes")  

    