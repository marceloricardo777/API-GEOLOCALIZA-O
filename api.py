# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
from flask import Flask
from flask_restful import Resource, Api
import pycep_correios
from geopy.geocoders import Nominatim
import folium
from folium import plugins
from folium.plugins import HeatMap
from flask import request,render_template,make_response
from flask_cors import CORS
import json
app = Flask(__name__)
api = Api(app)
class RenderMap(Resource):
    def post(self):
        try:
            data=json.loads(request.data)
            
            coord=[]
            for x in range(len(data)):
                coord.append([data[x]['lat'], data[x]['long']])
            
            mapa = folium.Map(width='100%', height='100%',location=[-5.087930,-42.800980], zoom_start=13,control_scale=True, prefer_canvas=True)
            HeatMap(coord).add_to(mapa)
            filepath = 'templates/map.html'
            mapa.save(filepath)
            response= make_response()
            headers = {'Access-Control-Allow-Origin': '*'}
            
            return request.url_root+'maparender'
        except ValueError:
            return {'error':ValueError}
   
class ConvertCep(Resource):
    def get(self,cep):
        endereco = pycep_correios.get_address_from_cep(cep)
        geolocator = Nominatim(user_agent="api_teste")
        location = geolocator.geocode('{cidade} - {bairro},'.format( cidade=endereco['cidade'], bairro=endereco['bairro'] ))
        if(location!=None):
                return {'latitude': location.latitude,'longitude':location.longitude}
        else:
            return {'error': True}
        

api.add_resource(ConvertCep, '/<string:cep>')
api.add_resource(RenderMap, '/mapa')
@app.route('/maparender/')
def maprender():
    print(request.url_root)
    return render_template('map.html')
if __name__ == '__main__':
    app.run(debug=False)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/*": {"origins": "*"}})
    
   
