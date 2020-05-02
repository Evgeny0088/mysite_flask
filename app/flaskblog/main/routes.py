from flask import request, render_template, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route("/")
def index():
	page = request.args.get('page', default = 1, type = int)
	posts = Post.query.order_by(Post.created.desc())\
								.paginate(per_page = 2, page = page)
	return render_template('home.html', title = 'Home page', posts = posts)

@main.route("/about")
def about():
	return render_template('about.html', title = 'About')