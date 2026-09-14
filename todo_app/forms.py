from django import forms
from .models import Task
from django.utils import timezone

class TaskForm(forms.ModelForm):
    """
    任务表单，包含验证逻辑：
    - title 必填
    - due_date 若填写，不能早于今天（演示用）
    """
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "status"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("标题不能为空。")
        return title

    def clean_due_date(self):
        due = self.cleaned_data.get("due_date")
        if due and due < timezone.localdate():
            raise forms.ValidationError("截止日期不能早于今天。")
        return due
