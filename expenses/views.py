from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Category, Expense


@login_required(login_url='login')
def index(request):
    page = request.GET.get('page', 1)
    expenses = Expense.objects.all()
    paginator = Paginator(expenses, 5)
    context = {
        'page_obj': paginator.get_page(page)
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