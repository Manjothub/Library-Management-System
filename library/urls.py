from django.urls import path
from library .views import *

urlpatterns = [
    path("", index, name="index"),
    path("add_book/", add_book, name="add_book"),
    path("view_books/", view_books, name="view_books"),
    path("view_students/", view_students, name="view_students"),
    path("issue_book/", issue_book, name="issue_book"),
    path("view_issued_book/", view_issued_book, name="view_issued_book"),
    path("student_issued_books/", student_issued_books, name="student_issued_books"),
    path("profile/", profile, name="profile"),
    path("edit_profile/", edit_profile, name="edit_profile"),

    path("student_registration/", student_registration, name="student_registration"),
    path("change_password/",change_password, name="change_password"),
    path("student_login/", student_login, name="student_login"),
    path("admin_login/", admin_login, name="admin_login"),
    path("logout/", Logout, name="logout"),

    path("delete_book/<int:myid>/", delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", delete_student, name="delete_student"),
    
]