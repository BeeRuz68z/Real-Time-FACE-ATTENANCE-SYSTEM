from django.shortcuts import render,redirect
from .models import *
import os
import cv2
# import numpy as np
# import face_recognition
from datetime import date
from django.shortcuts import render
from django.contrib import messages
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import face_recognition
import numpy as np

# Create your views here.
def index(request):
    if 'email' in request.session:
        a=Register.objects.all()
        la=len(a)
        s=Student.objects.all()
        ls=len(s)
        at=Attendence.objects.all()
        lat=len(at)
        return render(request, 'index.html',{'email':request.session['email'],'staff':la,'student':ls,'attendence':lat})
    else:
        return render(request, 'index.html',{'email':None})

def login(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            a=Register.objects.get(email=email)
            if a.password==password:
                request.session['email']=email
                return redirect('index')
            else:
                a='Incorrect password'
                return render(request, 'authentication-login.html',{'error':a})
        except Exception as e:
            a='Email Does Not Exist'
            return render(request, 'authentication-login.html',{'error':e})
    return render(request,'authentication-login.html')

def register(request):
    if request.method == 'POST':
        fname=request.POST.get('fname')
        dept=request.POST.get('dept')
        stfid=request.POST.get('stfid')
        email=request.POST.get('email')
        password=request.POST.get('password')
        a=Register.objects.all()
        b=[]
        for i in a:
            b.append(i.email)
        if email not in b:
            c=Register(fname=fname,dept=dept, stfid=stfid, email=email, password=password)
            c.save()
            return redirect('register')
        else:
            c='Email already registered'
            return render(request, 'authentication-register.html',{'error':c})
    return render(request,'authentication-register.html')

def logout(request):
    if 'email' in request.session:
        del request.session['email']
        return redirect('index')


def Recognizer(details):
    video = cv2.VideoCapture(0)

    known_face_encodings = []
    known_face_names = []

    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # image_dir = os.path.join(base_dir, "static")
    # image_dir = os.path.join(image_dir, "profile_pics")

    # base_dir = os.getcwd()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # os.chdir("..")
    base_dir = os.getcwd()
    image_dir = os.path.join(base_dir,
                             "{}\{}\{}\{}\{}\{}".format('static', 'images', 'Student_Images', details['branch'],
                                                        details['year'], details['section']))
    # print(image_dir)
    names = []
    for label in os.listdir(image_dir):
        label_path = os.path.join(image_dir, label)
        face_img=face_recognition.load_image_file(label_path)
        face_encoding = face_recognition.face_encodings(face_img)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(label)
    face_locations = []
    face_encodings = []
    #
    while True:
        _, frame = video.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        # rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                nex=os.path.splitext(name)[0]
                face_names.append(nex)
                if name not in names:
                    names.append(name)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left, top), font, 0.8, (255, 255, 255), 1)

        cv2.imshow("Face Recognition Panel", frame)

        if cv2.waitKey(1) == ord('s'):
            break
    #
    video.release()
    cv2.destroyAllWindows()
    return names
def student_details(request):
    if 'email' in request.session:
        branch = Student.BRANCH
        year = Student.YEAR
        section = Student.SECTION
        if request.method == 'POST':
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            registerid=request.POST.get('registerid')
            brn=request.POST.get('brn')
            yr=request.POST.get('yr')
            sec=request.POST.get('sec')
            pro=request.FILES['fileInput']
            password=request.POST.get('password')
            b=[]
            a=Student.objects.all()
            for i in a:
                b.append(i.registerid)
            if registerid not in b:
                c=Student(first_name=fname, last_name=lname,registerid=registerid,branch=brn,year=yr,section=sec,profilepic=pro,password=password)
                c.save()
                return redirect('index')
            else:
                c='registerid already registered'
                print(c)
        return render(request, 'student_details.html', {'email':request.session['email'],'branch':branch, 'year':year, 'section':section})
    else:
        return redirect('login')


def view_student(request):
    if 'email' in request.session:
        a=Student.objects.all()
        return render(request,'table.html',{'email':request.session['email'],'data':a})
    else:
        return redirect('login')


def take_attendance(request):
    if 'email' in request.session:
        branch = Department.BRANCH
        year = Department.YEAR
        section = Department.SECTION
        period=Department.PERIOD
        return render(request,'take_atten.html',{'email':request.session['email'],'branch':branch, 'year':year, 'section':section,'period':period})
    else:
        return redirect('login')


def attendance(request):
    if request.method == 'POST':
        a = Register.objects.get(email=request.session['email'])
        details = {
            'branch': request.POST['brn'],
            'year': request.POST['yr'],
            'section': request.POST['sec'],
            'period': request.POST['per'],
            'faculty': request.session['email']
        }
        att=Attendence.objects.filter(date=str(date.today()), branch=details['branch'], year=details['year'],
                                     section=details['section'], period=details['period'])
        print(att)
        names = Recognizer(details)
        print(names)
        if att.count() != 0:
            namesext = [os.path.splitext(filename)[0] for filename in names]
            print(namesext)
            for i in namesext:
                at=Attendence.objects.filter(date=str(date.today()),Student_ID=str(i),period=details['period'])
                print(bool(at))
                if bool(at) is False:
                    print('hi')
                    attendence = Attendence(faculty=a,
                                            Student_ID=str(i),
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            section=details['section'],
                                            status='Present')
                    attendence.save()
                    attendences = Attendence.objects.filter(date=str(date.today()), branch=details['branch'],
                                                            year=details['year'], section=details['section'],
                                                            period=details['period'])
                    print(attendences)
                    # context = {"attendences": attendences, "ta": True}
                    return render(request, 'viewattendance.html', {"attendences": attendences})
                else:
                    messages.info(request,"already attended..")
                    print('image')
                    return redirect('index')
            return redirect('index')
        else:
            students = Student.objects.filter(branch=details['branch'], year=details['year'],
                                              section=details['section'])
            names = Recognizer(details)
            namesext = [os.path.splitext(filename)[0] for filename in names]
            print(namesext)
            for student in students:
                if str(student.registerid) in namesext:
                    attendence = Attendence(faculty=a,
                                            Student_ID=str(student.registerid),
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            section=details['section'],
                                            status='Present')
                    attendence.save()
                else:
                    attendence = Attendence(faculty=a,
                                            Student_ID=str(student.registerid),
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            section=details['section'])
                    attendence.save()
            attendences = Attendence.objects.filter(date=str(date.today()), branch=details['branch'],
                                                    year=details['year'], section=details['section'],
                                                    period=details['period'])
            print(attendences)
            # context = {"attendences": attendences, "ta": True}
            return render(request, 'viewattendance.html',{"attendences": attendences})
    return redirect('index')
def take_attendance(request):
    if 'email' in request.session:
        branch = Department.BRANCH
        year = Department.YEAR
        section = Department.SECTION
        period=Department.PERIOD
        return render(request,'take_atten.html',{'email':request.session['email'],'branch':branch, 'year':year, 'section':section,'period':period})
    else:
        return redirect('login')


def search_attendance(request):
    if 'email' in request.session:
        return render(request,'search_attendance.html',{'email':request.session['email']})
    else:
        return redirect('login')

def searchtable(request):
    if request.method == 'POST':
        regid = request.POST['search']
        a=Attendence.objects.filter(Student_ID=regid)
        print(a)
        return render(request,'viewattendance.html',{'attendences':a})

def myprofile(request):
    if 'email' in request.session:
        a=Register.objects.get(email=request.session['email'])
        return render(request,'myprofile.html',{'email':request.session['email'],'reg':a})
    else:
        return redirect('login')