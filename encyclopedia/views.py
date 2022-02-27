from django.shortcuts import render, HttpResponse, redirect
import markdown2
import random

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
            "entry":(f"ERROR: No entry called '{entry}' found.")
        })

def random_page(request):
    list_of_entries = util.list_entries()
    entry = random.choice(list_of_entries)
    entry_html = (markdown2.markdown(util.get_entry(entry)))
    return redirect(f"wiki/{entry}", {
        "title": entry,
        "entry":entry_html
    })
