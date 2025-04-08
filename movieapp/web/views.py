from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from web.models import Movie

# Create your views here.


# class HomeView(TemplateView):
#     template_name = "web/home.html"


def index(request):
    return render(request, "web/home.html")


def movie_list(request):
    if request.method == 'GET':
        q = request.GET.get("q", "")
        per_page = request.GET.get("per_page", 10)
        page = request.GET.get("page", 1)

        queryset = Movie.objects.all()

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q)
            )

        paginator = Paginator(queryset, per_page)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        context = {
            'object_list': object_list,
        }

        return render(request, 'web/movie_list.html', context)
    return JsonResponse({'status': 'Invalid request'}, status=400)


def details(request, id):
    obj = get_object_or_404(Movie, pk=id)

    context = {
        "row": obj,
    }
    return render(request, "web/details.html", context)
