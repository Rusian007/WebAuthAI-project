from django.core.checks import messages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, logout
from vclass.models import Classroom,Student,Teacher,User,Class_Metarials, image_verify
from vclass.functions import get_user,get_class
from vclass.api.serializers import (
    TeacherRegistrationSerializer,
    StudentRegistrationSerializer,
    getClassroomSerializer,
    getClassIDSerializer,
    makeClassroomSerilizer,
    pdfCreateSerilizer,
    getMetarialIDSerializer,
    ImageSerializer )
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.http import FileResponse
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from classroom.settings import BASE_DIR
import face_recognition
import os, re, os.path,glob


@api_view(['POST', ])
@permission_classes([])
def Teacher_register(request):
    if request.method == 'POST':
        serializer = TeacherRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered new user.'
            #data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)



@api_view(['POST', ])
#@authentication_classes([])
@permission_classes([])
def Student_register(request):
    if request.method == 'POST':
        serializer = StudentRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered new user.'
            #data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')


@api_view(["POST"])
@permission_classes([])
def get_class(request):
    if request.method == 'POST':
        serializer = getClassroomSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
           username = serializer.validated_data.get('username')
           #print(username)
           user = User.objects.get(username = username)

           if (user.is_Student == True):
               student = Student.objects.get(pk=user)
               classes = Classroom.objects.filter(Student=student.pk)
               data = classroomSender(classes)
           
           elif (user.is_Teacher == True):
               teacher = Teacher.objects.get(pk=user)
               classes = Classroom.objects.filter(Teacher=teacher.pk)
               data = classroomSender(classes)


        return Response(data)


def classroomSender(classes):
    data = {}
    count = classes.count()
    data['count'] = count
    if count > 0 :
        key1 = "classname"
        key2 = "subject"
        key3 = "section"
        key4 = "classId"
        data.setdefault(key1, [])
        data.setdefault(key3, [])
        data.setdefault(key2, [])
        data.setdefault(key4, [])
        for class_ in classes:
            classname = class_.Class_name
            subject = class_.Subject
            section = class_.section
            classId = class_.id

            data[key1].append(classname)
            data[key2].append(subject)
            data[key3].append(section)
            data[key4].append(classId)
    return data


@api_view(["POST"])
@permission_classes([])
def get_class_details(request):
    
    data = {}
    serializer = getClassIDSerializer(data=request.data)
    
    if serializer.is_valid():
        my_id = serializer.validated_data.get('ClassId')
        
        classroom = Classroom.objects.get(id=my_id)
        classname = classroom.Class_name

        #students = Student.objects.filter(classroom = classroom)
        #studentcounter = students.count()

        metarials = Class_Metarials.objects.filter(Classroom = classroom)
        count = metarials.count()

        data['count'] = count
        data['classname'] = classname
        if count > 0 :
            key1 = "title"
            key2 = "Submit_Date"
            key3 = "Description"
            key4 = "id"
            data.setdefault(key1, [])
            data.setdefault(key2, [])
            data.setdefault(key3, [])
            data.setdefault(key4, [])
            #print(BASE_DIR)
            

            for metarial in metarials:
                title = metarial.title
                date = metarial.Submit_Date
                description = metarial.Description
                mid = metarial.id
                #url = metarial.Pdf.url
                #file_dir = BASE_DIR + url
                #print(file_dir)
                #pdf_file = open(file_dir, 'rb')
                #response = FileResponse(pdf_file)
                #response = HttpResponse(FileWrapper(pdf_file), content_type='application/pdf')
            
                data[key1].append(title)
                data[key2].append(date)
                data[key3].append(description)
                data[key4].append(mid)
                        
    
    return Response(data)

@api_view(["POST"])
@permission_classes([])
def get_pdf(request):
    data = {}
    serializer = getMetarialIDSerializer(data=request.data)
    my_id = None
    if serializer.is_valid():
        my_id = serializer.validated_data.get('MetarialId')
        #data["my_id"]=my_id
    metarial = Class_Metarials.objects.get(id = my_id)
    url = metarial.Pdf.url
    file_dir = BASE_DIR + url
    pdf_file = open(file_dir, 'rb')
    response = HttpResponse(FileWrapper(pdf_file), content_type='application/pdf')

    return response
    


@api_view(["POST"])
@permission_classes([])
def get_class_peoples(request):
    data = {}
    serializer = getClassIDSerializer(data=request.data)
    if serializer.is_valid():
        my_id = serializer.validated_data.get('ClassId')
        classroom = Classroom.objects.get(id=my_id)
        students = Student.objects.filter(classroom = classroom)

        count = students.count()
        data['counter'] = count
        if count>0:
            key1 = "name"
            key2 = "email"
            data.setdefault(key1, [])
            data.setdefault(key2, [])
            for student in students:
                fname = student.First_name
                lname = student.Last_name
                name = fname + " " + lname
                email = student.Email_address

                data[key1].append(name)
                data[key2].append(email)

    return Response(data)




@api_view(["POST"])
@permission_classes([])
def make_classroom(request):
    Unique_code = get_random_string(length=6)
    data = {}
    serializer = makeClassroomSerilizer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        
        user = User.objects.get(username = username)
        
        if (user.is_Student == True):
            data['Invalid'] = "Invalid"
        elif (user.is_Teacher == True):
            Subject = serializer.validated_data.get('Subject')
            section = serializer.validated_data.get('section')
            class_name = serializer.validated_data.get('Class_name')
            
            Invitation_Code = Unique_code
            teacher = Teacher.objects.get(pk=user.id)
            new_class = Classroom(Class_name = class_name, Subject=Subject, section=section,
                Invitation_Code=Invitation_Code
                )
            new_class.Teacher = teacher
            new_class.save()
            data['Valid'] = "Valid"
        
        
    return Response(data)

@api_view(["POST"])
@permission_classes([])
def pdfCreate(request):
    serializer = pdfCreateSerilizer(data=request.data)
    data = {}
    if serializer.is_valid():
        messages = serializer.save()
        data['Message'] = messages

    return Response(data)

@api_view(["POST"])
@permission_classes([])
def Check_images_AI(request):
    serializer = ImageSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        mid = serializer.save()
        Message = checkimages(mid)
        data['Message'] = Message
    return Response(data)


def checkimages(mid):
    dataResponse = ''
    known_face_encodings = []
    results =[]
    image_dir = os.path.join(BASE_DIR, 'media/avatar/')
    mypath = os.path.join(BASE_DIR, 'media/check/')

    for image_file in glob.glob(os.path.join(image_dir, '*.jpg')):      
        this_face = face_recognition.load_image_file(image_file) 
        this_face_encodings = face_recognition.face_encodings(this_face)[0]
        known_face_encodings += [this_face_encodings]

    obj = image_verify.objects.get(id = mid)
    url = obj.image.url
    Unknownmypath = BASE_DIR + url

    unknown_image = face_recognition.load_image_file(Unknownmypath) 
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

    for face_encoding in known_face_encodings:
        results = face_recognition.compare_faces( known_face_encodings,unknown_face_encoding )


#print(image_dir)
    if True in results:
        print("matched !")
        dataResponse = 'Match'
        for root, dirs, files in os.walk(mypath):
            for file in files:
                os.remove(os.path.join(root, file))
    else:
        print("UnMatched !")
        dataResponse = 'UnMatch'
    
    return dataResponse
    