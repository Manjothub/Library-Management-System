from django.urls import path
from library .views import *

urlpatterns = [
    path("", index, name="index"),
    path("admin_dashboard/",admin_dashboard,name="admin_dashboard"),
    path("add_book/", add_book, name="add_book"),
    path("books/<int:id>",get_book, name="getbook"),
    path("edit_book/",update_book, name="updatebook"),
    path("view_books/", view_books, name="view_books"),
    path("delete_book/<int:id>/", delete_book, name="deletebook"),
    path("admin_login/", admin_login, name="admin_login"),
    path("delete_student/<int:myid>/", delete_student, name="delete_student"),
    path("view_students/", view_students, name="view_students"),
    path("issue_book/", issue_book, name="issue_book"),
    path("view_issued_book/", view_issued_book, name="view_issued_book"),
    path("admin_profile",admin_profile,name="adminprofile"),
    
    path("student_issued_books/", student_issued_books, name="student_issued_books"),
    path("profile/", profile, name="profile"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("student_registration/", student_registration, name="student_registration"),
    path("change_password/",change_password, name="change_password"),
    path("student_login/", student_login, name="student_login"),

    path("logout/", Logout, name="logout"),

    
    
]