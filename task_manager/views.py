from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext


class IndexView(View):
    def get(self, request, *args, **kwargs):
        hello_from_hexlet = gettext("Hello from Hexlet!")
        coding_courses = gettext('Practical programming courses')
        read_more = gettext("Read more")
        exit = gettext("Exit")
        return render(request, 'index.html',
                    context={'hello_from_hexlet': hello_from_hexlet,
                            'coding_courses': coding_courses,
                            'read_more': read_more,
                            'exit': exit,
                            })
