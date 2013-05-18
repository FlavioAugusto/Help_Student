# -*- coding:utf-8 -*-

# Admin



# Model
from django.contrib import admin

# from help_student.models.student import Student
from help_student.models.matter import Matter
from help_student.models.student_has_matter import StudentHasMatter

admin.site.register(Matter)
# admin.site.register(Student)
admin.site.register(StudentHasMatter)
