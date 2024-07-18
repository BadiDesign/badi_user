from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.views import View


class BadiSelect2(View):
    model = None
    qs = None
    id = 'id'
    text = 'title'
    per_page = 20
    string = False

    def get_model(self):
        return self.model.objects.all() if self.qs is None else self.qs

    def get(self, request):
        page = request.GET.get('page', 1)
        search = request.GET.get('search')

        thing = self.get_model()

        if search is not None and len(search.strip()) > 0:
            thing = thing.filter(**{self.text + '__contains': search})
        if self.string:
            thing = thing.values('title')
        else:
            if self.id != 'id':
                thing = thing.annotate(id=F(self.id), text=self.get_text())
            else:
                thing = thing.annotate(text=self.get_text())
            thing = thing.values('id', 'text')

        paginator = Paginator(thing, self.per_page)
        results = paginator.page(int(page)).object_list
        results_bitten = list(results)
        if self.string:
            results_bitten = list(map(lambda x: {'id': x['title'], 'text': x['title']}, results_bitten))
        return JsonResponse({
            'results': results_bitten,
            "pagination": {
                "more": paginator.page(page).has_next()
            }
        }, safe=False)

    def get_text(self):
        return F(self.text)
