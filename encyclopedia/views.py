from turtle import title
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
    if util.search_entries(entry, list_of_entries):
        entry_html = (markdown2.markdown(util.get_entry(entry)))
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "entry":entry_html
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": "Error",
            "entry":(f"No entry called '{entry}' found. Try searching using the bar on the left instead n.")
        })

def random_page(request):
    list_of_entries = util.list_entries()
    entry = random.choice(list_of_entries)
    return redirect(f"wiki/{entry}")

def search(request):
    search = request.GET.get('q')
    list_of_entries = util.list_entries()
    if util.search_entries(search, list_of_entries):
        return redirect((f"wiki/{search}"))
    else:
        results_list = [i for i in list_of_entries if search.casefold() in i.casefold()]
        return render(request, "encyclopedia/searchResults.html", {
            "title": "Search results",
            "Heading": "Search results",
            "Results": results_list
        })

def create(request):
    if request.method == "POST":
        title = (request.POST.get('newTitle')).capitalize()
        body = request.POST.get('newBody')
        if title and body:
            if util.search_entries(title, util.list_entries()):
                return render(request, "encyclopedia/error.html", {
                "title": "Error",
                "entry": ("A page with that title already exists. Please edit that page, or try a different title.")
                })
            else:
                with open(f"entries/{title}.md", "w") as file:
                    file.write(f"# {title} \n \n" + body)
                    return redirect(f"wiki/{title}")

        elif title and not body:
            return render(request, "encyclopedia/error.html", {
            "title": "Error",
            "entry": (f"No body entered. Please try again.")
        })

        else:
            return render(request, "encyclopedia/error.html", {
            "title": "Error",
            "entry": (f"No title entered. Please try again.")
        })
    else: 
        return render(request, "encyclopedia/create.html", {
        "title": "Create page",
        "Heading": "Create page"
    })

def edit(request, entry):
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "body": util.get_entry(entry),
        "title": "Edit page",
        "Heading": (f"Edit page")
    })

def save(request, entry):
    body = request.POST.get('editedBody')
    with open(f"entries/{entry}.md", "r+") as f:
        f.truncate(2)
        f.write(body)
        return redirect(f"wiki/{entry}")
