from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Pokemon


def index(request):
    latest_pokemon_list = Pokemon.objects.order_by("national_number")
    template = loader.get_template("national_dex/index.html")
    context = {
        "query_results": latest_pokemon_list,
    }
    return HttpResponse(template.render(context, request))


def pokemon_detail(request, pokemon_name):
    pokemon = get_object_or_404(Pokemon, name=pokemon_name)
    return render(request, "national_dex/detail.html", {"pokemon": pokemon})
