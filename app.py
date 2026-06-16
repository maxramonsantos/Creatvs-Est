import os
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

# Adapta a URL para pg8000 (driver puro-Python) e remove sslmode da query string
_db_url = os.getenv("DATABASE_URL", "")
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+pg8000://", 1)
elif _db_url.startswith("postgresql://"):
    _db_url = _db_url.replace("postgresql://", "postgresql+pg8000://", 1)

# Remove ?sslmode=... da URL (pg8000 não aceita esse parâmetro na URL)
parsed = urlparse(_db_url)
qs = parse_qs(parsed.query)
qs.pop("sslmode", None)
_db_url = urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))

app.config["SQLALCHEMY_DATABASE_URI"] = _db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Categoria {self.nome}>"


with app.app_context():
    db.create_all()


@app.route("/popular")
def popular():
    categorias = [
        "Mercados",
        "Alimentação",
        "Saúde",
        "Beleza",
        "Automotivo",
        "Construção",
        "Agropecuária",
        "Educação",
        "Profissionais",
    ]

    for nome in categorias:
        db.session.add(Categoria(nome=nome))

    db.session.commit()

    return "Categorias cadastradas"


# CATEGORIAS = [
#     {"id": 1, "nome": "Mercados"},
#     {"id": 2, "nome": "Alimentação"},
#     {"id": 3, "nome": "Saúde"},
#     {"id": 4, "nome": "Beleza"},
#     {"id": 5, "nome": "Automotivo"},
#     {"id": 6, "nome": "Construção"},
#     {"id": 7, "nome": "Agropecuária"},
#     {"id": 8, "nome": "Educação"},
#     {"id": 9, "nome": "Profissionais"},
# ]


@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/loja-software")
def loja_de_software():
    return render_template("includes/page-loja-software.html")


@app.route("/catalogosd")
def catalogosd():
    categorias = Categoria.query.all()

    return render_template(
        "includes/page-catalogosd.html",
        categorias=categorias,
    )


@app.route("/catalogosd/catalogo")
def lista_catalogo():
    return jsonify(Categoria)


@app.route("/teste")
def teste():
    categorias = Categoria.query.all()

    return [{"id": c.id, "nome": c.nome} for c in categorias]


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
