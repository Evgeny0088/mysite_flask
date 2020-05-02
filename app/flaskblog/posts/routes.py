from flask import request, render_template, url_for, abort, flash, redirect, Blueprint
from flask_login import login_required, current_user
from flaskblog.models import Post
from flaskblog.posts.forms import NewPostForm
from flaskblog import db

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():
	form = NewPostForm()
	if request.method =='POST':
		if form.validate_on_submit():
			post = Post(title = form.title.data, content = form.content.data, autor = current_user)
			db.session.add(post)
			db.session.commit()
			flash(f'New post has been created!', 'success')
			return redirect(url_for('main.index'))
	return render_template('new_post.html', title = 'New Post', form = form, legend = 'New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title = post.title, post = post)

@posts.route('/post/<int:post_id>/update', methods = ['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	form = NewPostForm()
	if post.autor!=current_user:
		abort(403)
	if request.method=='POST':
		if form.validate_on_submit():
			post.title = form.title.data
			post.content = form.content.data
			db.session.commit()
			flash(f'Your post has been updated!', 'success')
			return redirect(url_for('posts.post', post_id = post.id))
	elif request.method=='GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('update_post.html', title = post.title, form=form, legend = 'Update Post')

@posts.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	flash(f'Post has been deleted!', 'info')
	return redirect(url_for('main.index'))