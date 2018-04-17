from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

class NewEntry(items):
    # handles new-entry form submissions
    def render_entry_form(self, title="", entry="", error=""):
        self.render("new-entry.html", title=title, entry=entry, error=error)

    def get(self):
        self.render_entry_form()

    def post(self):
        title = self.request.get("title")
        entry = self.request.get("entry")

        if title and entry:
            e = Entry(title=title, entry=entry)
            e.put()

            self.redirect("/blog/"+ str(e.key().id()))
        else:
            error = "We need both a title and entry content!"
            self.render_entry_form(title, entry, error)
        
class Entry(db.Model):
    title = db.StringProperty(required = True)
    entry = db.TextProperty(required = True)
    
class MainPage(everything):
    # handles the '/' webpage
    def get(self):
        self.render("base.html")


class BlogEntries(add):
    #handles the '/blog' webpage
    def render_entries(self, title="", entry="", error=""):
        entries = db.GqlQuery("SELECT * FROM Entry ORDER BY created DESC LIMIT 5")
        self.render("front.html", title=title, entry=entry, error=error, entries=entries)
    def get(self):
        self.render_entries()

class ViewPostHandler(everything):
    #handle viewing single post by entity id
    def render_single_entry(self, id, title="", entry="", error=""):
        single_entry = Entry.get_by_id(int(id), parent=None)
        self.render("single-entry.html", title=title, entry=entry, error=error, single_entry=single_entry)
    def get(self, id):
        if id:
            self.render_single_entry(id)
        else:
            self.render_single_entry(id, title = "nothing here!",
                        post = "there is no post with id "+ str(id))


    

    