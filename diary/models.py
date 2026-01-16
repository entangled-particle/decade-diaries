from django.db import models
from django.utils import timezone
from account.models import User


def current_year():
    return timezone.now().year


def current_month():
    return timezone.now().month


class Diary(models.Model):
    title = models.CharField(max_length=200)
    month = models.PositiveSmallIntegerField(
        default=current_month,
        choices=[(i, timezone.datetime(2000, i, 1).strftime("%B"))
                 for i in range(1, 13)],
    )
    year = models.PositiveSmallIntegerField(default=current_year)
    locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Diaries"


class Question(models.Model):
    number = models.PositiveSmallIntegerField(default=0)
    question = models.TextField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"{self.number}. {self.question}"


class Answer(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    file = models.FileField(upload_to='answers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer


class AnswerImage(models.Model):
    """
    Stores one uploaded image for an Answer (supports multiple per answer).
    """

    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="images")
    image = models.FileField(upload_to="answers/images/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"AnswerImage(answer_id={self.answer_id}, id={self.id})"
