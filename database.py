from sqlalchemy import create_engine, text

engine = 
create_engine("postgresql+psycopg2://postgres:q&T3Fr,Pka3zRhm@db.nvjjamhigviwfboskamm.supabase.co:5432/postgres?sslmode=require)")

with engine.connect() as conn:
    resultado = conn.execute(text("SELECT * from categoria"))
    print(resultado.all())

21# If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
22# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
23# engine = create_engine(DATABASE_URL, poolclass=NullPool)


# user=postgres
# password=[YOUR-PASSWORD]
# host=db.nvjjamhigviwfboskamm.supabase.co
# port=5432
# dbname=postgres