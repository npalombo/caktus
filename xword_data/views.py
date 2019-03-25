import random

from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_http_methods

from .models import Clue, Entry


@require_http_methods(["GET", "POST"])
def drill(request):
    context = {}

    if request.method == 'GET':
        clue_count = Clue.objects.all().count()
        random_index = random.randint(0, clue_count-1)
        clue = Clue.objects.select_related('entry', 'puzzle').all()[random_index]
        context['clue'] = clue
    elif request.method == 'POST':
        clue_id = request.POST.get('clue_id')
        answer_text = request.POST.get('answer')

        clue = Clue.objects.select_related('entry').get(pk=clue_id)

        if answer_text.upper() == clue.entry.entry_text.upper():
            return redirect('xword-answer', clue.id)
        else:
            context['clue'] = clue
            context['wrong_answer'] = answer_text

    return render(
        request,
        'drill.html',
        context
    )


@require_GET
def answer(request, clue_id):
    try:
        clue = Clue.objects.select_related('entry').get(pk=clue_id)
    except Clue.DoesNotExist:
        raise Http404()
    else:
        matching_entries = Entry.objects.filter(clue__clue_text=clue.clue_text)
        matching_entry_count = matching_entries.count()
        matching_entries = matching_entries.annotate(count=Count('id')).values('count', 'entry_text')

        return render(
            request,
            'answer.html',
            {
                'clue': clue,
                'matching_entries': matching_entries,
                'matching_entry_count': matching_entry_count,
            }
        )

