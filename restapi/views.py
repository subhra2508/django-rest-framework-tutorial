from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


from rest_framework import viewsets

from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoModelPermissions

from rest_framework.authentication import SessionAuthentication


from restapi.custompermissions import MyPermission


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.authentication import JWTAuthentication

# from restapi.custom-auth import CustomAuthentication


# Both the create and list are together becoz they don't want pk


# Model Object - Single Student Data

# def student_details(request, pk):
#     stu = Student.objects.get(id=pk)
#     serializer = StudentSerializer(stu)
#     json_data = JSONRenderer().render(serializer.data)
#     return HttpResponse(json_data, content_type='application/json')


# def student_list(request):
#     stu = Student.objects.all()
#     serializer = StudentSerializer(stu, many=True)
#     json_data = JSONRenderer().render(serializer.data)
#     return HttpResponse(json_data, content_type='application/json')


# @csrf_exempt
# def student_create(request):
#     if request.method == 'POST':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pydata = JSONParser().parse(stream)
#         serializer = StudentSerializer(data=pydata)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Data Created'}
#             # json_data = JSONRenderer().render(res)
#             # return HttpResponse(json_data,content_type='application/json')
#             return JsonResponse(res)
#         return JsonResponse(serializer.errors)


# def student_update(request):
#     pass

# This is the function based view below there is a class based view to the restapis
# @csrf_exempt
# def student_api(request):
#     if request.method == 'GET':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pydata = JSONParser().parse(stream)
#         id = pydata.get('id', None)
#         if id is not None:
#             stu = Student.objects.get(id=id)
#             serializer = StudentSerializer(stu)
#             return JsonResponse(serializer.data, safe=False)
#         stu = Student.objects.all()
#         serializer = StudentSerializer(stu, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     if request.method == 'POST':
#         # incoming data is json so
#         # make it to python
#         # make it to complex type
#         # then insert it to database
#         # send a respon in json
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythonData = JSONParser().parse(stream)
#         serializer = StudentSerializer(data=pythonData)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Data created'}
#             return JsonResponse(res)
#         return JsonResponse(serializer.errors)

#     if request.method == 'PUT':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythonData = JSONParser().parse(stream)
#         id = pythonData.get('id')
#         stu = Student.objects.get(id=id)
#         serializer = StudentSerializer(stu, data=pythonData, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Data updated'}
#             return JsonResponse(res)
#         return JsonResponse(serializer.errors)

#     if request.method == "DELETE":
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythonData = JSONParser().parse(stream)
#         id = pythonData.get('id')
#         stu = Student.objects.get(id=id)
#         stu.delete()
#         res = {'msg': 'Data Deleted'}
#         return JsonResponse(res)

# class based view
# @method_decorator(csrf_exempt, name='dispatch')
# class StudentAPI(View):
#     def get(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             json_data = request.body
#             stream = io.BytesIO(json_data)
#             pydata = JSONParser().parse(stream)
#             id = pydata.get('id', None)
#             if id is not None:
#                 stu = Student.objects.get(id=id)
#                 serializer = StudentSerializer(stu)
#                 return JsonResponse(serializer.data, safe=False)
#             stu = Student.objects.all()
#             serializer = StudentSerializer(stu, many=True)
#             return JsonResponse(serializer.data, safe=False)

#     def post(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             # incoming data is json so
#             # make it to python
#             # make it to complex type
#             # then insert it to database
#             # send a respon in json
#             json_data = request.body
#             stream = io.BytesIO(json_data)
#             pythonData = JSONParser().parse(stream)
#             serializer = StudentSerializer(data=pythonData)
#             if serializer.is_valid():
#                 serializer.save()
#                 res = {'msg': 'Data created'}
#                 return JsonResponse(res)
#             return JsonResponse(serializer.errors)

#     def put(self, request, *args, **kwargs):
#         if request.method == 'PUT':
#             print("put is executed")
#             json_data = request.body
#             stream = io.BytesIO(json_data)
#             pythonData = JSONParser().parse(stream)
#             id = pythonData.get('id')
#             stu = Student.objects.get(id=id)
#             serializer = StudentSerializer(
#                 stu, data=pythonData, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 res = {'msg': 'Data updated'}
#                 return JsonResponse(res)
#             return JsonResponse(serializer.errors)

#     def delete(self, request, *args, **kwargs):
#         if request.method == "DELETE":
#             json_data = request.body
#             stream = io.BytesIO(json_data)
#             pythonData = JSONParser().parse(stream)
#             id = pythonData.get('id')
#             stu = Student.objects.get(id=id)
#             stu.delete()
#             res = {'msg': 'Data Deleted'}
#             return JsonResponse(res)


########################################################
# FUNCTION BASED API VIEWS
########################################################

# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def student_api(request, pk=None):

#     if request.method == 'GET':
#         # id = request.data.get('id')
#         id = pk
#         if id is not None:
#             stu = Student.objects.get(id=id)
#             serializer = StudentSerializer(stu)
#             return Response(serializer.data)
#         stu = Student.objects.all()
#         serializer = StudentSerializer(stu, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'PUT':
#         # id = request.data.get('id')
#         id = pk
#         stu = Student.objects.get(pk=id)
#         serializer = StudentSerializer(stu, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data Updated'})
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#     if request.method == 'PATCH':
#         # id = request.data.get('id')
#         id = pk
#         stu = Student.objects.get(pk=id)
#         serializer = StudentSerializer(stu, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data Updated'})
#         return Response(serializer.errors)

#     if request.method == 'DELETE':
#         # id = request.data.get('id')
#         id = pk
#         stu = Student.objects.get(pk=id)
#         stu.delete()
#         return Response({'msg': 'Data Deleted'})

#######################################################
# CLASSBASED API VIEWS
#######################################################

# class StudentAPI(APIView):
#     def get(self, request, pk=None, format=None):
#         id = pk
#         if id is not None:
#             stu = Student.objects.get(id=id)
#             serializer = StudentSerializer(stu)
#             return Response(serializer.data)
#         stu = Student.objects.all()
#         serializer = StudentSerializer(stu, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk, format=None):
#         id = pk
#         stu = Student.objects.get(pk=id)
#         serializer = StudentSerializer(stu, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data Updated'})
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk, format=None):
#         id = pk
#         stu = Student.objects.get(pk=id)
#         serializer = StudentSerializer(stu, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data Updated'})
#         return Response(serializer.errors)

#     def delete(self, request, pk, format=None):
#         id = pk
#         stu = Student.objects.get(pk=id)
#         stu.delete()
#         return Response({'msg': 'Data Deleted'})

########################################################
# GENERIC APIVIEW AND MODEL MIXIN
########################################################

# class StudentList(GenericAPIView, ListModelMixin):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# class StudentCreate(GenericAPIView, CreateModelMixin):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class StudentRetrive(GenericAPIView, RetrieveModelMixin):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class StudentUpdate(GenericAPIView, UpdateModelMixin):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)


# class StudentDestroy(GenericAPIView, DestroyModelMixin):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# SERVING ALL OF THESE USING 2 URLS , CREATING GROUPS

# class LCStudentAPI(GenericAPIView, ListModelMixin, CreateModelMixin):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# # Retrieve Update and Destroy - PK Required
# class RUDStudentAPI(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class StudentViewSet(viewsets.ViewSet):
#     def list(self, request):
#         stu = Student.objects.all()
#         serializer = StudentSerializer(stu, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         id = pk
#         if id is not None:
#             stu = Student.objects.get(id=id)
#             serializer = StudentSerializer(stu)
#             return Response(serializer.data)

#     def create(self, request):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk):
#         id = pk
#         stu = Student.objects.get(pk=id)
#         serializer = StudentSerializer(stu, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Complete Data Updated'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, pk):
#         id = pk
#         stu = Student.objects.get(pk=id)
#         serializer = StudentSerializer(stu, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Partial Data Updated'})
#         return Response(serializer.errors)

#     def destroy(self, request, pk):
#         id = pk
#         stu = Student.objects.get(id=id)
#         stu.delete()
#         return Response({'msg': 'Data created'})


# ModelViewSet

# class StudentModelViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

# # BASIC AUTHENTICATION
# class StudentModelViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]

# SESSION AUTHENTICATION
# class StudentModelViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     authentication_classes = [SessionAuthentication]
#     # permission_classes = [IsAuthenticated]
#     # permission_classes = [IsAuthenticatedOrReadOnly]
#     # permission_classes = [DjangoModelPermissions]
#     permission_classes = [MyPermission]


# PERMISSIONS AND AUTHENTICATIONS IN FUNCTIONBASEDVIEWS ##########

# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def student_api(request, pk=None):

#     if request.method == 'GET':
#         # id = request.data.get('id')
#         id = pk
#         if id is not None:
#             stu = Student.objects.get(id=id)
#             serializer = StudentSerializer(stu)
#             return Response(serializer.data)
#         stu = Student.objects.all()
#         serializer = StudentSerializer(stu, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'PUT':
#         # id = request.data.get('id')
#         id = pk
#         stu = Student.objects.get(pk=id)
#         serializer = StudentSerializer(stu, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data Updated'})
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#     if request.method == 'PATCH':
#         # id = request.data.get('id')
#         id = pk
#         stu = Student.objects.get(pk=id)
#         serializer = StudentSerializer(stu, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Data Updated'})
#         return Response(serializer.errors)

#     if request.method == 'DELETE':
#         # id = request.data.get('id')
#         id = pk
#         stu = Student.objects.get(pk=id)
#         stu.delete()

########################################################
# Token Authentication
########################################################
# class StudentModelViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]


# # CUSTOM AUTHENTICATION
# class StudentModelViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     authentication_classes = [CustomAuthentication]
#     permission_classes = [IsAuthenticated]

# JWT AUTHENTICATION
class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
