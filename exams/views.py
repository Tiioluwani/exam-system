# exams/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from permit import Permit
import asyncio
import os

from .models import Exam, Question, Choice
from results.models import ExamAttempt, Answer

# Initialize Permit
permit = Permit(token=os.getenv("PERMIT_API_KEY"))


def build_user_data(user):
    """
    Converts Django user object into a dict for Permit SDK
    """
    return {
        "key": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "attributes": {
            "role": user.role
        }
    }


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def student_exams(request):
    now = timezone.now()
    exams = Exam.objects.filter(start_time__lte=now, end_time__gte=now)

    available_exams = []
    for exam in exams:
        user_data = build_user_data(request.user)

        # Debug: show what is being checked
        print(f"[DEBUG PERMIT CHECK] Checking: user_data={user_data}, action='attempt', resource={{'type': 'exam', 'id': '{exam.id}'}}")

        can_attempt = asyncio.run(permit.check(
            user=user_data,
            action="attempt",
            resource={
                "type": "exam",
                "id": str(exam.id),
            }
        ))

        # Debug: show the result
        print(f"[DEBUG PERMIT RESULT] For exam ID {exam.id}: can_attempt={can_attempt}")

        if can_attempt:
            available_exams.append(exam)

    return render(request, 'exams/student_exams.html', {'exams': available_exams})


@login_required
def attempt_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    user_data = build_user_data(request.user)

    # Check permission to attempt
    print(f"[DEBUG PERMIT CHECK] Attempt Exam: user_data={user_data}, action='attempt', resource={{'type': 'exam', 'id': '{exam.id}'}}")

    can_attempt = asyncio.run(permit.check(
        user=user_data,
        action="attempt",
        resource={
            "type": "exam",
            "id": str(exam.id),
        }
    ))

    print(f"[DEBUG PERMIT RESULT] Attempt Exam ID {exam.id}: can_attempt={can_attempt}")

    if not can_attempt:
        return HttpResponseForbidden("You don't have permission to attempt this exam.")

    # Fetch or create attempt
    attempt, created = ExamAttempt.objects.get_or_create(
        exam=exam,
        student=request.user
    )

    questions = exam.questions.prefetch_related('choices')
    question_data = []

    for question in questions:
        answer = attempt.answers.filter(question=question).first()
        question_data.append({
            'question': question,
            'choices': question.choices.all(),
            'answer': answer
        })

    if request.method == 'POST':
        for q in question_data:
            question = q['question']
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                selected_choice = get_object_or_404(Choice, id=selected_choice_id, question=question)
                Answer.objects.update_or_create(
                    attempt=attempt,
                    question=question,
                    defaults={'selected_choice': selected_choice}
                )

        attempt.submitted_time = timezone.now()
        attempt.save()
        return redirect('student_results')

    return render(request, 'exams/attempt_exam.html', {
        'exam': exam,
        'questions': question_data
    })


@login_required
def admin_exams(request):
    exams = Exam.objects.filter(created_by=request.user)
    return render(request, 'exams/admin_exams.html', {'exams': exams})
