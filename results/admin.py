# results/admin.py
from django.contrib import admin
from .models import ExamAttempt, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('question', 'selected_choice')
    can_delete = False

class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'start_time', 'submitted_time', 'get_score')
    list_filter = ('exam', 'student', 'submitted_time')
    search_fields = ('student__username', 'exam__title')
    inlines = [AnswerInline]
    readonly_fields = ('student', 'exam', 'start_time', 'submitted_time')
    
    def get_score(self, obj):
        return f"{obj.calculate_score():.2f}%"
    get_score.short_description = 'Score'

admin.site.register(ExamAttempt, ExamAttemptAdmin)