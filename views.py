from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Choice, Course, Enrollment, Submission

def index(request):
    return render(request, 'onlinecourse/course_list.html', {'courses': Course.objects.all()})

def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related('lesson_set', 'question_set__choice_set'), pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

@login_required
@require_POST
@transaction.atomic
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not course.question_set.exists():
        return HttpResponseBadRequest('This course has no exam yet.')
    raw_ids = [value for key in request.POST if key.startswith('choice_') for value in request.POST.getlist(key)]
    try:
        selected_ids = {int(value) for value in raw_ids}
    except (ValueError, TypeError):
        return HttpResponseBadRequest('Invalid choice.')
    choices = Choice.objects.filter(id__in=selected_ids, question__course=course)
    if set(choices.values_list('id', flat=True)) != selected_ids:
        return HttpResponseBadRequest('A choice does not belong to this course.')
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(choices)
    return redirect('onlinecourse:show_exam_result', course_id=course.pk, submission_id=submission.pk)

@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id, enrollment__course=course, enrollment__user=request.user)
    selected_ids = set(submission.choices.values_list('id', flat=True))
    earned = total = 0
    results = []
    for question in course.question_set.prefetch_related('choice_set').order_by('id'):
        correct = question.is_get_score(selected_ids.intersection(question.choice_set.values_list('id', flat=True)))
        total += question.grade
        earned += question.grade if correct else 0
        results.append({'question': question, 'correct': correct,
            'choices': [{'text': choice.choice_text, 'selected': choice.pk in selected_ids,
                        'correct': choice.is_correct} for choice in question.choice_set.all()]})
    score = round(100 * earned / total, 2) if total else 0
    return render(request, 'onlinecourse/exam_result_bootstrap.html', {
        'course': course, 'submission': submission, 'results': results,
        'earned': earned, 'total': total, 'score': score, 'passed': score >= 70,
    })
