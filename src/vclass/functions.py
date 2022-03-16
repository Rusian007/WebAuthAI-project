from .models import Student,Class_Metarials, User,Teacher,Classroom
from django.shortcuts import get_object_or_404
import base64
import face_recognition
import cv2, os
import numpy as np
from time import sleep
from .models import Student
import glob

def get_class(user):
    if (user.is_Teacher == True):
        teacher = Teacher.objects.get(pk=user)
        class_ = Classroom.objects.filter(Teacher=teacher.pk)
    elif(user.is_Student == True):
        student = Student.objects.get(pk=user)
        class_ = Classroom.objects.filter(Student=student.pk)
    else: 
        class_ = None
    return class_

def get_user (user):
    if(user.is_Teacher == True):
        teacher = Teacher.objects.get(pk=user)
        return teacher
        
    elif(user.is_Student == True):
        student = Student.objects.get(pk=user)
        return student
    

def get_class_and_metarials(request,my_id):
    obj = get_object_or_404(Classroom , id=my_id)
    students = Student.objects.filter(classroom = obj)
    metarials = Class_Metarials.objects.filter(Classroom = obj)
    context ={
        'object': obj,
        'students' : students,
        'metarials' : metarials,
    }
    return context

def convert_to_base64(pdf):
    with open(pdf, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
        
        return encoded_string


def match_picture():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_dir = os.path.join(BASE_DIR, 'media/avatar')

    known_face_encodings = []
    parent_dir = image_dir

    for image_file in glob.glob(os.path.join(parent_dir, '*.jpg')):
        
        this_face = face_recognition.load_image_file(image_file) 
        this_face_encodings = face_recognition.face_encodings(this_face)[0]
        known_face_encodings += [this_face_encodings]

    video_capture = cv2.VideoCapture(0)

    known_face_names = []

    # Create arrays of known face encodings and their names
    students = Student.objects.all()
    for student in students:
        fname = student.First_name
        lname = student.Last_name
        fullname = fname + ' '+ lname
        known_face_names += [fullname]
    

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    sleep(6)
    match = False
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        matches = []
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) and True in matches:
            sleep(2)
            match = True
            break
        # Hit 'q' on the keyboard to quit!
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            match = False
            break

    
    video_capture.release()
    cv2.destroyAllWindows()
    
    return match