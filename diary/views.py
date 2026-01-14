from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Diary, Question, Answer, AnswerImage
from .forms import DiaryForm


@login_required
def home(request):
    diaries = Diary.objects.all()
    return render(request, 'diary/home.html', {'diaries': diaries})

@login_required
def create(request):
    if request.method == "POST":
        form = DiaryForm(request.POST)
        if form.is_valid():
            diary = form.save()
            # Pre-create blank answers for every question for every active, non-superuser user.
            User = get_user_model()
            users = User.objects.filter(is_superuser=False, is_active=True).only("id")
            questions = Question.objects.all().only("id")
            Answer.objects.bulk_create(
                [
                    Answer(diary=diary, user=u, question=q, answer="")
                    for u in users
                    for q in questions
                ],
                batch_size=1000,
            )
            return redirect("diary:detail", diary_id=diary.id)
    else:
        form = DiaryForm()

    return render(request, "diary/create.html", {"form": form})

@login_required
@require_POST
def save_answer(request, diary_id, question_id):
    """
    Save (create/update) a single answer for the logged-in user.
    """
    if request.user.is_superuser:
        return HttpResponseForbidden("Superusers are not allowed to submit diary answers.")

    diary = get_object_or_404(Diary, id=diary_id)
    if diary.locked:
        return HttpResponseForbidden("This diary is locked.")
    question = get_object_or_404(Question, id=question_id)

    answer_text = request.POST.get("answer", "")
    uploaded_images = request.FILES.getlist("images")

    existing = (
        Answer.objects.filter(diary=diary, user=request.user, question=question)
        .order_by("-updated_at")
        .first()
    )
    if existing:
        existing.answer = answer_text
        existing.save(update_fields=["answer", "updated_at"])
        answer_obj = existing
    else:
        answer_obj = Answer.objects.create(
            diary=diary, user=request.user, question=question, answer=answer_text
        )

    # Append any newly uploaded images (do not delete existing ones).
    if uploaded_images:
        AnswerImage.objects.bulk_create(
            [AnswerImage(answer=answer_obj, image=f) for f in uploaded_images]
        )

    messages.success(request, "Saved.")
    return redirect("diary:detail", diary_id=diary.id)

@login_required
def detail(request, diary_id):
    diary = get_object_or_404(Diary, id=diary_id)

    # Users for this diary (exclude superusers)
    User = get_user_model()
    users = (
        User.objects.filter(is_superuser=False, is_active=True)
        .order_by("first_name", "email")
    )

    # All questions, rendered as rows. Each user becomes a column.
    questions = Question.objects.all()

    # Latest answer per (user, question) for this diary.
    answer_qs = (
        Answer.objects.filter(diary=diary, user__is_superuser=False)
        .select_related("user", "question")
        .prefetch_related("images")
        .order_by("user_id", "question_id", "-updated_at")
    )
    answer_by_pair = {}
    for ans in answer_qs:
        key = (ans.user_id, ans.question_id)
        if key not in answer_by_pair:
            answer_by_pair[key] = ans

    rows = []
    for q in questions:
        cells = [{"user": u, "answer": answer_by_pair.get((u.id, q.id))} for u in users]
        rows.append({"question": q, "cells": cells})

    return render(
        request,
        "diary/detail.html",
        {
            "diary": diary,
            "users": users,
            "rows": rows,
        },
    )