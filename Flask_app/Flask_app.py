# on Flask_app.py
from flask import Flask, render_template
app = Flask(__name__) 

post1 = [
    {
        'author': 'Sooho Kim',
        'title': 'Post 1',
        'content': 'First post content',
        'date_posted': 'March 23, 2021'
    },
    {
        'author': 'Jane Doe',
        'title': 'Post 2',
        'content': 'Second post content',
        'date_posted': 'March 25, 2021'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=post1)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)