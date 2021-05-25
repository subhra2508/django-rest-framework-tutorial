from rest_framework import serializers
from .models import Student


# validators
# start with r
# def start_with_r(value):
#     if value[0].lower() != 'r':
#         raise serializers.ValidationError('Name must be start with R')
#     return value


# class StudentSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100, validators=[start_with_r])
#     roll = serializers.IntegerField()
#     city = serializers.CharField(max_length=100)

#     def create(self, validate_data):
#         return Student.objects.create(**validate_data)

#     def update(self, instance, validate_data):
#         instance.name = validate_data.get('name', instance.name)
#         print('====data updated=====')
#         instance.roll = validate_data.get('roll', instance.roll)
#         instance.city = validate_data.get('city', instance.city)
#         instance.save()
#         return instance

# FIELD LEVEL VALIDATION
# def validate_roll(self, value):
#     if value >= 200:
#         raise serializers.ValidationError('Seat Full')
#     return value


# # Object Level Validation
# def validate(self, data):
#     nm = data.get('name')
#     ct = data.get('city')
#     if nm.lower() == 'rohit' and ct.lower() != 'ranchi':
#         raise serializers.ValidationError('City must be Ranchi')
#     return data


##########################################################
# Model serializer
##########################################################
# class StudentSerializer(serializers.ModelSerializer):
# def start_with_r(value):
#     if value[0].lower() != 'r':
#         raise serializers.ValidationError('Name must be start with R')
#     return value
# name = serializers.CharField(read_only=True)
# name = serializers.CharField(validators=[start_with_r])

# class Meta:
#     model = Student
#     fields = ['name', 'roll', 'city']
#     # read_only_fields = ['roll', 'name']
#     # extra_kwargs = {'name':{'read_only':True}}

# FIELD LEVEL VALIDATION

# def validate_roll(self, value):
#     if value >= 200:
#         raise serializers.ValidationError('Seat Full')
#     return value

# # Object Level Validation
# def validate(self, data):
#     nm = data.get('name')
#     ct = data.get('city')
#     if nm.lower() == 'rohit' and ct.lower() != 'ranchi':
#         raise serializers.ValidationError('City must be Ranchi')
#     return data

##################################################################
# MODEL SERIALIZER FOR FUNCTION BASED API VIEWS
##################################################################

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
