from django.shortcuts import render, redirect

from . import util
import markdown, random

md= markdown.Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    if request.method == 'POST':
        entry = [request.POST['q']]
        entry[0] = entry[0].lower()
        error = ["Not Found"]
        entries = util.list_entries()
        list_entry = []
        for en in entries:
            temp = [en]
            en = en.lower()
            if(entry[0] in en):
                if(entry[0] == en):
                    response = redirect("/wiki/"+temp[0])
                    return response
                list_entry.append(temp[0])
           
        if(len(list_entry)>0):
            return render (request, "encyclopedia/search.html", {
                "entries": list_entry
            })
        else:
            return render (request, "encyclopedia/search.html", {
                "entries": error
            })
        


def entry(request, entry_name):
    entry = util.get_entry(entry_name)
    name_split = entry_name.split("/")
    name = name_split[len(name_split)-1]
    if entry != None:
        return render(request, "encyclopedia/entry.html",{
            "entry": md.convert(entry), "title":name
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "entry": "Entry Not Found", "title":name, "hide":'hide'
        })

def edit(request, entry_name):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        response = redirect("/wiki/"+title)
        return response
    entry = util.get_entry(entry_name)
    name_split = entry_name.split("/")
    name = name_split[len(name_split)-1]
    return render(request, "encyclopedia/edit.html",{
        "title":name, "content":entry
    })

def new(request):
    if request.method == 'POST':
        title = request.POST['title']
        match_title = title.lower()
        content = request.POST['content']
        entries = util.list_entries()
        for en in entries:
            en = en.lower()
            if(match_title == en):
                return render(request, "encyclopedia/new.html",{
                    "title":title, "content":content, "alert":"An entry with the same name already exist. Please try a different title."
                })
        util.save_entry(title,content)
        response = redirect("/wiki/"+title)
        return response
    return render(request, "encyclopedia/new.html",{

    })

def random_view(request):
    entries = util.list_entries()
    length = len(entries)-1
    n = random.randint(0,length)
    title = entries[n]
    response = redirect("/wiki/"+title)
    return response