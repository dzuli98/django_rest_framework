import json
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    data = request.data
    #print("!!!!!", data)
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save() # creates a new product instance and saves it to database
        #data = serializer.data
        #print("!!!!!!!!!!!", data) only includes given data, or data set to null in model, thats' why price is not inlcuded here
        #print(data)
        #print("!!!!!!!!!", instance.id)
        print(serializer.data)
        return Response(serializer.data)

@api_view(["GET"]) #writing message if the method is not get/dont have to do it manually
def api_home_5(request, *args, **kwargs):
    """
    DRF API VIEW
    """
    instance = Product.objects.all().order_by("?").first()
    data = {}
    if instance:
        '''
        one of the main reasons to use drf
        data serialization -> clean
        enrichment of serializers easily 
        serializers -> how to change representation of data
        multiple serializers for the same model
        '''
        data = ProductSerializer(instance).data
    return Response(data)

@api_view(["GET"]) #writing message if the method is not get/dont have to do it manually
def api_home_4(request, *args, **kwargs):
    """
    DRF API VIEW
    """
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields = ["id", "title", "price", "sale_price"])
    return Response(data)

def api_home_3(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields = ["id", "title"])
    return JsonResponse(data)

def api_home_2(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data['id'] = model_data.id
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price
        # model instance (model_data)
        # turn a Python dict
        # return Json
    return JsonResponse(data)

def api_home_1(request, *args, **kwargs):
    # request -> HttpRequest -> Django
    # request.body
    #print("!!!!!", request.scheme)
    #print("!!!!!", request.body)
    #print("!!!!!", request.path)
    #print("!!!!!", request.GET)
    body = request.body #byte string of JSON data
    data = {}
    try:
        data = json.loads(body) # string of Json data -> Python Dict
    except:
        pass
    #print(data)
    #data['headers'] = request.headers
    #print(request.headers)
    data['params'] = dict(request.GET)
    data['content_type'] = request.content_type
    data['headers'] = dict(request.headers)
    return JsonResponse(data)