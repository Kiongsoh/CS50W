from markdown2 import Markdown
from django.shortcuts import render, redirect
from django.urls import reverse
from . import util
import random

# markdowner = Markdown()
# markdowner.convert("*boo!*")

# convert stored .md files in entries folder to html using markdown2 package
def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

# passing a variable entries as a dictionary to the home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# every time u are building a fn for a webpage
def entry(request, title):
    # check if the name is in our list of entries
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html",
            {"message": "page does not exist"})

    # if no display error page

    # if yes render entry page
    else:
        content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html",
            {"title": title, "content": content})

def search(request):
    if request.method=="POST":
        # exact matches
        # form input name defined in layout page
        query = request.POST['q']
        if util.get_entry(query) is not None:
            # content = convert_md_to_html(query)
            # return render(request, "encyclopedia/entry.html",
            #     {"content": content})
            url = reverse('entry', args=[query])
            return redirect(url)
    
        # partial matches
        else:
            search_result = []
            existing_entries  = util.list_entries()
            # save results to a list
            for entry in existing_entries:
                if query.lower() in entry.lower():
                    search_result.append(entry)
            
            # display on html
            return render(request, "encyclopedia/results.html",
                {"search_result": search_result})

def create_page(request):
    if request.method=="GET":
        return render(request, "encyclopedia/create_page.html")
    # if post:
    else:
        # get form input, save to variable
        title = request.POST['title']
        page_content = request.POST['page_content']

        # check if page exists
        if util.get_entry(title) is not None:
        # if yes go to error page
            return render(request, "encyclopedia/error.html",
                {"message": "page already exist"})

        # if no save to disk
        else:
            util.save_entry(title, page_content)
            # return entry page
            # Construct the URL with the title parameter
            url = reverse('entry', args=[title])
            return redirect(url)


def edit(request, title):
    content = util.get_entry(title)

    if request.method=="GET":
        return render(request, "encyclopedia/edit.html",
            {'title': title, 'content': content})

    else:
        # does not retreive title value, because title was not suppose to change
        new_content = request.POST['page_content']
        util.save_entry(title, new_content)
        # return entry page
        # Construct the URL with the title parameter
        url = reverse('entry', args=[title])
        return redirect(url)

def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    url = reverse('entry', args=[rand_entry])
    return redirect(url)
