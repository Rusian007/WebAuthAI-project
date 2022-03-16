from django.urls import path,include
from vclass.api.views import (
    Teacher_register,
    User_logout,
    Student_register,
    get_class,
    get_class_details,
    make_classroom,
    pdfCreate,
    get_class_peoples,
    get_pdf,
    Check_images_AI
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = "vclass"

urlpatterns = [
    path('registert', Teacher_register, name="teacher-register"),
    path('registers', Student_register, name="student-register"),
    path('login',obtain_auth_token, name="login"),
    path('logout',User_logout, name="logout"),
    path('ClassroomInfo',get_class, name="classroom"),
    path('ClassDetails',get_class_details, name="details"),
    path('ClassMake',make_classroom, name="Class-make"),
    path('PdfUpload',pdfCreate, name="Pdf-upload"),
    path('ClassPeople',get_class_peoples, name="peoples"),
    path('getPdf',get_pdf, name="pdf-return"),
    path('ai',Check_images_AI, name="image-verify"),
    #path('rest-auth/', include('rest_auth.urls')),
]