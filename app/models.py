from django.db import models

# Create your models here.
class Register(models.Model):
    fname=models.CharField(max_length=50)
    dept=models.CharField(max_length=50)
    stfid=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=50)

    def __str__(self):
        return self.email

def student_directory_path(instance, filename):
    name, ext = filename.rsplit(".", 1)
    name = instance.registerid # + "_" + instance.branch + "_" + instance.year + "_" + instance.section
    filename = name +'.'+ ext
    return 'Student_Images/{}/{}/{}/{}'.format(instance.branch,instance.year,instance.section,filename)

class Department(models.Model):
    BRANCH = (
        ('CSE', 'CSE'),
        ('IT', 'IT'),
        ('ECE', 'ECE'),
        ('CHEM', 'CHEM'),
        ('MECH', 'MECH'),
        ('EEE', 'EEE'),
    )
    YEAR = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    SECTION = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    PERIOD=(
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
    )
    branch = models.CharField(max_length=100, null=True, choices=BRANCH)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    section = models.CharField(max_length=100, null=True, choices=SECTION)
    period=models.CharField(max_length=100, null=True, choices=PERIOD)

class Student(models.Model):
    BRANCH = (
        ('CSE', 'CSE'),
        ('IT', 'IT'),
        ('ECE', 'ECE'),
        ('CHEM', 'CHEM'),
        ('MECH', 'MECH'),
        ('EEE', 'EEE'),
    )
    YEAR = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    SECTION = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    registerid=models.CharField(max_length=50)
    branch = models.CharField(max_length=100, null=True, choices=BRANCH)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    section = models.CharField(max_length=100, null=True, choices=SECTION)
    profilepic=models.ImageField(upload_to=student_directory_path,null=True, blank=True)
    password=models.CharField(max_length=100)

    def __str__(self):
        return str(self.registerid)


class Attendence(models.Model):
    faculty = models.ForeignKey(Register, null = True, on_delete= models.SET_NULL)
    # student = models.ForeignKey(Student, null = True, on_delete= models.SET_NULL)
    Student_ID = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add = True, null = True)
    time = models.TimeField(auto_now_add=True, null = True)
    branch = models.CharField(max_length=200, null = True)
    year = models.CharField(max_length=200, null = True)
    section = models.CharField(max_length=200, null = True)
    period = models.CharField(max_length=200, null = True)
    status = models.CharField(max_length=200, null = True, default='Absent')

    def __str__(self):
        return str(self.Student_ID + "_" + str(self.date)+ "_" + str(self.period))