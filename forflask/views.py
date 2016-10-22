from flask import render_template, request, url_for, redirect
from forflask import app
from os import listdir, remove
from datetime import datetime
from forms import CreateForm, EditForm
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER

def get_accounts():
	f=open("forflask/static/database/names")
	accounts=[]
	for line in f:
		account=[]
		while ";" in line:
			account+=[line[:line.index(";")]]
			line=line[line.index(";")+1:]
		account+=[line]
		accounts+=[account]
	f.close()
	return accounts
	
def get_list():
	accs=get_accounts()
	acc_list=[len(accs)]
	for element in accs:
		if element[1]:
			acc_list+=[element[1]]
	return acc_list

def get_num():
	nums=[]
	accs=get_accounts()[1:]
	for acc in accs:
		nums+=[int(acc[0])]
	'''if acc[0]!="num":'''
	nums.sort()
	num=1
	for i in nums:
		if i==num:
			num+=1
		else:
			break
	return num

def delete_account(num):
	lines=open("forflask/static/database/names").readlines()
	i=0
	for line in lines:
		if num==line[:line.index(';')]:
			break
		i+=1
	lines.pop(i)
	f=open("forflask/static/database/names","w")
	f.writelines(lines)
	f.close()

def delete_image(num):
	i=False
	for file_name in listdir("forflask/static/database/"):
		if num in file_name:
			i=True
			break
	if i:
		remove("forflask/static/database/"+file_name)	
	
def num_from_post(post_id):
	lines=open("forflask/static/database/names").readlines()
	num=lines[post_id][:lines[post_id].index(';')]
	return num

def get_posts(post_id):
	accs=get_accounts()
	posts=[]
	for i in range(len(accs[0])):
		post=[accs[0][i]]
		post+=[accs[post_id][i]]
		posts+=[post]
	return posts

@app.route('/')	
@app.route('/index')
def index():
    return render_template('start.html',
    acc_list=get_list())

@app.route('/post/<int:post_id>',methods= ['GET','POST'])
def show_account(post_id):
	posts=get_posts(post_id)
	
	if request.method == 'POST':
		if request.form['submit'] == 'delete' or 1:
			delete_account(posts[0][1])
			delete_image(posts[0][1])
			return redirect(url_for("index"))
	i=True
	
	num = num_from_post(post_id)
	for file_name in listdir("forflask/static/database/"):
		if num in file_name:
			i=False
			break
	if i:
		file_name=''
			
	return render_template("account.html",
		filename=url_for('static',filename=("database/"+file_name)),
		posts=posts,
		acc_list=get_list(),
		post_id=post_id,
		editing=True)
		
@app.route('/create',methods= ['GET','POST'])
def make_create():
	form=CreateForm()
	num=get_num()
	if form.image.data:
		image_name=secure_filename(form.image.data.filename)
		form.image.data.save(UPLOAD_FOLDER+str(num)+image_name[image_name.index('.'):])
	if form.is_submitted():
		'''Data Saving'''
		name = str(form.name)
		info = str(form.info)
		name=name[name.index('value="')+7:name.index('">')].replace(";",",")
		info=info[info.index('>')+1:info.index('</')].replace(";",",").replace('\n',' ')
		
		f=open("forflask/static/database/names","a")
		f.write(str(num)+";"+name+";"+str(datetime.now())[:-7].replace('-','.')+";"+info+'\n')
		f.close()
		
		return redirect("/post/"+str(get_list()[0]-1))
	return render_template('create.html',
		title='Create your character?',
		form=form,
		acc_list=get_list())
	
@app.route('/edit/<int:post_id>',methods= ['GET','POST'])
def edit(post_id):
	form=EditForm()	
	post=get_posts(post_id)
	num = num_from_post(post_id)
	defaults = [post[1][1],post[3][1]]
	if form.image.data:
		delete_image(num_from_post(post_id))
		image_name=secure_filename(form.image.data.filename)
		form.image.data.save(UPLOAD_FOLDER+str(num)+image_name[image_name.index('.'):])
	if form.is_submitted():
		'''Data Saving'''
		name = str(form.name)
		info = str(form.info)
		name=name[name.index('value="')+7:name.index('">')]
		info=info[info.index('>')+1:info.index('</')]
		 
		if not post[1][1]==name or not post[3][1]==info:
			delete_account(num)
			f=open("forflask/static/database/names","a")
			f.write(str(num)+";"+name+";"+post[2][1]+";"+info+'\n')
			f.close()
		'''return redirect('/accont/'+num)'''
		return redirect('post/'+str(post_id))
	return render_template('create.html',
		title='Edit your hero!',
		form=form,
		defaults=defaults,
		acc_list=get_list())



