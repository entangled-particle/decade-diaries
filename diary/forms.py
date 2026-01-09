from django import forms
from django.utils import timezone

from .models import Diary


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ["month", "year", "title"]
        widgets = {
            "month": forms.Select(attrs={"class": "form-select"}),
            "year": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. December 2026",
                    "autofocus": True,
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        start = now.year - 10
        end = now.year + 10
        year_choices = [(y, y) for y in range(start, end + 1)]
        self.fields["year"].choices = year_choices
        # Ensure the Select widget gets populated options.
        self.fields["year"].widget.choices = year_choices
        self.fields["title"].required = False

        if not self.instance.pk:
            self.initial.setdefault("month", now.month)
            self.initial.setdefault("year", now.year)
            month_name = timezone.datetime(2000, int(self.initial["month"]), 1).strftime("%B")
            self.initial.setdefault("title", f"{month_name} {int(self.initial['year'])}")

    def clean(self):
        cleaned = super().clean()
        month = cleaned.get("month")
        year = cleaned.get("year")
        title = cleaned.get("title")
        if month and year:
            month_name = timezone.datetime(2000, int(month), 1).strftime("%B")
            # Only auto-generate if the user didn't provide a custom title.
            if not title or not str(title).strip():
                cleaned["title"] = f"{month_name} {int(year)}"
        return cleaned
