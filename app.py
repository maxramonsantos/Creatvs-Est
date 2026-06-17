import os
import ssl
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Adaptação para pg8000 (único driver puro-Python que funciona no Nix/Replit)
# psycopg2-binary não funciona neste ambiente pois a extensão C não carrega.
_db_url = os.getenv("DATABASE_URL", "")
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+pg8000://", 1)
elif _db_url.startswith("postgresql://"):
    _db_url = _db_url.replace("postgresql://", "postgresql+pg8000://", 1)

# pg8000 não aceita sslmode nem channel_binding na query string — removemos
_parsed = urlparse(_db_url)
_qs = parse_qs(_parsed.query)
_qs.pop("sslmode", None)
_qs.pop("channel_binding", None)
_db_url = urlunparse(_parsed._replace(query=urlencode(_qs, doseq=True)))

_ssl_ctx = ssl.create_default_context()

app.config["SQLALCHEMY_DATABASE_URI"] = _db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"ssl_context": _ssl_ctx}}

db = SQLAlchemy(app)


# ==========================
# MODELS
# ==========================


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}


# ==========================
# DADOS INICIAIS
# ==========================

CATEGORIAS_INICIAIS = [
    {"id": 1, "nome": "Mercados"},
    {"id": 2, "nome": "Alimentação"},
    {"id": 3, "nome": "Saúde"},
    {"id": 4, "nome": "Beleza"},
    {"id": 5, "nome": "Automotivo"},
    {"id": 6, "nome": "Construção"},
    {"id": 7, "nome": "Agropecuária"},
    {"id": 8, "nome": "Educação"},
    {"id": 9, "nome": "Profissionais"},
]


def popular_banco():
    """Insere categorias apenas se a tabela estiver vazia"""

    if Categoria.query.count() == 0:
        categorias = [
            Categoria(id=item["id"], nome=item["nome"]) for item in CATEGORIAS_INICIAIS
        ]

        db.session.add_all(categorias)
        db.session.commit()

        print("✅ Categorias inseridas com sucesso!")
    else:
        print("ℹ️ Categorias já existem no banco.")


# ==========================
# ROTAS
# ==========================


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/loja-software")
def loja_de_software():
    return render_template("includes/page-loja-software.html")


@app.route("/catalogosd")
def catalogosd():
    categorias = Categoria.query.order_by(Categoria.nome).all()

    return render_template("includes/page-catalogosd.html", categorias=categorias)


@app.route("/catalogosd/catalogo")
def lista_catalogo():
    categorias = Categoria.query.order_by(Categoria.id).all()

    return jsonify([categoria.to_dict() for categoria in categorias])


@app.route("/ferramentas")
def ferramentas():
    return render_template("includes/page-ferramentas.html")


@app.route("/creatvs-joga")
def creatvs_joga():
    return render_template("includes/page-creatvs-joga.html")


@app.route("/aprenda")
def apenda():
    return render_template("includes/page-aprenda.html")


# ==========================
# INICIALIZAÇÃO
# ==========================

with app.app_context():
    db.create_all()
    popular_banco()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
