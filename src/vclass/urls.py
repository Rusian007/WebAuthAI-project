from django.urls import path,reverse,include
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from .views import (
     register,
    student_register,
    teacher_register,
    login_view,logout_view,
    Class_create_view,mail_sending,
    landing_view,student_view,teacher_view,
    joinclass_view, Student_class_detail_view,
    Teacher_class_detail_view,
    Student_profile_view,Student_update_view,
    pdf_create_view, people_view,
    task_view,task_detail_view,
    pdf_view, written_question,
    annotaion_view,
    recorded_question,
    check_view,
    show_questions_view
    )

app_name = 'portf'

urlpatterns = [
    path('student', student_view, name= 'student-home'),
    path('teacher', teacher_view, name= 'teacher-home'),
    path('teacher/<success>', teacher_view, name= 'teacher-home'),
    path('register/', register, name= 'register'),
    path('login/', login_view, name= 'login'),
    path('logout/', logout_view, name= 'logout'),
    path('student_register/', student_register.as_view(), name= 'student_register'),
    path('teacher_register/', teacher_register.as_view(), name= 'teacher_register'),
    path('class_create/', Class_create_view, name= 'class_creation'),
    path('class_join/', joinclass_view, name= 'class_join'),
    path('mailing/', mail_sending, name= 'mailing'),
    path('', landing_view, name= 'land'),
    path('Studentclass/<int:my_id>',Student_class_detail_view, name= 'student-class-view'),
    path('teacherclass/<int:my_id>' , Teacher_class_detail_view, name="teacher-class-view"),
    path('profile', Student_profile_view, name="student-profile"),
    path('update/<int:pk>', Student_update_view, name="student-update"),
    path('create/<int:my_id>', pdf_create_view, name="pdf-create"),
    path('people/<int:my_id>', people_view, name="people"),
    path('task/<int:my_id>', task_view, name="task"),
    path('taskdetail/<int:my_id>', task_detail_view, name="task-detail"),
    path('checking/<success>/<int:my_id>/', check_view, name="check"),
    path('viewer/<success>/<int:my_id>/', pdf_view, name="pdf-view"),
    path('written/<int:my_id>', written_question, name="written"),
    path('annotation/<int:my_id>', annotaion_view, name="annote"),
    path('recorded/<int:my_id>', recorded_question, name="recorded"),
    path('questions/', show_questions_view, name="questions"),
]