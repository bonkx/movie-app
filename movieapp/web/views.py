from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from web.models import Movie

# Create your views here.


def index(request):
    return render(request, "web/home.html")


def movie_list(request):
    if request.method == 'GET':
        q = request.GET.get("q", "")

        queryset = Movie.objects.all()

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q)
            )

        data = queryset
        context = {
            'object_list': data,
        }

        return render(request, 'web/movie_list.html', context)
    return JsonResponse({'status': 'Invalid request'}, status=400)


def details(request, id):
    queryset = Movie.objects.filter(pk=id).first()

    context = {
        "row": queryset,
    }
    return render(request, "web/details.html", context)
