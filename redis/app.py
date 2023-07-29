from flask import Flask, render_template, redirect, url_for
import redis
import datetime
import threading

app = Flask(__name__)
r = redis.Redis()

def limpar_banco():
    # Função para limpar o banco de dados
    r.flushall()

@app.route('/')
def index():
    # Recupere os pontos dos usuários do Redis
    usuario1_pontos = int(r.get('usuario1_pontos') or 0)
    usuario2_pontos = int(r.get('usuario2_pontos') or 0)

    # Verifique quem está em primeiro lugar no ranking
    if usuario1_pontos > usuario2_pontos:
        primeiro_lugar = "Usuário 1"
    elif usuario2_pontos > usuario1_pontos:
        primeiro_lugar = "Usuário 2"
    else:
        primeiro_lugar = "Empate"

    # Recupere o último momento em que um usuário subiu no ranking
    ultimo_momento = r.get('ultimo_momento')

    return render_template('index.html', usuario1_pontos=usuario1_pontos, usuario2_pontos=usuario2_pontos, primeiro_lugar=primeiro_lugar, ultimo_momento=ultimo_momento)

@app.route('/usuario1')
def aumentar_pontos_usuario1():
    # Incremente os pontos do usuário 1 no Redis
    r.incr('usuario1_pontos')

    # Registre o momento atual como o último momento em que um usuário subiu no ranking
    r.set('ultimo_momento', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return redirect(url_for('index'))

@app.route('/usuario2')
def aumentar_pontos_usuario2():
    # Incremente os pontos do usuário 2 no Redis
    r.incr('usuario2_pontos')

    # Registre o momento atual como o último momento em que um usuário subiu no ranking
    r.set('ultimo_momento', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Iniciar a contagem regressiva para limpar o banco após 1 minuto
    t = threading.Timer(5, limpar_banco)
    t.start()

    # Executar o servidor Flask
    app.run(debug=True)
