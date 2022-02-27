from django.shortcuts import render, HttpResponse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    list_of_entries = util.list_entries()
    if entry in list_of_entries:
        entry_html = (markdown2.markdown(util.get_entry(entry)))
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "entry":entry_html
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": "Error",
            "entry":(f"No entry called '{entry}' found.")
        })
