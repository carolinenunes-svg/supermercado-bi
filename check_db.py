import sqlite3

conn = sqlite3.connect('data/supermercado.db')
cur = conn.cursor()

# Check compras columns
cur.execute("PRAGMA table_info(compras)")
print("=== compras columns ===")
for c in cur.fetchall():
    print(c)

# Check views
print("\n=== vw_alerta_reposicao ===")
cur.execute("SELECT * FROM vw_alerta_reposicao LIMIT 3")
rows = cur.fetchall()
cur.execute("PRAGMA table_info(vw_alerta_reposicao)")  # won't work for views
# Get column names from description
cur.execute("SELECT * FROM vw_alerta_reposicao LIMIT 1")
print("columns:", [d[0] for d in cur.description])
print("sample:", rows[:2])

print("\n=== vw_alerta_validade ===")
cur.execute("SELECT * FROM vw_alerta_validade LIMIT 1")
print("columns:", [d[0] for d in cur.description])

print("\n=== vw_divergencia_inventario ===")
cur.execute("SELECT * FROM vw_divergencia_inventario LIMIT 1")
print("columns:", [d[0] for d in cur.description])

# Check compras for total_cost
cur.execute("SELECT * FROM compras LIMIT 1")
print("\n=== compras sample ===")
print("columns:", [d[0] for d in cur.description])

conn.close()
