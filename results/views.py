# results/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from permit import Permit
import os

from .models import ExamAttempt
from exams.models import Exam

# Initialize Permit.io
permit = Permit(token=os.getenv("PERMIT_API_KEY"))


@login_required
def student_results(request):
    attempts = ExamAttempt.objects.filter(
        student=request.user,
        submitted_time__isnull=False
    ).select_related('exam')
    
    results = []
    for attempt in attempts:
        allowed = permit.check(
            user=request.user,
            resource={
                'id': str(attempt.id),
                'type': 'result',
                'attributes': {
                    'student_id': str(attempt.student.id)
                }
            },
            action='read'
        )
        if allowed:
            results.append({
                'attempt': attempt,
                'score': attempt.calculate_score()
            })
    
    return render(request, 'results/student_results.html', {'results': results})


@login_required
def admin_results(request):
    exams = Exam.objects.filter(created_by=request.user)
    
    results = []
    for exam in exams:
        allowed = permit.check(
            user=request.user,
            resource={
                'type': 'result',
                'attributes': {
                    'exam_id': str(exam.id)
                }
            },
            action='read'
        )
        if allowed:
            attempts = ExamAttempt.objects.filter(
                exam=exam,
                submitted_time__isnull=False
            ).select_related('student')
            
            exam_results = []
            for attempt in attempts:
                exam_results.append({
                    'attempt': attempt,
                    'student': attempt.student,
                    'score': attempt.calculate_score()
                })
            
            results.append({
                'exam': exam,
                'attempts': exam_results
            })
    
    return render(request, 'results/admin_results.html', {'results': results})


@login_required
def view_result(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id)
    
    allowed = permit.check(
        user=request.user,
        resource={
            'id': str(attempt.id),
            'type': 'result',
            'attributes': {
                'student_id': str(attempt.student.id),
                'exam_id': str(attempt.exam.id)
            }
        },
        action='read'
    )
    
    if not allowed:
        return HttpResponseForbidden("You do not have permission to view this result.")
    
    answers = attempt.answers.all().select_related('question', 'selected_choice')
    
    return render(request, 'results/view_result.html', {
        'attempt': attempt,
        'answers': answers,
        'score': attempt.calculate_score()
    })
