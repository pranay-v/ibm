from flask import Blueprint, render_template,request, jsonify,Response
from flask_login import login_required, current_user
import requests,json
from . import db
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64
import urllib
import logging
import matplotlib
matplotlib.use('Agg')
from matplotlib.ticker import MaxNLocator
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

@main.route('/statistics')
@login_required
def stats():
    return render_template('statistics.html', name=current_user.name)

@main.route('/statistics',methods=['POST'])
@login_required
def state_wise_details():
    
    if request.form.get('first') == 'State Wise Production Capacity as of 2021':
        

        data = requests.get('https://api.data.gov.in/resource/25f042e3-0a9b-4874-a5e6-43bdacee2325?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset=0&limit=10')

        dicti = data.json()
        xarr =['Andhra_Pradesh', 'Gujarat', 'Karnataka', 'Kerala', 'Madhya_Pradesh', 'Maharashtra', 'Rajasthan', 'Tamil_Nadu', 'Telangana', 'Others']
        yarr=[]
        for i in dicti['records']:
           print(i['state'])
           #xarr.append(i['state'])
           yarr.append(i['cumulative_capacity_till_30_06_2021_mw_'])
        
        fig = plt.figure(figsize = (16, 6))
        
        #xarr[0] = 'Andhra_Pradesh'
        #xarr[4] = 'Madhya_Pradesh'
        plt.bar(xarr, yarr, color ='maroon',align='center')
 
        #plt.xlabel("State")
        plt.ylabel("cumulative_capacity_till_30_06_2021(megawatts)")
        plt.title("State-Wise Production Capacity as of 2021")
        plt.plot()
        #plt.xticks(rotation=10, ha='right')
        #plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
        #plt.gca().yaxis.set_major_locator(MaxNLocator(prune='lower'))
    #plt.show()
    
        output = io.BytesIO()
        plt.savefig(output, format='png')
        plt.close()
        output.seek(0)
        plot_url = urllib.parse.quote(base64.b64encode(output.getvalue()).decode('utf-8'))#base64.b64encode(output.getvalue()).decode('utf8')
        
    
    elif request.form.get('second') == 'Wind Generation Growth Over the Years':    
        
        data0 = requests.get('https://api.data.gov.in/resource/7ccec9c7-8530-4126-827f-aee464402e6a?api-key=579b464db66ec23bdd000001221a16751cb141c54c5421d954cc7370%20&format=json')

        dict0 = data0.json()
#print(dict0)
        xarr0 =[]
        yarr0=[]
        print(dict0['records'])
        for i in dict0['records']:
            xarr0.append(i['_year'])
            yarr0.append(i['wind_energy_generation__in_mu_'])


        fig = plt.figure(figsize = (8, 4))
        
        plt.bar(xarr0, yarr0, color ='maroon',align='center')

        plt.ylabel("Energy Generation in Mega Units(MU)")
        plt.title("Energy Production Comparison - 2013/14 vs 20/21")
        plt.plot()

        output = io.BytesIO()
        plt.savefig(output, format='png')
        plt.close()
        output.seek(0)
        plot_url = urllib.parse.quote(base64.b64encode(output.getvalue()).decode('utf-8'))#base64.b64encode(output.getvalue()).decode('utf8')

    elif request.form.get('third') == 'Capacity Growth in India over the Years':    
        
        data2 = requests.get('https://api.data.gov.in/resource/8c55baee-3e42-457f-92c4-a0005e954bcc?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json')
        xarr1 =[]
        yarr1=[]
        xarr1.append('as_on_31_03_2014')
        xarr1.append('as_on_31_08_2020')  
        yarr1.append(21.04)
        yarr1.append(37.99)

        fig = plt.figure(figsize = (8, 4))
        
        plt.bar(xarr1, yarr1, color ='maroon',align='center')

        plt.ylabel("Giga Watts(GW)")
        plt.title("Installed Capacity Comparison - 2014 vs 2020")
        plt.plot()

        output = io.BytesIO()
        plt.savefig(output, format='png')
        plt.close()
        output.seek(0)
        plot_url = urllib.parse.quote(base64.b64encode(output.getvalue()).decode('utf-8'))#base64.b64encode(output.getvalue()).decode('utf8')
    
    elif request.form.get('fourth') == 'Wind Power Generation in TN':   
        data3 = requests.get('https://api.data.gov.in/resource/cd0db9ce-a9c9-41cb-89cc-8f2b8eb2cd10?api-key=579b464db66ec23bdd000001221a16751cb141c54c5421d954cc7370&format=json&offset=0&limit=50')
        dict3=data3.json()
        for i in dict3['records']:
             if i['name_of_state_ut'] == 'Tamil Nadu':
               print(i)
        #dynamically adding values to a list was cumbersome since the field names were convoluted
        #hence after checking the values created lists manually
        xarr2 = ['2014_15','2015_16','2016_17','2017_18','2018_19','2019_20','2020_21']
        yarr2 = [10147.06,7273.23, 11935.26,12358,12600.85,14126.93,13692.16]

        fig = plt.figure(figsize = (10, 5))
        
        plt.bar(xarr2, yarr2, color ='maroon',align='center')

        plt.ylabel("Mega Units(MU)")
        plt.title("Wind Power Generation in TN Over the Years")
        plt.plot()

        output = io.BytesIO()
        plt.savefig(output, format='png')
        plt.close()
        output.seek(0)
        plot_url = urllib.parse.quote(base64.b64encode(output.getvalue()).decode('utf-8'))#base64.b64encode(output.getvalue()).decode('utf8')
    
    return render_template('statistics.html', plot_url=plot_url,img="yes")
        
    
   

    return render_template('statistics.html')