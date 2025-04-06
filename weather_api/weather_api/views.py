import requests
import json
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.core.cache import cache

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def weather_api (request,address) :
    try :
        
        data = cache.get(address)
        if not data :

            response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{address}?unitGroup=metric&include=current&key=8KQEGVGDUENDDKAU69BX4C953&contentType=json")
            if response.status_code == 404 :
                return Response({"invalid address provided"},status=400)
            elif response.status_code != 200 :
                return Response({"error": "Error fetching data from the weather service."}, status=response.status_code)
            data = json.loads(response.text)
            cache.set(address, data, timeout=60*5)

        return Response(data)
    except requests.exceptions.RequestException:
        return Response({"error":"Network error. Please check your connection."}, status=503)
    # except Exception as e :
    #     return Response({"error" : f"unexpected error :{str(e)}"},status=500)
