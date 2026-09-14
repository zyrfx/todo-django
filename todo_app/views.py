from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import HttpResponse
import openpyxl
from datetime import datetime
from django import forms
from django.db import models

def task_list(request):
    """
    列表视图：支持按状态、优先级、关键字筛选，并显示统计信息与分页。
    GET 参数：
     - status: pending / done / all
     - priority: 1/2/3 或不传
     - q: 关键词（在标题或描述中搜索）
     - page: 页码
    """
    qs = Task.objects.all()

    # 过滤
    status = request.GET.get("status", "all")
    if status in [Task.STATUS_PENDING, Task.STATUS_DONE]:
        qs = qs.filter(status=status)

    priority = request.GET.get("priority")
    if priority in ["1", "2", "3"]:
        qs = qs.filter(priority=int(priority))

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(models.Q(title__icontains=q) | models.Q(description__icontains=q))

    # 统计
    total_count = Task.objects.count()
    done_count = Task.objects.filter(status=Task.STATUS_DONE).count()
    pending_count = Task.objects.filter(status=Task.STATUS_PENDING).count()

    # 排序已在模型 meta 中处理
    # 分页
    page = request.GET.get("page", 1)
    paginator = Paginator(qs, 8)  # 每页 8 条
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "page_obj": page_obj,
        "total_count": total_count,
        "done_count": done_count,
        "pending_count": pending_count,
        "filter_status": status,
        "filter_priority": priority,
        "q": q,
    }
    return render(request, "todo_app/task_list.html", context)

def task_create(request):
    """创建任务"""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("todo_app:task_list"))
    else:
        form = TaskForm()
    return render(request, "todo_app/task_form.html", {"form": form, "action": "创建任务"})

def task_update(request, pk):
    """更新任务"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse("todo_app:task_list"))
    else:
        form = TaskForm(instance=task)
    return render(request, "todo_app/task_form.html", {"form": form, "action": "编辑任务"})

def task_detail(request, pk):
    """任务详情"""
    task = get_object_or_404(Task, pk=pk)
    return render(request, "todo_app/task_detail.html", {"task": task})

def task_delete(request, pk):
    """删除任务（带确认）"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect(reverse("todo_app:task_list"))
    return render(request, "todo_app/confirm_delete.html", {"task": task})

def task_toggle_status(request, pk):
    """切换任务完成/未完成状态"""
    task = get_object_or_404(Task, pk=pk)
    task.status = Task.STATUS_DONE if task.status == Task.STATUS_PENDING else Task.STATUS_PENDING
    task.save()
    return redirect(request.META.get("HTTP_REFERER", reverse("todo_app:task_list")))

def export_tasks_excel(request):
    """
    导出当前筛选结果为 Excel 文件（xlsx）。
    使用 openpyxl 创建工作簿，包含列：ID, 标题, 描述, 状态, 优先级, 截止日期, 创建时间。
    与 task_list 的筛选参数一致（status, priority, q）。
    """
    qs = Task.objects.all()

    status = request.GET.get("status", "all")
    if status in [Task.STATUS_PENDING, Task.STATUS_DONE]:
        qs = qs.filter(status=status)

    priority = request.GET.get("priority")
    if priority in ["1", "2", "3"]:
        qs = qs.filter(priority=int(priority))

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(models.Q(title__icontains=q) | models.Q(description__icontains=q))

    # 创建 Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tasks"

    headers = ["ID", "标题", "描述", "状态", "优先级", "截止日期", "创建时间"]
    ws.append(headers)

    for t in qs:
        ws.append([
            t.id,
            t.title,
            (t.description or ""),
            t.get_status_display(),
            dict(Task.PRIORITY_CHOICES).get(t.priority, ""),
            t.due_date.isoformat() if t.due_date else "",
            t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    # 生成 response
    filename = f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response
