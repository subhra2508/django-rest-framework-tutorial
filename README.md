- GET - INORDER TO GET DATA
- POST - INORDER TO CREATE DATA
- PUT - COMPLETE UPDATE OF THE DATA
- PATCH - PARTIAL UPDATE OF THE DATA
- DELETE - INORDER TO DELETE THE DATA

# django-rest framework

- every row in the model is a object in python
  thses complex datatype needs to be convert into python native datatype ,this process is called
  serialization.

# serializer
complex data type to simple python data type
the reverse is also true

- DRF provides serializer class to serialize and deserialize
  - How to create serializer class
  
```py
from rest_framework import serializers
class ModelNameSerializer(serializers.serializer):
```

- Model Object::serialization-->::python Dict::Render into Json-->::Json Data
- JSONRENDERER is used to render serialized data into json which is understandable by front end
- importing JSONRenderer
- from rest_framework.renderers import JSONRenderer

Render the Data into Json
json_data = JSONRenderer().render(serializer.data)

JsonResponse(data,encoder=DjangoJsonEncoder,safe=True,json_dumps_params=None,\*\*kwargs)

- An httpResponse subclass that helps to create a json-encoded response.It inherits most behavior from its
  superclass with a couple differences:
- Its default content-type header is set to application/json
- The first parameter,data,should be a dict instance.If the safe parameter is set to false it cab be any JSON-serializable object.
- The encoder,which defaults to django.core.serializers.json.DjangoJsonEncoder,will be used to serialie the
  data.
- the safe boolen parameter defaults to True. If it's set to False,any object can be passed for serilization
  (otherwise only dict instances are allowed).If safe is True and a non-dict object is passed as the first argument,
  a TypeError will be raised.

### serializer Field

- serializer fields handle converting between primitive values and internal datatypes.
  They also deal with validating input values,as well as retrieving and setting the values from their parent objects.
- different serializers fields
- CharField(),IntegerField(), etc.
- core arguments
  - label
  - validators
  - error_messages
  - help_text
  - required
  - initial
  - style
    - ```py
      password = serializers.Charfield(
        max_length = 100,
        style ={'input_type':'password','placeholder':'Password'}
      )
      ```
- read_only -> read-only fields are included in the api output but should not be included in the input
  during create or update operations.Any 'read_only' fields that are incorrectly included in the serializer input
  will be ignored .

- write_only - Set this to True to ensure that the field may be used when updating or creating an instance,but is not
  included when serializing the representation .

- allow_null,source

### DESERIALIZATION

json data -> python native data type -> complex data type

BytesIO - A stream implementation using an in-memory bytes buffer.It inherits BufferedIOBase . The buffer is
discarded when the close() method is called .

import io
stream = io.BytesIO(json_data)

JSONParser() - json to python native data type
from rest_framwork.parsers import JSONParser
parsed_data = JSONParser().Parse(stream)

### De-serialization

Deserialization allows parsed data to be converted back into complex types,after first validating the incoming
data.

creating serializer object
serializer = studentSerializer(data = parsed_data)

validate data
serializer.is_valid()

if it is valid then we get the data in
serializer.validated_data

if any error occurs , we get the errors in
serializer.errors

### create data or insert data

```py
from rest_framework import serializers
class StudentSerializer(serializers.Serializer):
  name = serializers.charField(max_length = 100)
  roll = serializers.IntegerField()
  city = serializers.CharField(max_lenght = 100)

  def create(self,validate_data):
    return Student.objects.create(**validate_data)
```

### update data

```py
#partial update , complete update
from rest_framework import serilizers
class StudentSerializer(serializers,Serializer):
  name = serializers.CharFiled(max_length=100)
  roll = serializers.IntegerField()
  city = serilizers.CharField(max_length=100)


  def update(self,instance,validate_data):
    instance.name = validate_data.get('name',instance.name)
    instance.roll = validate_data.get('roll',instance.roll)
    instance.roll = validate_data.get('city',instance.city)
    instance.save()
    return instance
```

```py
# in views.py
# complete update
# By default,serializers must be passed values for all required fields or they will raise validation error
# required all data from front End/client
serializer = StudentSerializer(stu,data=pydata)
if serializer.is_valid():
  serilizer.save()

#for partial update
serializer = StudentSerializer(stu,data=pydata,partial = True)
if serializer.is_valid():
  serilizer.save()

```

# validation

### Field Level validation (single field validation)

- we can specify custom field-level validation by adding validate_fieldName methods to your Serializer subclass
- These are similar to the clean_fieldName methods on django forms
- validate_fieldName methods should return the validated value or raise a serializers.ValidationError
  - syntax:- def validate_fieldname(self,value)
  - Example:- def validate_roll(self,value)
    - where , value is the field value that requires validation

```py
from rest_framework import serializers
class StudentSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100)
  roll = serializers.IntegerField()
  city = serializers.CharField(max_length = 100)

  def validate_roll(self,value): # this method is automatically invoked when is_valid() method is called
    if value >= 200:
      raise serializers.ValidationError("Seat Full")
    return value
```

### object level validation (when we need multiple field validation)
- when we need to do validation that requires access to multiple fields we do object level validation
by adding a method called validate() to serializer subclass
- It raises a serializers.ValidationError if necessary, or just return the validated values
- syntax :- def validate(self,data)
  - def validate(self,data)
    - where , data is a dictionary of field values

```py
from rest_framework import serializers
class StudentSerializer(serializers.Serializer):
  name = serializer.CharField(max_length=100)
  roll = serializer.IntegerField()
  city = serializer.CharField(max_length=100)

  def validate(self,data):
    nm = data.get('name')
    ct = data.get('city')
    if nm.lower() === 'chinu' and ct.lower()!='bbsr':
      raise serializers.ValidationError('city must be bbsr')
    return data
```

# Validators
- Most of the time you're dealing with validation in REST framework you'll simply be relying on the default
field validation , or writing explicit validation methods on serializer or field classes

- However , sometimes you'll want to place your validation logic into reusable components, so that it
can easily be reused throughout your codebase . This can be achieved by using validator function and validator
classes.

### REST framework the validation is performed entirely on the serializer class. This is advantageous for the following reasons :
- It introduce a proper separation of concerns , making your code behavior more obvious.
- It is easy to switch between using shortcut Modelserializer classes and using explicit Serializer classes.Any validation behavior being used for Modelserializer is simple to replicate.
- Printing the repr() of a serializer instance will show you exactly what validation rules it applies. There's no extra hidden validation behavior being called on the model instance .

- When you're using ModelSerializer all of this is handled automatically for you. If you want to drop down to using Serializer classes instead, then you need to define the validation rules explicitly.

```py
from rest_framework import serializers

def start_with_r(value):
  if value['0'].lower()!='r':
    raise serializers.ValidationError('Name should start with R')

class StudentSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100,validators=[start_with_r])
  roll = serializers.IntegerField()
  city = serializers.CharField(max_length=100)

```

# ModelSerializer Class

- The ModelSerializer class provides a shortcut that lets you automatically create a serializer class with fields that correspond to the Model fields.

### The ModelSerializer class is the same as a regular Serializer class , except that:
  - It will automatically generate a set of fields for you,based on the model
  - It will automatically generate validators for the serializer,such as unique_together validators.
  - It includes simple default implementations of create() and update()
```py
from rest_framework import serializers
class StudentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Student
    fields = ['id','name','roll','city']
    #fields ='__all__'
    #exclude = ['roll']
```
### Create ModelSerializer Class

```py
from rest_framework import serializers
class StudentSerializer(serializers.ModelSerializer):
  name = serializers.CharField(read_only=True)
  class Meta:
    model = Student
    fields=['id','name','roll','city']
#OR
# class StudentSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Student
#     fields=['id','name','roll','city']
#     read_only_fields = ['name','roll']
```



### validation would be same as normal serializers validation
```py
from rest_framework import serializers
class StudentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Student
    fields = ['id','name','roll','city']

  def validate_roll(self,value):
    if value >= 200:
      raise serializers.ValidationError('Seat Full')
```

# Function Based api_view

- This wrapper provide a few bits of functionality such as making sure you receive Request instances in your view, and adding context to Response objects so that content negotiation can be performed.

- The wrapper also provide behaviour such as returning 405 Method Not Allowed reponses when appropriate, and handling
any ParseError exceptions that occur when accessing request.data with malformed input.

- By default only GET methods will be accepted. Other methods will respond with "405 Method Not Allowed".
- syntax:
@api_view()


@api_view(['GET','POST','PUT','DELETE'])
def function_name(request):
    pass 

```py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def student_list(request):
  if request.method == 'GET':
    stu = Student.objects.all()
    serializer = StudentSerializer(stu,many=True)
    return Response(serializer.data)
```
```py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def student_create(request):
  if request.method == 'POST':
    serializer = StudentSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      res = {'msg':'Data Created'}
      return Response(res,status=status.HTTP_201_CREATED)
    return Response(serializer.error,status = status.HTTP_400_BAD_REQUEST)
```

- REST framework's Request objects provide flexible request parsing that allows you to treat requests with json data or other media types in the same way that you would normally deal with form data .

- <em>request.data</em> -> request.data returns the parsed content of the request.body. This is similar to the standard request.POST and request.FILES attributes except that:
  - It includes all parsed content,including file and non-file inputs.
  - It supports parsing the content of HTTP methods other than POST,meaning that you can access the content of PUT and PATCH requests.
  - It supports REST framework's flexible request parsing,rather than just supporting form data. For example you can handle incoming JSON data in the same way that you handle incoming form data.

- <em>request.method</em> -> request.method returns the uppercased string representation of the request's HTTP method.
- Browser-based PUT,PATCH and DELETE forms are transparently supported.
-<em>request.query_params</em> -> request.query_params is a more correctly named synonym for request.GET
  - For clarity inside your code,we recommend using request.query_params instead of the Django's standard request.GET. Doing so will help keep your codebase more correct and abvious - any HTTP method type may include query parameters,not just GET requests.

# Response()
- REST framework supports HTTP content negotiation by providing a Response class which allows you to return content that can be rendered into multiple content types,depending on the client request.
- Response objects are initialized with data,which should consist of native python primitives.REST framework then uses standard HTTP content negotiation to determine how it should render the final response content.
- Response class simply provides a nicer interface for returning content-neogotiated Web API responses, that can be rendered to multiple formats.
  - syntax: Response(data,status=None,template_name=None,headers=None,content_type=None)
    - data: The unrendered, serialized data for the response
    - status: A status code for the response.Defaults to 200
    - template_name: A template name to use only if HTMLRenderer or some other custom template renderer is the accepted renderer for the response.
    - headers: A dictionary of HTTP headers to use in the response.
    - content_type: The content type of the response. Typically,this will be set automatically by the renderer as determined by content negotiation,but there may be some cases where you need to specify the content type explicitly.

# CLASS BASED APIVIEW

- REST framework provides an APIView class , which subclass Django's View class. APIView classes are different from regular view classes in the following ways:
  - Requests passed to the handler methods will be REST framework's Request instances,not Django's HttpRequest instances.
  - Handler methods may return REST framework's Response,instead of Django's HttpResponse.The view will manage content negotiation and setting the correct renderer on the response.
  - Incoming requests will be authenticated and appropriate permission and/or throttle checks will be run before dispatching the request to the handler method.

```py
from rest_framework.views import APIView
class StudentAPI(APIView):
  def get(self,request,format=None):
    stu = Student.objects.all()
    serializer = StudentSerializer(stu,many=True)
    return Response(serializer.data)
  
  def post(self,request,format=None):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({'msg':'Data Created'},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
```

# GenericAPIView
- This class extends REST framework's APIView class, adding commonly required behavior for standard list and detail views.
### Attributes
- queryset - The queryset that should be used for returning objects from this view.Typically,you must either set this attribute, or override the get_queryset() method. If you are overriding a view method, it it important that you call get_queryset() instead of accessing this property directly, as queryset will get evaluated once, and those results will be cached for all subsequent requests.

- serializer_class - The serializer class that should be used for validating and deserializing input and for serializing output. Typically, you must either set this attribute,or override the get_serializer_class() method.

- lookup_field - The model field that should be used to for performing object lookup of individual model instances.Defaults to 'pk'.

- lookup_url_kwarg - The URL keyword argument that should be used for object lookup.The URL conf should include a keyword argument corresponding to this value. If unset this defaults to using the same value as lookup_field.

- pagination_class - The pagination class that should be used when paginating list results.Defaults to the same value as the DEFAULT_PAGINATION_CLASS setting, which is 'rest_framework.pagination.PageNumberPagination'.setting pagination_class = None will disable pagination on this view.

- filter_backends - A list of backend classes that should be used for filtering the queryset. Defaults to the same value as the DEFAULT_FILTER_BACKENDS setting.

- Methods - get_queryset(self) - It returns the queryset that should be used for list views,and that should be used as the base for lookups in details views.Defaults to returning the queryset specified by the queryset attribute.

- This method should always be used rather than accessing self.queryset directly, as self.queryset gets evaluated only once, and those results are cached for all subsequent request.

- get_object(self) - It returns an object instance that should be used for detail views.Defaults to using the lookup_field parameter to filter the base queryset.

- get_serializer_class(self) - It returns the class that should be used for the serializer.Defaults to returning the serializer_class attribute.

- get_serializer_context(self) - It returns a dictionary containing any extra context that should be supplied to the serializer.

- get_serializer(self,instance=None,data=None,many=False,partial=False) - It returns a serializer instance.

- get_paginated_response(self,data) - It returns a paginated style Response object

- paginated_queryset(self,queryset) - paginate a queryset if required, either returning a page object, or None if pagination is not configured for this view.

- filter_queryset(self,queryset) - Given a queryset, filter it with whichever filter backend are in use, returning a new queryset.

# MIXINS

- One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behaviour.
- The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any model-backed API views we create.
- Those bits of common behaviour are implemented in REST framework's mixin classes
- The mixin classes provide the actions that are used to provide the basic view
- Note that the mixin classes provide action methods rather than defining the handler methods,such as get() and post(),directly.This allows for more flexible composition of behavior. 

- The mixin classes can be imported from rest_framework.mixins
- ListModelMixin
  - It provides a list(request,*args,**kwargs) method,that implements listing a queryset.
  - If the queryset is populated, this returns a 200 OK response,with a serialized representation of the queryset as the body of the response. The response data may optionally be paginated.

  from rest_framework.mixins import ListModelMixin
  from rest_framework.generics import GenericAPIView

```py
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
class StudentList(ListModelMixin,GenericAPIView):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
  def get(self,request,*args,**kwargs):
    return self.list(request,*args,**kwargs)

```

### Create ModelMixin
It provides a create(request,*args,**kwargs) method,that implements creating and saving a new Model instance.

- If an object is created this returns a 201 Created response, with a serialized representation of the object as the body of the response. If the representation contains a key named url,then the location header of the response will be populated with that value.

- If the request data provided for creating the object was invalid, a 400 Bad Request response will be returned, with the error details as the body of the response.

```py
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
class StudentCreate(CreateModelMixin,GenericAPIView):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
  def post(self,request,*arg,**kwargs):
    return self.create(request,*args,*kwargs)
```
### RetrieveModel Mixin
- It provides a retrieve(request,*args,**kwargs) method , that implements returing an existing model instance in a response.
- If an object can be retrived this return a 200 ok response, with a serialized representation of the object as the body of the response. Otherwise it will return a 404 Not Found.

```py
from rest_framework.mixin import RetrieveModelMixin
from rest_framework.generics import GenericAPIView

class StudentRetrieve(RetrieveModelMixin,GenericAPIView):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
  def get(self,request,*args,**kwargs):
    return self.retrieve(request,*args,**kwargs)

``` 
### UpdateModelMixin

- It provides a update(request,*args,**kwargs) method, that implements updating and saving an existing model instance.
- It also provides a partial_update(request,*args,*kwargs) method, which is similar to the update method, except that all fields for the update will be optional. This allows support for HTTP PATCH requests.
- If an object is updated this return a 200 OK response, with a serialized representation of the object as the body of the response.
- If the request data provided for updating the object was invalid, a 400 Bad Request response will be returned, with the error details as the body of the response.


### DestroyModelMixin

- It provides a destroy(request,*args,**kwargs) method, that implements deletion of an existing model instance.
- If an object is deleted this return a 204 No Content response, otherwise it will return a 404 Not Found.

```py
from rest_framework.mixin import DestroyModelMixin
from rest_framework.generics import GenericAPIView
class StudentDestroy(DestroyModelMixin,GenericAPIView):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
  def delete(self,request,*args,**kwargs):
    return self.destroy(request,*args,**kwargs)
```


# Concrete View Class

- The following classes are the concrete generic views.
- If you're using generic views this is normally the level you'll be working at unless you need heavily customized behavior.
- The view classes can be imported from rest_framework.generics
### ListAPIView
- It is used for read-only endpoints to represent a collection of models instances. It provides a get method handler.
- Extends: GenericAPIView,ListModelMixin
  ```py
    from rest_framework.generics import ListAPIView
    class StudentList(ListAPIView):
      queryset = Student.objects.all()
      serializer_class = StudentSerializer
  ```
### CreateAPIView
- It is used for create-only endpoints.It provides a post method handler.
- Extends:GenericAPIView,CreateModelMixin

```py
from rest_framework.generics import CreateAPIView
class StudentCreate(CreateAPIView):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
```

### RetrieveAPIView
- It is used for update-only endpoints for a single model instance. It provides put and patch method handlers
- Extends:GenericAPIView,UpdateModelMixin
```py
from rest_framework.generics import RetrieveAPIView
class StudentCreate(RetrieveAPIView):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
```

### UpdateAPIView
- It is used for delete-only endpoints for a single model instance.It provides a delete method handler.
- Extends: GenericAPIView,DestroyModelMixin
```py
from rest_framework.generics import UpdateAPIView
class StudentCreate(UpdateAPIView):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
```
# all are in the same way
- DestroyAPIView
- ListCreateAPIView
- RetrieveUpdateAPIView
- RetrieveDestroyAPIView
- RetrieveUpdateDestroyAPIView

# ViewSet

- Django REST framework allows you to combine the logic for a set of related views in a single class , called a ViewSet.
- There are two main advantage of using a ViewSet over using a View class.
  - Repeated logic can be combined into a single class
  - By using routers, we no longer need to deal with wiring up the URL conf ourselves.
### ViewSet Class
- A ViewSet class is simply a type of class-based View, that does not provide any method handlers such as get() or post(), and instead provides actions such as list() and create()
  - list() - Get All Records
  - retrieve() - Get Single Record
  - create() - Create/Insert Record
  - update() - Update Record Completely
  - partial_update() - Update Record Partially
  - destroy() - Delete Record

```py 
from rest_framework import viewsets
class StudentViewSet(viewsets.ViewSet):
  def list(self,request):
    pass
  def create(self,request):
    pass
  def retrieve(self,request,pk=None):
    pass
  def update(self,request,pk=None):
    pass
  def partial_update(self,request,pk=None):
    pass
  def destroy(self,request,pk=None):
    pass
```
- During dispatch,the following attributes are available on the ViewSet:-
  - basename - the base to use for the URL names that are created.
  - action - the name of the current action (e.g list,create).
  - detail - boolean indicating if the current action is configured for a list or detail view
  - suffix - the display suffix for the viewset type - mirrors the details attribute
  - name - the display name for the viewset. This argument is mutually exclusive to suffix
  - description - the display description for the individual view of a viewset.

  for defining router
  - <em>ViewSet-URL Config</em>
```py
from django.urls import path,include
from rest_framework.routers import DefaultRouter
router = DefaultRouter() # Creating Default Router Object
router.register('studentapi',views.StudentViewSet,basename='student') #Register StudentViewSet with Router

urlpatterns = [
  path("",include(router.urls)),# The API URL's are now determined automatically by the router.
]
```

