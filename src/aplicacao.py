import json
import sqlite3
from flask import Flask
from flask import render_template
from flask import jsonify, redirect
from flask import request

app = Flask(__name__)

con = sqlite3.connect('agenda.db', check_same_thread=False)

from datetime import date

@app.route('/')
def index():
    return redirect('/agenda', code=302)


@app.route("/agenda-agrupada", methods=["GET"])
def listarContatosAgrupados():
    cursor = con.cursor()
    comando_sql = "SELECT EMPRESA , GROUP_CONCAT(NOME, ',') FROM contatos GROUP BY EMPRESA"
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    return jsonify(dados)

@app.route("/agenda", methods=["GET"])
def listarContatos():
    cursor = con.cursor()
    comando_sql = "SELECT * FROM contatos"
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    return jsonify(dados)


@app.route("/agenda/nome", methods=["GET"])
def listarContatos2():
    nome = request.args.get('nome', default='*', type=str)
    cursor = con.cursor()
    comando_sql = "SELECT * FROM contatos WHERE NOME = '"+ str(nome)+"'"
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    return jsonify(dados)

@app.route("/agenda/empresa", methods=["GET"])
def listarContatos3():
    empresa = request.args.get('empresa', default='*', type=str)
    cursor = con.cursor()
    comando_sql = "SELECT * FROM contatos WHERE EMPRESA = '"+ str(empresa)+"'"
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    return jsonify(dados)

@app.route("/agenda/email", methods=["GET"])
def listarContatos4():
    email = request.args.get('email', default='*', type=str)
    cursor = con.cursor()
    comando_sql = "SELECT * FROM contatos WHERE EMAIL = '"+ str(email)+"'"
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    return jsonify(dados)

@app.route("/agenda/id", methods=["GET"])
def listarContatos5():
    id = request.args.get('id', default='*', type=str)
    cursor = con.cursor()
    comando_sql = "SELECT * FROM contatos WHERE ID = "+ str(id)
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    return jsonify(dados)

@app.route("/agenda", methods=["POST"])
def inserirContatos():
    try:
        cursor = con.cursor()
        comando_sql = "INSERT INTO contatos (NOME, EMPRESA, TELEFONE, EMAIL) values ('"+request.get_json().get('NOME')+"', '"+request.get_json().get('EMPRESA')+"', '"+request.get_json().get('TELEFONE')+"', '"+ request.get_json().get('EMAIL')+"')"
        cursor.execute(comando_sql)
        con.commit()
        return jsonify("Sucesso!"), 200
    except sqlite3.OperationalError:
        return jsonify("Erro de execução de query!"), 404


@app.route("/agenda/<int:id>", methods=["PUT"])
def atualizarContatos(id):
    try:
        cursor = con.cursor()
        comando_sql = f"UPDATE contatos  SET NOME = '"+request.get_json().get('NOME')+"', EMPRESA = '"+request.get_json().get('EMPRESA')+"', TELEFONE = '"+request.get_json().get('TELEFONE')+"', EMAIL = '"+ request.get_json().get('EMAIL')+"' WHERE ID = "+ str(id) +""
        cursor.execute(comando_sql)
        con.commit()
        return jsonify("Sucesso!"), 200
    except sqlite3.OperationalError:
        return jsonify("Erro de execução de query!"), 404

@app.route("/agenda/<int:id>", methods=["DELETE"])
def deletarContatos(id):
    try:
        cursor = con.cursor()
        comando_sql = f"DELETE FROM contatos WHERE ID = " + str(id) + ""
        cursor.execute(comando_sql)
        con.commit()
        return jsonify("Sucesso!"), 200
    except sqlite3.OperationalError:
        return jsonify("Erro de execução de query!"), 404


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)