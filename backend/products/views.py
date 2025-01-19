from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.authentication import TokenAuthentication
from api.mixins import StaffEditorPermissionMixin, UserQuerysetMixin
# from django.http import Http404
from .models import Product
from .serializers import ProductSerializer



class ProductListCreateAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    '''authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
        ] -> added to settings.py file'''
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] # if a user dont have any permissions, it will still be possible to view data in api view
    # even though in admin view it will not be possible to view data
    #overwriting default settings from setting.py
    # dont need permission classes after adding StaffEditorPermissionMixin
    # mixin -> classes with specific functionality from witch other classes inherit
    def perform_create(self, serializer): #overriddiing the function
        #serializer.save(user=self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(user=self.request.user, content = content)
        # send a Django signal
    
    # commended as UserQuerysetMixin is included
    # def get_queryset(self, *args, **kwargs):
    #     '''request = self.request # views definitely have request
    #     #serializer may not have request
    #     print(request.user)
    #     return super().get_queryset(*args, **kwargs)'''
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     return qs.filter(user=request.user)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductCreateAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] 

    def perform_create(self, serializer): #overriddiing the function
        #serializer.save(user=self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(content = content)
        # send a Django signal

product_create_view = ProductCreateAPIView.as_view()

class ProductDetailAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] 
    #lookup_field ='pk' #default befaviuor, uses pk for search


product_detail_view = ProductDetailAPIView.as_view()

class ProductListAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.ListAPIView):
    '''
    not gonna use this method
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] 
    #lookup_field ='pk'


product_list_view = ProductListAPIView.as_view()

class ProductUpdateAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field ='pk'
    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] 

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ##
        
product_update_view = ProductUpdateAPIView.as_view()

class ProductDestroyAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field ='pk'
    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] 

    def perform_destroy(self, instance):
        # instance
        super().perform_destroy(instance)
        
product_destroy_view = ProductDestroyAPIView.as_view()

#the purpose is to show how generics.CreateAPIView
# is created --> CreateAPIView = GenericAPIView + CreateModelMixin
class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
product_mixin_view = ProductMixinView.as_view()

# so, this do the same as generic
# a lot of logic required, it can be confusing
# function views -> flexible (writing from scratch) -> generic view needs modifying
@api_view(['GET', 'POST']) #this do the same as the previous
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method 

    if method == "GET":
        #url_args
        if pk is not None:
            #get request -> detail view
            obj = get_object_or_404(Product, pk = pk)
            data = ProductSerializer(obj).data
            return Response(data)
        #list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    if method == "POST":
        #create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')
            if content is None:
                content = title
            serializer.save(content = content)
            return Response(serializer.data)