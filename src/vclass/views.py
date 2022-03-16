from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Student, User,Teacher,Classroom,Class_Metarials,Questions
from django.views.generic import CreateView
from .forms import(StudentForm,
    TeacherForm,
    loginform,
    classcreation,
    classjoinform,
    ProfileUpdateForm,
    pdfCreateForm,
    questionCreateForm,
) 
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseNotFound
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .functions import get_class,get_user,get_class_and_metarials,convert_to_base64,match_picture
import os


# Create your views here.

def student_view(request):
    name = None
    count = 0
    if request.user.is_authenticated == False:
        return HttpResponseNotFound("Page not found")
    elif request.user.is_Student:
        current_user = request.user
        
        form = classjoinform()
        #student = Student.objects.get(pk=current_user)
        student = get_user(current_user)
        name = student.First_name

        #print(student.image.url)
        try:
            class_ = Classroom.objects.filter(Student=student)
        except:
            class_ = None

        if class_  != None:
            for every in class_:
                count = count+1
                #print(count)

    else:
        return HttpResponse("Page Not Found")

    context = {
        'name' : name,
        'form' : form,
        'class' : class_,
        'student' : student,
        'count' : count
    }
    return render(request,'sign/studentview.html',context)

def teacher_view(request,success=False):
    if request.user.is_authenticated == False:
        return HttpResponseNotFound("Page not found")

    elif request.user.is_Teacher:
        #form = SendEmailForm()
        createform = classcreation()
        current_user = request.user
        class_ = get_class(current_user)
        user = get_user(current_user)
        name = user.First_name
        student_count = {}
        totalsutdents = 0
        totalclass = 0
        if class_  != None:
            for peicode in class_:
                code = peicode.Student.all().count()
                totalsutdents = totalsutdents+code
                a = {peicode : code}
                student_count.update(a)
                totalclass = totalclass+1
                #print(student_count)

        #object=Teacher.objects.get(user_id=current_user.id)
    else:
        return HttpResponseNotFound("Page not found")

    context = {
        'class' : class_,
        'success' : success,
        'form' : createform,
        'student_count' : student_count,
        'name' : name,
        'totalstudent' : totalsutdents,
        'totalclass' : totalclass
    }
    return render(request,'sign/teacherview.html',context)

def mail_sending(request):
    code=None
    if request.method == 'GET':
        code = request.GET.get('code')
        success=False
    if request.method == 'POST':
        code = request.POST.get("Class_code")
        email = request.POST.get("Email")
        if code == None or email == None:
            success = False
            return redirect('portf:teacher-home',success)
        #print(code)
        body = "Hello. Your classroom code is {}. Please join your class.".format(code)
        email = EmailMessage('Classroom | Confirmation', body, to=[email])
        email.send()
        success = True
        return redirect('portf:teacher-home',success)
    current_user = request.user
    class_ = get_class(current_user)
    context = {
        'class' : class_,
        'code' : code
    }
    return render(request, 'sign/mailing.html',context)    



def register(request):
    context = { }
    return render(request, 'sign/register.html', context)



def login_view(request):
    if request.method == 'POST':
        form = loginform(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_Student == True:
                    return redirect('portf:student-home')
                elif request.user.is_Teacher == True:
                    return redirect('portf:teacher-home')
            else:
                print()
                messages.error(request, "Invalid username or password :(")
        else:
            print()
            messages.error(request, "Incorrect username or password :(")
    form = loginform()
    context = {
        "form":form
    }
    return render (request, "sign/login.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)

        return redirect('portf:login')


class student_register(CreateView):
    model = User
    form_class = StudentForm
    template_name = 'sign/student_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        user=form.save()
        #login(self.request,user)
        return redirect('portf:login')


class teacher_register(CreateView):
    model = User
    form_class = TeacherForm
    template_name = 'sign/teacher_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        user=form.save()
        #login(self.request,user)
        return redirect('portf:login')



def Class_create_view(request):
    Unique_code = get_random_string(length=6)

    if request.method == 'POST':
        if request.user.is_authenticated:
                #C_Teacher = User.objects.get(pk=request.user.id)
                Subject = request.POST.get('Subject')
                section = request.POST.get('Section')
                class_name = request.POST.get('Class_Name')
                #Invitation_Code = form.cleaned_data.get('Invitation_Code')
                Invitation_Code = Unique_code
                teacher = Teacher.objects.get(pk=request.user.id)
                new_class = Classroom(Class_name = class_name, Subject=Subject, section=section,
                Invitation_Code=Invitation_Code
                )
                new_class.Teacher = teacher
                new_class.save()
                return redirect('portf:teacher-home')


    elif request.user.is_authenticated:
        form = classcreation()
    elif request.user.is_authenticated == False:
        return HttpResponseNotFound("Page not found")
    context = { 'form' : form, 'code' : Unique_code }


    return render(request,'sign/create.html',context)


def joinclass_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            code = request.POST.get('code')

            #try:
            class_ = get_object_or_404(Classroom, Invitation_Code=code)
             #print(class_)
            student = get_user(request.user)
            #print(class_.pk)
            
            class_.Student.add(student)
            return redirect('portf:student-home')
            #except:
                #return HttpResponse('Wrong Class Code')

    return HttpResponse("Class Joined")

def landing_view(request):
    return render(request,'sign/landing.html')


def Student_class_detail_view(request, my_id):
    user = get_user(request.user)
    current_class = get_object_or_404(Classroom , id=my_id)
    try:
        classes = Classroom.objects.filter(Student = user)
    except:
        return HttpResponse("Invalid Request")
    if current_class in classes:
        context = get_class_and_metarials(request,my_id)
    else:
        return HttpResponse("Class Not Found")
    return render (request,"sign/class.html" , context)


def Teacher_class_detail_view(request, my_id):
    user = get_user(request.user)
    current_class = get_object_or_404(Classroom , id=my_id)
    try:
        classes = Classroom.objects.filter(Teacher = user)
    except:
        return HttpResponse("Invalid Request")
    if current_class in classes:
        context = get_class_and_metarials(request,my_id)
    else:
        return HttpResponse("Class Not Found")
    return render(request,"sign/class.html" ,context)



def Student_profile_view(request):
    current_user = request.user
    student = get_user(current_user)

    context={
        'student' : student,
    }
    return render(request,"sign/studentprofile.html",context)

def Student_update_view(request,pk):

    if request.user.is_authenticated == False:
        return HttpResponseNotFound("Page not found")
        
    student = Student.objects.get(user=pk)
    form= ProfileUpdateForm(instance=student)

    if request.method == 'POST':
        form= ProfileUpdateForm(request.POST,request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('portf:student-profile')
    context={
        'form' : form,
        'student' : student,
    }

    return render(request,'sign/updateView.html',context)

def pdf_create_view(request,my_id):
    classroom = get_object_or_404(Classroom , id=my_id)
    if request.method == 'POST':
        form = pdfCreateForm(request.POST,request.FILES)
        if form.is_valid():
            newObj = form.save(commit=False)
            newObj.Classroom = classroom
            newObj.save()
            return redirect("portf:teacher-class-view",classroom.id)
    else:
        form = pdfCreateForm()
    context ={
        'form' : form
    }
    return render(request,'sign/pdfCreate.html',context)

def people_view(request,my_id):
    context = get_class_and_metarials(request,my_id)
    return render(request,"sign/people.html",context)

def task_view(request,my_id):
    context = get_class_and_metarials(request,my_id)
    return render(request,"sign/task.html",context)

def task_detail_view(request, my_id):
    user = get_user(request.user)
    
    metarials = get_object_or_404(Class_Metarials , pk=my_id)
    classroom = metarials.Classroom
    success = "False"
    context = {
       'metarials' : metarials,
       'class' : classroom,
       'success' : success,
    }
    return render(request,"sign/taskdetail.html",context)

def check_view(request,success, my_id):
    if request.user.is_Student:
        match = match_picture()
        if match:    
            return redirect ("portf:pdf-view",success ,my_id)
        else:
            return render(request,"sign/failed.html")
    if request.user.is_Teacher:
        return redirect ("portf:pdf-view",success ,my_id)

def pdf_view(request, success, my_id):
    form = questionCreateForm()
    metarials = get_object_or_404(Class_Metarials , pk=my_id)
    
    if success == "True":
        show = True
    else:
        show = False  
    #print(checked)
    

    context = {
        'metarial':metarials,
        'form' : form,
        'success' : success,
        'show' : show,
    }
    return render(request, 'sign/pdfviewer.html',context);

def written_question(request,my_id):
    checked = "True"
    if request.user.is_Teacher:
        return HttpResponse("Not allowed")
    else:
        metarials = get_object_or_404(Class_Metarials , pk=my_id)
        student = get_user(request.user)
    if request.method == 'POST':
        form = questionCreateForm(request.POST)
        
        if form.is_valid():
            written = form.cleaned_data.get('Written')
            tag = form.cleaned_data.get('Tag')

            newQ = Questions( Written = written, Tag=tag )
            newQ.Class_Metarials = metarials
            newQ.Student = student
            newQ.save()
            success = "True"
            return redirect('portf:pdf-view',success, metarials.id)
        
    return render(request, 'sign/written_question.html')

def annotaion_view(request,my_id):
    
    if request.user.is_Teacher:
        return HttpResponse("Not allowed")
    else:
        if request.method == 'POST':
            page = request.POST.get('page')
        metarials = get_object_or_404(Class_Metarials , pk=my_id)
        student = get_user(request.user)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        url = BASE_DIR + metarials.Pdf.url
        #print(url)
        encoded = convert_to_base64( url )

        context = {
            'page':page,
            'pdfBase64' : encoded,
            'metarial' : metarials,
        }
    return render(request, 'sign/annotation.html',context)

def recorded_question(request,my_id):
    if request.method == 'POST':
        recording = request.FILES.get('file')
        full = "Not Null"
        newQ = Questions( Voice = recording ,Check=full )
        metarials = get_object_or_404(Class_Metarials , pk=my_id)
        newQ.Class_Metarials = metarials
        student = get_user(request.user)
        newQ.Student = student
        newQ.save()
    return HttpResponse("sent")

def show_questions_view(request):
    if request.user.is_Teacher:
        AllQuestions=[]
        AllClasses = get_class(request.user)

        for eachClass in AllClasses:
            Metarials = Class_Metarials.objects.filter(Classroom = eachClass)
            for metarial in Metarials:
                questions = Questions.objects.filter(Class_Metarials = metarial)
                for question in questions:
                    AllQuestions.append(question)
                    
        context = {
            'questions' : AllQuestions 
        }
        return render(request, 'sign/question.html',context)

    else:
        return HttpResponse("Invalid Request")

