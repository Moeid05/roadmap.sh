from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
import json

class Converter(View):
    def get(self,request):
        return render(request, 'template.html')
    def post(self,request) :
        data = json.loads(request.body)
        mproperty = data['mproperty']
        value = data['value']
        iunit = data['input_unit'].lower()
        ounit = data['output_unit'].lower()
        res = 0
        if mproperty == 'length' :
            units = {
                'centimeter' : 100,
                'meters': 1,
                'kilometers': 0.001,
                'miles': 0.000621371,
                'feet': 3.28084,
                'inches': 39.3701,
            }
            if iunit not in units or ounit not in units:
                raise ValueError("Invalid unit")
            value_in_meters = value / units[iunit]
            res = value_in_meters * units[ounit] 
        elif mproperty == 'weight' :
            units = {
                'grams': 1,
                'kilograms': 0.001,
                'pounds': 0.00220462,
                'ounces': 0.035274,
            }
            if iunit not in units or ounit not in units:
                raise ValueError("Invalid unit")
            value_in_gram = value / units[iunit]
            res = value_in_gram * units[ounit]
        elif mproperty == 'temperature':
            if iunit == 'celsius':
                if ounit == 'fahrenheit':
                    res = (value * 1.8) + 32
                elif ounit == 'kelvin':
                    res = value + 273.15
            elif iunit == 'fahrenheit':
                if ounit == 'celsius':
                    res = (value - 32) / 1.8
                elif ounit == 'kelvin':
                    res = (value - 32) / 1.8 + 273.15
            elif iunit == 'kelvin':
                if ounit == 'celsius':
                    res = value - 273.15
                elif ounit == 'fahrenheit':
                    res = (value - 273.15) * 1.8 + 32
        return JsonResponse({"result" : round(res, 2)})