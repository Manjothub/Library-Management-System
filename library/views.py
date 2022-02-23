
from django.http import JsonResponse
from library.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from . forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    return render(request, "common/index.html")

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        category = request.POST.get('category')
        volume = request.POST.get('volume')
        desc = request.POST.get('book_desc')
        publish = request.POST.get('publish_date')
        status = request.POST.get('check') == 'on'
        books = Book.objects.create(name=name, author=author, isbn=isbn,volume=volume, category=category,description=desc, published_date=publish,availability = status)
        books.save()
        print(books)
        # print('okkkkkk')
        alert = True
        return render(request, "admin/admin_dashboard.html", {'alert':alert})
    return render(request, "admin/admin_dashboard.html")

def get_book(request,id):
    data = Book.objects.filter(id=id).values()
    return JsonResponse({'res': list(data)}, safe=False)


def update_book(request):
    if request.method == "POST":
        id = request.POST.get("id")
        instance = Book.objects.get(id=id)
        ins = BookForm(request.POST,  instance=instance)
        if ins.is_valid():
            ins.save()
            messages.success(request, 'Book Updated Successfully')
            return redirect("view_books")
        messages.error(request, 'Book not Updated')
        return redirect("view_books")

def delete_book(request,id):
    books = Book.objects.get(id=id)
    books.delete()
    return redirect("view_books")
@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "admin/view_books.html", {'books':books})

@login_required(login_url = '/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "admin/view_students.html", {'students':students})

@login_required(login_url = '/admin_login')
def issue_book(request):
    if request.method == 'POST':
        book_name=request.POST.get('name')
        author_name=request.POST.get('author')
        student_id= request.POST.get('student_id')
        isbn_number = request.POST.get('isbn')
        book_volume = request.POST.get('volume')
        book_category = request.POST.get('category')
        books = Book.objects.get(id=book_name)
        student = Student.objects.get(id=student_id)
        issuebook = IssuedBook(
            student_name =student,
            book_name =books,
            isbn = isbn_number,
            Volume = book_volume,
            author_name = author_name,
            category = book_category
        )
        if issuebook is not None:
            issuebook.save()
            messages.success(request,'Book Issued Sucessfully')
            return redirect('admin_dashboard')
        else:
            messages.error(request,'Book Issued Failed')
            return redirect('admin_dashboard')
    return render(request, "admin/admin_dashboard.html")

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    return render(request, "admin/view_issued_book.html", {'issuedBooks':issuedBooks})




@login_required(login_url = '/student_login')
def student_issued_books(request):
    # student = Student.objects.filter(user_id=request.user.id)
    # issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    # li1 = []
    # li2 = []

    # for i in issuedBooks:
    #     books = Book.objects.filter(isbn=i.isbn)
    #     for book in books:
    #         t=(request.user.id, request.user.get_full_name, book.name,book.author)
    #         li1.append(t)

    #     days=(date.today()-i.issued_date)
    #     d=days.days
    #     fine=0
    #     if d>15:
    #         day=d-14
    #         fine=day*5
    #     t=(issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
    #     li2.append(t)
    return render(request,'admin/student_issued_books.html')

def admin_profile(request):
    user = User.objects.get(id=request.user.id)
    context ={
        "user":user
    }
    return render(request,'admin/admin_profile.html',context)


@login_required(login_url = '/student_login')
def profile(request):
    return render(request, "student/profile.html")

@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "student/edit_profile.html", {'alert':alert})
    return render(request, "student/edit_profile.html")



def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    messages.success(request,'Book Deleted Successfully')
    return redirect("/view_students")

def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "common/change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "common/change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "common/change_password.html")

def student_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        branch = request.POST.get('branch')
        date_birth=request.POST.get('dob_student')
        gender=request.POST.get('gender')
        roll_no = request.POST.get('roll_no')
        image = request.FILES.get('image')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            passnotmatch = True
            return render(request, "admin/student_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Student.objects.create(user=user, phone=phone, branch=branch,student_dob=date_birth,gender=gender,roll_no=roll_no, image=image)
        
        user.save()
        student.save()
        # alert = True
        return redirect('student_login')
    return render(request, "admin/student_registration.html")

def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("studentdashboard")
        else:
            alert = True
            return render(request, "student/student_login.html", {'alert':alert})
    return render(request, "student/student_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin/admin_login.html", {'alert':alert})
    return render(request, "admin/admin_login.html")

def Logout(request):
    logout(request)
    return redirect ("/")


def admin_dashboard(request):
    books = Book.objects.all()
    student = Student.objects.all()
    studentdata = Student.objects.all().count()
    bookdata = Book .objects.all().count()
    
    bookissuedata = IssuedBook.objects.all().count()
    context ={
        'books':books,
        'students':student,
        'data':studentdata,
        'bookdata':bookdata,
        'issuedata':bookissuedata
    }
    return render(request,'admin/admin_dashboard.html',context)


def student_dashboard(request):
    return render(request,'student/student_dashboard.html')

def contactus(request):
    return render(request,'common/contact_us.html')