from django.shortcuts import render

from .models import Course


# Create your views here.
def course_list(request):
    courses = Course.objects.all()
    return render(
        request,
        'courses/course_list.html',
        {'courses': courses},
    )


def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    return render(
        request,
        'courses/course_detail.html',
        {'course': course}
    )
