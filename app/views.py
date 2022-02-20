from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter(original=0, test=0)
counter_click = Counter(original=0, test=0)


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    if request.GET.get('from-landing') == 'original':
        counter_click['original'] += 1
    elif request.GET.get('from-landing') == 'test':
        counter_click['test'] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    page_param = request.GET.get('ab-test-arg')
    if page_param == 'original':
        view_template = 'landing.html'
        counter_show['original'] += 1
    elif page_param == 'test':
        view_template = 'landing_alternate.html'
        counter_show['test'] += 1
    return render(request, view_template)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    try:
        test_conversion = counter_click['test'] / counter_show['test']
    except ArithmeticError:
        test_conversion = 0
    try:
        original_conversion = counter_click['original'] / counter_show['original']
    except ArithmeticError:
        original_conversion = 0
    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
