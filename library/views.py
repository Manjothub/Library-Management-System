
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
        image = request.POST.get('bookimg')
        book_pdf = request.POST.get('bookpdf')
        desc = request.POST.get('book_desc')
        publish = request.POST.get('publish_date')
        status = request.POST.get('check') == 'on'
        books = Book.objects.create(name=name, author=author, isbn=isbn,volume=volume,book_image=image,book_src=book_pdf, category=category,description=desc, published_date=publish,availability = status)
        if books is not None:
            messages.success(request,'Book added Successfully')
            books.save()
            return redirect('admin_dashboard')
        else:
            messages.error(request,'Fill all the necessary details')
            return redirect('admin_dashboard')        
    return render(request, "admin/admin_dashboard.html")



@login_required(login_url = '/admin_login')
def get_book(request,id):
    data = Book.objects.filter(id=id).values()
    return JsonResponse({'res': list(data)}, safe=False)

@login_required(login_url = '/admin_login')
def update_book(request):
    if request.method == "POST":
        id = request.POST.get("id")
        instance = Book.objects.get(id=id)
        ins = BookForm(request.POST,  instance=instance)
        if ins.is_valid():
            # ins.save()
            print('valid')
            print(ins)
            messages.success(request, 'Book Updated Successfully')
            return redirect("view_books")
        messages.error(request, 'Book not Updated')
        return redirect("view_books")


@login_required(login_url = '/admin_login')
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
    user = request.user
    student = Student.objects.filter(user=user)
    issuedBooks = IssuedBook.objects.filter(student_name=student[0])
    issuedBooksdata = IssuedBook.objects.filter(student_name=student[0]).count()
    context={
        'issuebooks':issuedBooks,
        'issuedata' :issuedBooksdata
    }
    return render(request,'student/issued_book.html',context)


@login_required(login_url = '/admin_login')
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


@login_required(login_url = '/admin_login')
def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    messages.success(request,'Book Deleted Successfully')
    return redirect("/view_students")

@login_required(login_url = '/admin_login')
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

@login_required(login_url = '/admin_login')
def admin_dashboard(request):
    books = Book.objects.all()
    student = Student.objects.all()
    studentdata = Student.objects.all().count()
    bookdata = Book.objects.all().count()
    
    bookissuedata = IssuedBook.objects.all().count()
    context ={
        'books':books,
        'students':student,
        'data':studentdata,
        'bookdata':bookdata,
        'issuedata':bookissuedata
    }
    return render(request,'admin/admin_dashboard.html',context)

@login_required(login_url = '/student_login')
def student_dashboard(request):
    books = Book.objects.all().count()
    user = request.user
    student = Student.objects.filter(user=user)
    issuedBooksdata = IssuedBook.objects.filter(student_name=student[0]).count()
    context={
        'books':books,
        'issuedBooksdata': issuedBooksdata     
    }
    return render(request,'student/student_dashboard.html',context)

def contactus(request):
    return render(request,'common/contact_us.html')


def student_books_views(request):
    books = Book.objects.all()
    return render(request,'student/view_books.html',{'books':books})