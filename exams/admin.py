# exams/admin.py
from django.contrib import admin
from .models import Exam, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'exam', 'marks')
    list_filter = ('exam',)
    search_fields = ('text',)

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'duration_minutes', 'created_by')
    list_filter = ('created_by', 'start_time')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)