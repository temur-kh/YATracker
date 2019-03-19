from django.contrib import admin


from .models.user import (
        User,
        Student,
        Instructor,
        Admin
        )

admin.site.register([User, Student, Instructor, Admin])
