from flask import Flask, render_template, request, session, redirect, url_for
import dataset


app = Flask("project")

app.secret_key = 'Pomp22'

@app.route("/")

def page_init():
	return render_template("index.html")




@app.route("/tipoget")

def ir_get():
	return render_template("get.html")


@app.route("/tipopost")

def ir_post():
	return render_template("post.html")





@app.route("/receber/", methods=['GET','POST'])

def receber():
	if request.method == 'GET' :
		return u"tipo GET <br>Nome: {} <br> idade: {}".format(request.args.get("nome"),request.args.get("idade")) 

	elif request.method == 'POST' :
		return u"tipo POST <br>Nome: {} <br> idade: {}".format(request.form["nome"],request.form["idade"])





@app.route("/inform")
def info() :
	return "informacoes"


@app.route("/sessao")
def acesso_sessao() :
	return u'''
	<h1>inicio da sessao</h1>
	<form action="{}" method="post">
		usuario: <input type="text" name="usuario"/>
		<br/>
		<input type="submit" value="Acesso restrito"/>
	</form>
	'''.format(url_for('validacao_sessao'))

@app.route("/validacao/", methods=['POST'])

def validacao_sessao() :
	if request.method == "POST" :
		session['usuario'] = request.form["usuario"]
		return redirect(url_for('acesso_restrito'))

	return redirect(url_for('acesso_sessao'))

@app.route("/restrito")

def acesso_restrito() :
	if ( session ) :
		return u"area restrita. <br/>usuario {}".format(session['usuario'])

	return redirect(url_for('acesso_sessao'))

@app.route("/log_off")

def out() :
	session.pop('usuario', None)
	return redirect(url_for('acesso_sessao'))

@app.route("/operacao")
def operacao_banco() :
	with dataset.connect("sqlite:///python.db") as db:
		db['aulas'].insert(dict(nome=u"aula 1", tipo=u"Python"))
		db['aulas'].insert(dict(nome=u"aula 2", tipo=u"Banco de dados"))
		db['aulas'].insert(dict(nome=u"aula 3", tipo=u"html_"))
		db['aulas'].insert(dict(nome=u"aula 4", tipo=u"js"))

	return u"Crud"

@app.route("/banco")

def listar_banco() :
	with dataset.connect("sqlite:///python.db") as db:
		lista = db['aulas'].all()

	html = "<ul>"

	for item in lista:
		html += "<li>{id} - {nome} - {tipo}</li>".format(id=item['id'],nome=item['nome'],tipo=item['tipo'])
	html += "</ul>"

	return u"banco <Br>Lista: <br>{}".format(html)




@app.route("/teste")

def teste():
	return "ok"



app.run(use_reloader=True)
