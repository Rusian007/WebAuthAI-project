from django.test import TestCase
from django.urls import reverse,resolve
from vclass.views import( landing_view,
                        login_view,
                        mail_sending,
                        logout_view,
                        Student_profile_view,
                        people_view,
                        task_view,
                        show_questions_view,
                        register
                        )
from vclass.models import  Teacher,User
# Create your tests here.

class URLTests(TestCase):
    def test_testlandingpage(self):
       url = reverse('portf:land')
       print(resolve(url))
       self.assertEqual(resolve(url).func,landing_view)

    def test_login(self):
       url = reverse('portf:login')
       print(resolve(url))
       self.assertEqual(resolve(url).func,login_view) 

    def test_email(self):
       url = reverse('portf:mailing')
       print(resolve(url))
       self.assertEqual(resolve(url).func,mail_sending) 

    def test_logout(self):
       url = reverse('portf:logout')
       print(resolve(url))
       self.assertEqual(resolve(url).func,logout_view) 


    def test_Student_profile(self):
       url = reverse('portf:student-profile')
       print(resolve(url))
       self.assertEqual(resolve(url).func,Student_profile_view) 

    def test_people_view(self):
       url = reverse('portf:people')
       print(resolve(url))
       self.assertEqual(resolve(url).func,people_view) 

    def test_taskList_view(self):
       url = reverse('portf:task')
       print(resolve(url))
       self.assertEqual(resolve(url).func,task_view) 

    def test_QuestionList_view(self):
       url = reverse('portf:questions')
       print(resolve(url))
       self.assertEqual(resolve(url).func,show_questions_view) 

    def test_register_view(self):
       url = reverse('portf:register')
       print(resolve(url))
       self.assertEqual(resolve(url).func,register) 


class Modeltest(TestCase):
   def setUp(self):
      User.objects.create(username = "timmy")
   
   def teacher_set_up(self):
      user = User.objects.get(id=1)
      Teacher.objects.create(First_name="joker", Last_name="dead",user = user,Email_address="cck@example.com")