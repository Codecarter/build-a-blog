from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog@localhost8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column (db.Integer,primary_key= True)
    title = db.Column (db.String (180))
    body = db.Column (db.String (1000))
    created = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.created = datetime.utcnow()

    def is_valid(self):
        if self.title and self.body and self.created:
            return True
        else:
            return False
@app.route("/")
def index():
    return redirect("/blog") 

@app.route("/blog") 
def display_blog_entries():

    entry_id = request.args.get('id') 
    if (entry_id):
        entry = Entry.query.get(entry_id) 
        return render_template ('single_entry.html', title= "Blog Entry", entry=entry)
        sort = request.args.get('sort')
    if (sort == "newest"): 
        all_entries= Entry.query.order_by(Entry.created.desc()).all()
    else:
        all_entries= Entry.query.all()
    return render_template('all_entries.html', title= 'All Entries', all_entries= all_entries)

@app.route('/new_entry', methods=['GET','POST'])
def new_entry():
    if request.method == 'POST':
        new_entry_title = request.form['title']
        new_entry_body = request.form['body']
        new_entry= Entry(new_entry_title, new_entry_body)
        if new_entry_title == "" or new_entry_body == "":
            flash("Please check your entry for errors. Both a title and body are required")
            return render_template('new_entry_form.html',title= 'Create new blog entry', new_entry_title= new_entry_title, new_entry_body=new_entry_body)
        else:
            db.session.add(new_entry) 
            db.session.commit()

            url="/blog?=" + str(new_entry.id)
            return redirect(url) 
    return render_template('new_entry_form.html', title= "Create new blog entry")  

if __name__ == '__main__':
    app.run()   
        