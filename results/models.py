# results/models.py
from django.db import models
from django.conf import settings
from exams.models import Exam, Question, Choice

class ExamAttempt(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_attempts')
    start_time = models.DateTimeField(auto_now_add=True)
    submitted_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['exam', 'student']
        
    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"
    
    def is_completed(self):
        return self.submitted_time is not None
    
    def calculate_score(self):
        total_questions = self.exam.questions.count()
        correct_answers = self.answers.filter(selected_choice__is_correct=True).count()
        return (correct_answers / total_questions) * 100 if total_questions > 0 else 0

class Answer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)  # <-- NEW for essays

    class Meta:
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"Answer to {self.question.text[:50]}"
