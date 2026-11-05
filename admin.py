from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']
    list_filter = ['course']

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course', 'order']

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['name']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
