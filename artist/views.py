import json
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.core import serializers
from django.db.models import Q
from django import http
from .models import Artist

# Create your views here.


class HomePage(View):
    template_name = 'artist/list.html'
    def get(self, request):
        return render(request, self.template_name)


class ArtistList(View):
    relations_to_serialize = {}
    extras = {}

    def get(self, request):
        search_kwargs = request.GET.dict()
        objects = self.prepare_search(Artist.objects.all(), **search_kwargs)
        page_no = search_kwargs.get('page_no', 0)
        per_page = search_kwargs.get('per_page', 10)
        show_all = search_kwargs.get('show_all', 0)
        prev_page_no = 0
        next_page_no = 0
        current_page_number = 0
        num_of_pages = objects.count()
        if not int(show_all):
            paginator = Paginator(objects, per_page)
            try:
                objects = paginator.page(page_no)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                objects = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                objects = paginator.page(paginator.num_pages)

            try:
                prev_page_no = objects.previous_page_number()
            except InvalidPage as e:
                prev_page_no = page_no
            try:
                next_page_no = objects.next_page_number()
            except InvalidPage as e:
                next_page_no = page_no
            current_page_number = objects.number
            num_of_pages = objects.paginator.num_pages
        serialized_objects = json.loads(serializers.serialize(
            'json',
            objects,
            relations=self.relations_to_serialize,
            extras=self.extras
        ))
        response_values = {
            'objects': serialized_objects,
            'previous_page_number': prev_page_no,
            'next_page_number': next_page_no,
            'current_page_number': current_page_number,
            'num_of_pages': num_of_pages,
            'per_page': per_page
        }
        response = http.HttpResponse()
        response.status_code = 200
        response.write(json.dumps(response_values))
        response['Content-Type'] = 'application/json'
        return response

    def prepare_search(self, objects, **search_kwargs):
        if search_kwargs.get('search_text'):
            objects = objects.filter(
                Q(name__icontains=search_kwargs.get('search_text'))
            )
        return objects