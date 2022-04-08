import sys
import json
from django.http import HttpResponse, HttpResponseRedirect


def handler404(request, exception):
    """
    A simple 404 handler to redirect the user to the main homepage.
    """
    return HttpResponseRedirect('https://medicineforukraine.org')

def handler500(request):
    """
    A simple 500 handler to tell the user something went wrong.
    """
    type_, value, traceback = sys.exc_info()

    return HttpResponse(json.dumps({
                            "message": "An exception occurred.",
                            "exception": str(value),
                            "contact": "webmaster@medicineforukraine.org",
                        }),
                        content_type='application/json')