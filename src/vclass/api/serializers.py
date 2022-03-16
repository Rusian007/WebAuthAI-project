from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from vclass.models import Student,Teacher,Class_Metarials,Classroom,image_verify
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import auth
from datetime import date


class StudentRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    Last_name = serializers.CharField(write_only=True)
    Email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required = True)
    Image = serializers.ImageField( )
    class Meta:
        model = User
        fields = ['username', 'password', 'password2','first_name','Last_name','Email','Image']
        extra_kwargs = { 'password' : {'write_only' : True} }

    def save(self):
        password1 = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password2 != password1 :
            raise serializers.ValidationError('Password does not match')
        elif password2 == password1 :
            #user = super().save(commit=False)
            password =  make_password(self.validated_data['password'])
            username = self.validated_data['username']
            user = User.objects.create( )
            user.password = password
            user.username = username
            user.is_Student = True

            user.save()
            student = Student.objects.create(user=user)
            student.Email_address=self.validated_data['Email']
            student.First_name=self.validated_data['first_name']
            student.Last_name= self.validated_data['Last_name']
            student.image = self.validated_data["Image"]
            student.save()

        return user

        
class TeacherRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    Last_name = serializers.CharField(write_only=True)
    Email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required = True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2','first_name','Last_name','Email']
        extra_kwargs = { 'password' : {'write_only' : True} }

    def save(self):
        password1 = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password2 != password1 :
            raise serializers.ValidationError('Password does not match')
        elif password2 == password1 :
            #user = super().save(commit=False)
            password =  make_password(self.validated_data['password'])
            username = self.validated_data['username']
            user = User.objects.create( )
            user.password = password
            user.username = username
            user.is_Teacher = True

            user.save()
            teacher = Teacher.objects.create(user=user)
            teacher.Email_address=self.validated_data['Email']
            teacher.First_name=self.validated_data['first_name']
            teacher.Last_name= self.validated_data['Last_name']
            teacher.save()

        return user

class getClassroomSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)

class getClassIDSerializer(serializers.Serializer):
    ClassId = serializers.IntegerField(write_only=True)
class getMetarialIDSerializer(serializers.Serializer):
    MetarialId = serializers.IntegerField(write_only=True)

class makeClassroomSerilizer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    Subject = serializers.CharField(write_only=True)
    section = serializers.IntegerField(write_only=True)
    Class_name = serializers.CharField(write_only=True)

class pdfCreateSerilizer(serializers.ModelSerializer):
    Pdf = serializers.FileField()
    title = serializers.CharField(max_length=80, write_only=True)
    Description = serializers.CharField(write_only=True)
    #Submit_Date = serializers.DateField(write_only=True)
    Classroom = serializers.IntegerField(write_only=True)

    class Meta:
        model = Class_Metarials
        fields = ['Pdf', 'title', 'Description','Submit_Date','Classroom']

    def save(self):
        classid = self.validated_data['Classroom']
        pdf = self.validated_data["Pdf"]
        title = self.validated_data['title']
        Description = self.validated_data['Description']
        today = date.today()
        date_ = today.strftime("%Y-%m-%d")
        classroom = Classroom.objects.get(id=classid)

        newMetarial = Class_Metarials( title = title ,Pdf=pdf,Description = Description, Submit_Date=date_,Classroom=classroom )
        newMetarial.save()
        return "Saved"


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = image_verify
        fields = ['image']

    def save(self):
        image = self.validated_data["image"];
        verify = image_verify.objects.create(image = image)
        verify.save()
        return verify.id