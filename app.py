import os

from flask import Flask, abort, redirect, render_template_string, request, url_for

from estacionamento import Estacionamento

app = Flask(__name__)
estacionamento = Estacionamento(storage_type=os.getenv("ESTACIONAMENTO_STORAGE_TYPE", "json"))
estacionamento.carregar()
estacionamento.definir_tarifa("carro", 15.0)
estacionamento.definir_tarifa("moto", 8.0)

HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Estacionamento</title>
    <style>
      body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #0f172a, #1e293b); color: #f8fafc; }
      .container { max-width: 1000px; margin: 40px auto; padding: 24px; background: rgba(17,24,39,0.95); border-radius: 20px; box-shadow: 0 12px 35px rgba(0,0,0,0.35); }
      h1 { margin-top: 0; }
      .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 20px; }
      .card { background: #1f2937; border-radius: 14px; padding: 16px; }
      form { display: grid; gap: 10px; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); margin-bottom: 20px; }
      input, button { padding: 10px 12px; border-radius: 10px; border: 1px solid #334155; }
      button { background: #2563eb; color: white; cursor: pointer; }
      ul { padding-left: 18px; }
      .muted { color: #94a3b8; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Estacionamento Premium</h1>
      <p class="muted">Gestão moderna, rápida e elegante para seu estacionamento.</p>
      <div class="cards">
        <div class="card"><strong>Ocupadas:</strong> {{ painel.ocupadas }}</div>
        <div class="card"><strong>Livres:</strong> {{ painel.livres }}</div>
        <div class="card"><strong>Ocupação:</strong> {{ painel.percentual }}%</div>
      </div>
      <div class="card"><strong>Tarifas:</strong> carro R$15, moto R$8</div>
      <h2>Cadastro</h2>
      <form method="post" action="/cadastrar">
        <input name="tipo" placeholder="tipo" required>
        <input name="nome" placeholder="nome" required>
        <input name="placa" placeholder="placa" required>
        <input name="telefone" placeholder="telefone" required>
        <input name="valor_mensal" placeholder="valor mensal">
        <input name="codigo_acesso" placeholder="codigo acesso">
        <button type="submit">Salvar</button>
      </form>
      <h2>Clientes</h2>
      <ul>
        {% for cliente in clientes %}
          <li>{{ cliente.tipo }} - {{ cliente.nome }} - {{ cliente.placa }}</li>
        {% endfor %}
      </ul>
      <h2>Movimentações ativas</h2>
      <ul>
        {% for movimento in movimentacoes %}
          <li>{{ movimento.placa }} - entrada {{ movimento.entrada }}</li>
        {% endfor %}
      </ul>
    </div>
  </body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        HTML,
        clientes=estacionamento.listar_clientes(),
        movimentacoes=estacionamento.listar_movimentacoes_ativas(),
        painel=estacionamento.obter_painel_ocupacao(),
    )


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    tipo = request.form.get("tipo", "avulso")
    nome = request.form.get("nome", "")
    placa = request.form.get("placa", "")
    telefone = request.form.get("telefone", "")
    valor_mensal = request.form.get("valor_mensal")
    codigo_acesso = request.form.get("codigo_acesso")

    try:
      estacionamento.cadastrar_cliente(
        tipo=tipo,
        nome=nome,
        placa=placa,
        telefone=telefone,
        valor_mensal=float(valor_mensal) if valor_mensal else None,
        codigo_acesso=codigo_acesso,
      )
    except (TypeError, ValueError) as err:
      abort(400, description=str(err))
    estacionamento.salvar()
    return redirect(url_for("index"))


if __name__ == "__main__":
  debug = os.getenv("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
  app.run(debug=debug)
