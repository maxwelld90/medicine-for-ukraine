from django.http import HttpResponseRedirect

def redirector(request):
    return HttpResponseRedirect('https://medicineforukraine.org')