from turtle import title
from django.shortcuts import render, HttpResponse, redirect
import markdown2
import random

from . import util

def index(request):
    """
    Renders the index page
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    """
    Renders the page of a particular entry, converting
    to HTML before publishing. If no entry by the name
    requested, returns an Error page.
    """
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
            "entry":(f"No page called '{entry}' found. Try searching using the bar on the left instead.")
        })

def random_page(request):
    """
    Grabs a random page from the list of entries and
    renders it.
    """
    list_of_entries = util.list_entries()
    entry = random.choice(list_of_entries)
    return redirect(f"wiki/{entry}")

def search(request):
    """
    Uses the search bar in the layout.html file to search for
    existing pages. If an exact match (case insensitively), 
    redirects to the matchin entry page.
    
    If a partial match, renders a list of all the entry pages
    with the partial match.
    """
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
    """
    Creates a new entry, with a separate title and body.
    Returns errors if either a title or a body is not entered.
    Returns an error if a page with that name already exists.
    """
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
    """
    Renders an edit page for the entry that was being viewed.
    """
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "body": util.get_entry(entry),
        "title": "",
        "Heading": (f"Edit page")
    })

def save(request, newEntry):
    """
    Saves the edits made to a page and overwrites the old file.
    """
    body = request.POST.get('editedBody')
    
    with open(f"entries/{newEntry}.md", "w") as f:
        f.write(body)
        return redirect(f'/wiki/{newEntry}')
