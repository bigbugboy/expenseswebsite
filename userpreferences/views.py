import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from .models import UserPreference


@login_required(login_url='login')
def index(request):

    currency_data = []
    filepath = settings.BASE_DIR / 'currencies.json'
    with open(filepath, 'r', encoding='utf8') as f:
        data = json.load(f)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})
    exists = UserPreference.objects.filter(user=request.user).exists()
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    else:
        user_preferences = UserPreference.objects.create(user=request.user)
    context = {
        'currencies': currency_data,
        'user_preferences': user_preferences
    }
    if request.method == 'POST':
        currency = request.POST['currency']
        if not currency:
            messages.error(request, '请选择货币')
            return render(request, 'userpreferences/index.html', context)
        user_preferences.currency = currency
        user_preferences.save()
        context[user_preferences] = user_preferences
        messages.success(request, '修改成功')
    
    return render(request, 'userpreferences/index.html', context)
