from django.db import models

class Task(models.Model):
    """
    任务模型：包含标题、描述、状态、优先级、截止日期和时间戳字段。
    status 用中文界面显示为 '未完成' / '已完成'，但存储为 'pending'/'done'。
    """
    STATUS_PENDING = "pending"
    STATUS_DONE = "done"
    STATUS_CHOICES = [
        (STATUS_PENDING, "未完成"),
        (STATUS_DONE, "已完成"),
    ]

    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "低"),
        (PRIORITY_MEDIUM, "中"),
        (PRIORITY_HIGH, "高"),
    ]

    title = models.CharField("标题", max_length=200)
    description = models.TextField("描述", blank=True)
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    priority = models.IntegerField("优先级", choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    due_date = models.DateField("截止日期", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "任务"
        verbose_name_plural = "任务列表"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
