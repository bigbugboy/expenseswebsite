from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
import datetime
from collections import defaultdict


from .models import Category, Expense


@login_required(login_url='login')
def index(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', '').strip()
    if not search:
        expenses = Expense.objects.all()
    else:
        expenses = Expense.objects.filter(
            Q(owner=request.user),
            Q(amount__startswith=search)|
            Q(date__startswith=search)|
            Q(description__icontains=search)|
            Q(category__icontains=search)
        )

    paginator = Paginator(expenses, 3)
    context = {
        'page_obj': paginator.get_page(page),
        'search_text': search
    }
    
    return render(request, 'expenses/index.html', context)


@login_required(login_url='login')
def add_expense(request):
    context = {
        'categories': Category.objects.all(),
        'values': request.POST,
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)
    else:
        amount = request.POST['amount']
        category = request.POST['category']
        if not amount:
            messages.error(request, '数量不能为空')
            return render(request, 'expenses/add_expense.html', context)
        if not category:
            messages.error(request, '类型不能为空')
            return render(request, 'expenses/add_expense.html', context)
        
        expense = Expense(
            amount=amount,
            description=request.POST['description'],
            category=request.POST['category'],
            owner=request.user,
        )
        date = request.POST['date']
        if date:
            expense.date = date
        expense.save()
        messages.success(request, '添加成功')
        return redirect(to='expenses')



@login_required(login_url='login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        if not amount:
            messages.error(request, '数量不能为空')
            return render(request, 'expenses/edit_expense.html', context)
        if not category:
            messages.error(request, '类型不能为空')
            return render(request, 'expenses/edit_expense.html', context)
        
        expense.amount = amount
        expense.category = category
        expense.description = request.POST['description']
        date = request.POST['date']
        if date:
            expense.date = date
        expense.save()
        messages.success(request, '修改成功')
        return redirect(to='expenses')


@login_required(login_url='login')
def delete_expense(request, id):
    Expense.objects.filter(pk=id).delete()
    messages.success(request, '删除成功')
    return redirect(to='expenses')


@login_required(login_url='login')
def this_month_data_stats(request):
    start_date = datetime.date.today().replace(day=1)
    expenses = Expense.objects.filter(owner=request.user, date__gte=start_date).all()

    # amount per category
    # amount per day
    category_dict = defaultdict(int)
    day_dict = defaultdict(int)
    for item in expenses:
        category_dict[item.category] += item.amount
        day_dict[item.date] += item.amount
    category_stats = [{'name': k, 'value': v} for k, v in category_dict.items()]
    day_stats = [[str(k), v] for k, v in day_dict.items()]


    response_data = {
        'category_stats': category_stats,
        'day_stats': sorted(day_stats, key=lambda x: x[0]),
    }
    return JsonResponse(response_data)



def expense_summary_index(request):
    return render(request, 'expenses/summary_index.html')
