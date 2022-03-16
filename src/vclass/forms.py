
from django import forms
from django.db.models import fields
from django.forms.widgets import ClearableFileInput, FileInput
from .models import Student,Teacher,User,Classroom,Class_Metarials
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import transaction
from django.forms import ImageField


class StudentForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget= forms.TextInput())
    Last_name = forms.CharField(required=True,widget= forms.TextInput())
    Email = forms.EmailField(required=True,widget= forms.TextInput())
    Image = forms.ImageField( )
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Student = True

        user.save()
        student = Student.objects.create(user=user)
        student.First_name = self.cleaned_data.get('first_name')
        student.Last_name = self.cleaned_data.get('Last_name')
        student.Email_address=self.cleaned_data.get('Email')
        student.save()
        student.image = self.cleaned_data.get("Image")
        student.save()
        return user

class TeacherForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget= forms.TextInput())
    Last_name = forms.CharField(required=True,widget= forms.TextInput( ))
    Email = forms.EmailField(required=True,widget= forms.TextInput())

    class Meta(UserCreationForm.Meta):
        model = User


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Teacher = True

        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.Email_address=self.cleaned_data.get('Email')
        teacher.First_name=self.cleaned_data.get('first_name')
        teacher.Last_name= self.cleaned_data.get('Last_name')
        teacher.save()
        return user

class loginform (AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(loginform, self).__init__(*args, **kwargs)

    username= forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Enter Your Username',
                           'class' : 'form-control'
                           }))
    password = forms.CharField(widget=forms.PasswordInput (
        attrs={'placeholder' : 'Enter Password','class' : 'form-control'}
    ))

class classcreation(forms.Form):
    Class_Name = forms.CharField(required=True)
    Subject = forms.CharField(required=True)
    Section = forms.IntegerField(required=True)

class classjoinform(forms.Form):
    code = forms.CharField(required=True)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Student
        fields = ['First_name','Last_name','Email_address','image']

class pdfCreateForm(forms.ModelForm):
    Submit_Date= forms.DateField(label='Due Date', widget=forms.SelectDateWidget(
        attrs={'class': "input--style-6"}
    ))
    title = forms.CharField(max_length=80, widget=forms.TextInput(
        attrs={'class' : "input--style-6"}
    ))
    Description = forms.CharField(widget=forms.Textarea(
        attrs={'class' : "textarea--style-6"}
    ))
    
    class Meta:
        model = Class_Metarials
        fields = ('title','Description','Submit_Date','Pdf')

class questionCreateForm(forms.Form):

    Written= forms.CharField(widget=forms.Textarea(attrs={"rows":1, "cols":50, 
        'id' : "input"
    }))
    Tag = forms.CharField(required = False, widget=forms.NumberInput(attrs={
        'id' : 'value',
        'class' : 'hide'
    }))

