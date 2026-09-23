"""
gerar_dados.py
Script para geração determinística e reproduzível dos 7 arquivos CSV fictícios
para a camada de Business Intelligence do Supermercado Alvorada Ltda.
Período: 01/04/2026 a 29/06/2026 (90 dias)
"""

import os
import csv
import random
from datetime import date, datetime, timedelta

def main():
    # Fixar seed para total reprodutibilidade
    random.seed(42)

    output_dir = os.path.join(os.path.dirname(__file__), 'data', 'raw')
    os.makedirs(output_dir, exist_ok=True)

    start_date = date(2026, 4, 1)
    end_date = date(2026, 6, 29)
    days_count = (end_date - start_date).days + 1  # 90 dias

    print("Iniciando geração da massa de dados sintética...")

    # =========================================================================
    # 1. PRODUTOS (40 itens conforme CADASTRO_BASE.md)
    # =========================================================================
    produtos_base = [
        # Mercearia Seca (8)
        {"id": 8, "name": "Arroz 5 kg", "cat": "Mercearia Seca", "sub": "Grãos", "unit": "UN", "min": 40, "ideal": 120, "price": 26.90, "base_cost": 18.50},
        {"id": 9, "name": "Café 500 g", "cat": "Mercearia Seca", "sub": "Matinais", "unit": "UN", "min": 25, "ideal": 80, "price": 18.90, "base_cost": 13.00},
        {"id": 10, "name": "Óleo de soja 900 ml", "cat": "Mercearia Seca", "sub": "Óleos e Azeites", "unit": "UN", "min": 50, "ideal": 150, "price": 6.99, "base_cost": 4.80},
        {"id": 11, "name": "Feijão Preto 1 kg", "cat": "Mercearia Seca", "sub": "Grãos", "unit": "UN", "min": 35, "ideal": 100, "price": 7.99, "base_cost": 5.40},
        {"id": 12, "name": "Açúcar Refinado 1 kg", "cat": "Mercearia Seca", "sub": "Matinais", "unit": "UN", "min": 40, "ideal": 110, "price": 4.49, "base_cost": 3.10},
        {"id": 13, "name": "Macarrão Espaguete 500 g", "cat": "Mercearia Seca", "sub": "Massas", "unit": "UN", "min": 30, "ideal": 90, "price": 3.99, "base_cost": 2.70},
        {"id": 14, "name": "Farinha de Trigo 1 kg", "cat": "Mercearia Seca", "sub": "Farinhas", "unit": "UN", "min": 25, "ideal": 75, "price": 4.89, "base_cost": 3.30},
        {"id": 15, "name": "Sal Refinado 1 kg", "cat": "Mercearia Seca", "sub": "Condimentos", "unit": "UN", "min": 20, "ideal": 60, "price": 2.29, "base_cost": 1.40},

        # Laticínios e Frios (7)
        {"id": 1, "name": "Leite integral 1 L", "cat": "Laticínios e Frios", "sub": "Leites", "unit": "UN", "min": 60, "ideal": 180, "price": 5.49, "base_cost": 3.80},
        {"id": 2, "name": "Iogurte natural 170 g", "cat": "Laticínios e Frios", "sub": "Iogurtes", "unit": "UN", "min": 20, "ideal": 60, "price": 3.89, "base_cost": 2.50},
        {"id": 3, "name": "Queijo Mussarela Fatiado 200 g", "cat": "Laticínios e Frios", "sub": "Queijos", "unit": "UN", "min": 25, "ideal": 70, "price": 9.90, "base_cost": 6.80},
        {"id": 4, "name": "Requeijão Cremoso 200 g", "cat": "Laticínios e Frios", "sub": "Derivados", "unit": "UN", "min": 15, "ideal": 45, "price": 7.50, "base_cost": 5.10},
        {"id": 5, "name": "Manteiga com Sal 200 g", "cat": "Laticínios e Frios", "sub": "Derivados", "unit": "UN", "min": 15, "ideal": 40, "price": 10.90, "base_cost": 7.50},
        {"id": 6, "name": "Presunto Cozido Fatiado 200 g", "cat": "Laticínios e Frios", "sub": "Embutidos", "unit": "UN", "min": 20, "ideal": 50, "price": 6.80, "base_cost": 4.60},
        {"id": 7, "name": " Creme de Leite 200 g ", "cat": "Laticínios e Frios", "sub": "Derivados", "unit": "UN", "min": 30, "ideal": 90, "price": 3.49, "base_cost": 2.30}, # Desvio ETL: espaços

        # Hortifrúti (6)
        {"id": 16, "name": "Banana Prata", "cat": "Hortifrúti", "sub": "Frutas", "unit": "KG", "min": 30, "ideal": 90, "price": 5.99, "base_cost": 3.60},
        {"id": 17, "name": "Maçã Nacional", "cat": "Hortifrúti", "sub": "Frutas", "unit": "KG", "min": 20, "ideal": 60, "price": 8.99, "base_cost": 5.80},
        {"id": 18, "name": "Tomate Longa Vida", "cat": "Hortifrúti", "sub": "Legumes", "unit": "KG", "min": 25, "ideal": 70, "price": 7.49, "base_cost": 4.80},
        {"id": 19, "name": "Batata Inglesa", "cat": "Hortifrúti", "sub": "Legumes", "unit": "KG", "min": 40, "ideal": 120, "price": 5.49, "base_cost": 3.40},
        {"id": 20, "name": "Cebola Nacional", "cat": "Hortifrúti", "sub": "Legumes", "unit": "KG", "min": 25, "ideal": 75, "price": 4.99, "base_cost": 3.10},
        {"id": 21, "name": "Alface Crespa", "cat": "Hortifrúti", "sub": "Verduras", "unit": "UN", "min": 15, "ideal": 40, "price": 3.29, "base_cost": 1.80},

        # Açougue e Carnes (6)
        {"id": 22, "name": "Coxão Mole Bovino", "cat": "Açougue e Carnes", "sub": "Bovinos", "unit": "KG", "min": 20, "ideal": 60, "price": 38.90, "base_cost": 28.50},
        {"id": 23, "name": "Carne Moída Bovina (Acém)", "cat": "Açougue e Carnes", "sub": "Bovinos", "unit": "KG", "min": 25, "ideal": 75, "price": 28.90, "base_cost": 20.80},
        {"id": 24, "name": "Peito de Frango Resfriado", "cat": "Açougue e Carnes", "sub": "Aves", "unit": "KG", "min": 30, "ideal": 90, "price": 18.90, "base_cost": 13.20},
        {"id": 25, "name": "Coxa e Sobrecoxa de Frango", "cat": "Açougue e Carnes", "sub": "Aves", "unit": "KG", "min": 30, "ideal": 85, "price": 12.90, "base_cost": 8.90},
        {"id": 26, "name": "Bisteca Suína", "cat": "Açougue e Carnes", "sub": "Suínos", "unit": "KG", "min": 20, "ideal": 50, "price": 19.90, "base_cost": 14.10},
        {"id": 27, "name": "Linguiça Toscana", "cat": "Açougue e Carnes", "sub": "Embutidos Frescos", "unit": "KG", "min": 25, "ideal": 70, "price": 21.90, "base_cost": 15.30},

        # Bebidas (7)
        {"id": 28, "name": "Refrigerante Cola 2 L", "cat": "Bebidas", "sub": "Refrigerantes", "unit": "UN", "min": 40, "ideal": 120, "price": 9.49, "base_cost": 6.30},
        {"id": 29, "name": "Refrigerante Guaraná 2 L", "cat": "Bebidas", "sub": "Refrigerantes", "unit": "UN", "min": 35, "ideal": 100, "price": 7.99, "base_cost": 5.20},
        {"id": 30, "name": "Suco de Uva Integral 1 L", "cat": "Bebidas", "sub": "Sucos", "unit": "UN", "min": 15, "ideal": 45, "price": 12.90, "base_cost": 8.80},
        {"id": 31, "name": "Suco de Laranja 1 L", "cat": "Bebidas", "sub": "Sucos", "unit": "UN", "min": 15, "ideal": 45, "price": 8.90, "base_cost": 6.00},
        {"id": 32, "name": "Água Mineral sem Gás 500 ml", "cat": "Bebidas", "sub": "Águas", "unit": "UN", "min": 50, "ideal": 150, "price": 2.00, "base_cost": 0.90},
        {"id": 33, "name": "Cerveja Pilsen Lata 350 ml", "cat": "Bebidas", "sub": "Alcoólicos", "unit": "UN", "min": 80, "ideal": 240, "price": 3.69, "base_cost": 2.45},
        {"id": 34, "name": "Cerveja Puro Malte Lata 350 ml", "cat": "Bebidas", "sub": "Alcoólicos", "unit": "UN", "min": 60, "ideal": 180, "price": 4.49, "base_cost": 3.05},

        # Higiene e Limpeza (6)
        {"id": 35, "name": "Detergente Líquido 500 ml", "cat": "Higiene e Limpeza", "sub": "Limpeza de Louça", "unit": "UN", "min": 40, "ideal": 120, "price": 2.49, "base_cost": 1.50},
        {"id": 36, "name": "Sabão em Pó 1 kg", "cat": "Higiene e Limpeza", "sub": "Lavanderia", "unit": "UN", "min": 30, "ideal": 90, "price": 12.90, "base_cost": 8.70},
        {"id": 37, "name": "Amaciante de Roupas 2 L", "cat": "Higiene e Limpeza", "sub": "Lavanderia", "unit": "UN", "min": 20, "ideal": 60, "price": 11.50, "base_cost": 7.80},
        {"id": 38, "name": "Desinfetante Pinho 1 L", "cat": "Higiene e Limpeza", "sub": "Limpeza Geral", "unit": "UN", "min": 25, "ideal": 75, "price": 6.90, "base_cost": 4.50},
        {"id": 39, "name": "Sabonete em Barra 90 g", "cat": "Higiene e Limpeza", "sub": "Higiene Pessoal", "unit": "UN", "min": 40, "ideal": 120, "price": 2.79, "base_cost": 1.70},
        {"id": 40, "name": "Papel Higiênico Folha Dupla 4 un", "cat": "Higiene e Limpeza", "sub": "Higiene Pessoal", "unit": "UN", "min": 30, "ideal": 90, "price": 6.49, "base_cost": 4.20}
    ]

    produtos_rows = []
    for p in produtos_base:
        produtos_rows.append({
            "product_id": p["id"],
            "barcode": f"7891000{p['id']:06d}",
            "product_name": p["name"],
            "category": p["cat"],
            "subcategory": p["sub"],
            "unit_of_measure": p["unit"],
            "min_stock": p["min"],
            "ideal_stock": p["ideal"],
            "sale_price": f"{p['price']:.2f}",
            "active_flag": "S"
        })

    with open(os.path.join(output_dir, 'produtos.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "product_id", "barcode", "product_name", "category", "subcategory",
            "unit_of_measure", "min_stock", "ideal_stock", "sale_price", "active_flag"
        ])
        writer.writeheader()
        writer.writerows(produtos_rows)
    print(f"[OK] produtos.csv gerado com {len(produtos_rows)} produtos.")

    # =========================================================================
    # 2. FORNECEDORES (8 fornecedores conforme CADASTRO_BASE.md)
    # =========================================================================
    fornecedores_rows = [
        {"supplier_id": "FOR-001", "company_name": "Distribuidora Sul Brasil de Alimentos Ltda.", "trade_name": "Distribuidora Sul Brasil", "cnpj": "00.111.222/0001-33", "contact_name": "Marcos Oliveira", "contact_whatsapp": "(51) 98111-0101", "lead_time_days": 3, "city_state": "Porto Alegre / RS"},
        {"supplier_id": "FOR-002", "company_name": "Cooperativa Lácteos Vale Sul Ltda.", "trade_name": "Lácteos Vale Sul", "cnpj": "00.222.333/0001-44", "contact_name": "Juliana Becker", "contact_whatsapp": "(51) 98222-0202", "lead_time_days": 2, "city_state": "Lajeado / RS"},
        {"supplier_id": "FOR-003", "company_name": "Central de Abastecimento Hortifruti Ltda.", "trade_name": "Hortifruti Central", "cnpj": "00.333.444/0001-55", "contact_name": "Roberto Souza", "contact_whatsapp": "(51) 98333-0303", "lead_time_days": 1, "city_state": "Porto Alegre / RS"},
        {"supplier_id": "FOR-004", "company_name": "Frigorífico e Charqueada Pampa S.A.", "trade_name": "Frigorífico Pampa", "cnpj": "00.444.555/0001-66", "contact_name": "André Fagundes", "contact_whatsapp": "(55) 98444-0404", "lead_time_days": 2, "city_state": "Santa Maria / RS"},
        {"supplier_id": "FOR-005", "company_name": "Indústria de Bebidas Serra Gaúcha Ltda.", "trade_name": "Bebidas Serra Gaúcha", "cnpj": "00.555.666/0001-77", "contact_name": "Fernanda Rossi", "contact_whatsapp": "(54) 98555-0505", "lead_time_days": 3, "city_state": "Caxias do Sul / RS"},
        {"supplier_id": "FOR-006", "company_name": "Comercial e Distribuidora LimpaLar Ltda.", "trade_name": "Distribuidora LimpaLar", "cnpj": "00.666.777/0001-88", "contact_name": "Marcelo Santos", "contact_whatsapp": "", "lead_time_days": 4, "city_state": "Novo Hamburgo / RS"}, # Desvio ETL: WhatsApp nulo
        {"supplier_id": "FOR-007", "company_name": "Atacadão Regional de Secos e Molhados S.A.", "trade_name": "Atacadão Regional", "cnpj": "00.777.888/0001-99", "contact_name": "Patrícia Lima", "contact_whatsapp": "(51) 98777-0707", "lead_time_days": 2, "city_state": "Canoas / RS"},
        {"supplier_id": "FOR-008", "company_name": "Distribuidora e Logística MixSul Ltda.", "trade_name": "Distribuidora MixSul", "cnpj": "00.888.999/0001-11", "contact_name": "Thiago Werner", "contact_whatsapp": "(51) 98888-0808", "lead_time_days": 3, "city_state": "São Leopoldo / RS"},
    ]

    with open(os.path.join(output_dir, 'fornecedores.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "supplier_id", "company_name", "trade_name", "cnpj", "contact_name",
            "contact_whatsapp", "lead_time_days", "city_state"
        ])
        writer.writeheader()
        writer.writerows(fornecedores_rows)
    print(f"[OK] fornecedores.csv gerado com {len(fornecedores_rows)} fornecedores.")

    # Matriz Produto x Fornecedor (respeitando CADASTRO_BASE.md)
    matriz_fornecedores = {
        1: ["FOR-002", "FOR-008"],
        2: ["FOR-002"],
        3: ["FOR-002", "FOR-008"],
        4: ["FOR-002"],
        5: ["FOR-002", "FOR-008"],
        6: ["FOR-004", "FOR-002"],
        7: ["FOR-002", "FOR-007"],
        8: ["FOR-001", "FOR-007", "FOR-008"],
        9: ["FOR-001", "FOR-007", "FOR-008"],
        10: ["FOR-001", "FOR-007"],
        11: ["FOR-001", "FOR-007"],
        12: ["FOR-001", "FOR-007"],
        13: ["FOR-001", "FOR-008"],
        14: ["FOR-001", "FOR-007"],
        15: ["FOR-001", "FOR-007"],
        16: ["FOR-003"],
        17: ["FOR-003"],
        18: ["FOR-003"],
        19: ["FOR-003", "FOR-007"],
        20: ["FOR-003", "FOR-007"],
        21: ["FOR-003"],
        22: ["FOR-004"],
        23: ["FOR-004"],
        24: ["FOR-004"],
        25: ["FOR-004"],
        26: ["FOR-004"],
        27: ["FOR-004"],
        28: ["FOR-005", "FOR-007"],
        29: ["FOR-005", "FOR-007"],
        30: ["FOR-005"],
        31: ["FOR-005"],
        32: ["FOR-005", "FOR-007"],
        33: ["FOR-005", "FOR-007"],
        34: ["FOR-005", "FOR-007"],
        35: ["FOR-006", "FOR-007"],
        36: ["FOR-006", "FOR-007"],
        37: ["FOR-006", "FOR-008"],
        38: ["FOR-006", "FOR-007"],
        39: ["FOR-006", "FOR-007"],
        40: ["FOR-006", "FOR-008"]
    }

    prod_dict = {p["id"]: p for p in produtos_base}

    # =========================================================================
    # 3. ESTOQUE INICIAL EM 01/04/2026
    # =========================================================================
    initial_stock = {}
    for p in produtos_base:
        pid = p["id"]
        initial_stock[pid] = float(p["ideal"])

    initial_stock[1] = 120.0  # Leite: começa equilibrado
    initial_stock[9] = 60.0   # Café: estoque intermediário
    initial_stock[10] = 120.0 # Óleo: estoque inicial 120
    initial_stock[16] = 90.0  # Banana: estoque inicial 90 kg

    # =========================================================================
    # 4. COMPRAS (compras.csv)
    # =========================================================================
    compras_rows = []
    purchase_id_seq = 501
    nfe_seq = 12000
    total_purchased = {p["id"]: 0.0 for p in produtos_base}

    purchase_dates = [
        date(2026, 4, 3), date(2026, 4, 15), date(2026, 4, 28),
        date(2026, 5, 8), date(2026, 5, 20), date(2026, 5, 30),
        date(2026, 6, 8), date(2026, 6, 18), date(2026, 6, 26)
    ]

    for p_date in purchase_dates:
        nfe_seq += 1
        current_nfe = str(nfe_seq)

        for p in produtos_base:
            pid = p["id"]
            
            # Cenário 1: Leite Integral - compras regulares até 08/06, cessa depois
            if pid == 1:
                if p_date > date(2026, 6, 8):
                    continue
                qty = 150.0

            # Cenário 2: Café 500 g - compra extra em maio, cessa em junho
            elif pid == 9:
                if p_date == date(2026, 4, 15):
                    qty = 40.0
                elif p_date == date(2026, 5, 8):
                    qty = 130.0
                else:
                    continue

            # Cenário 4: Arroz 5 kg - compras periódicas de 100 un
            elif pid == 8:
                qty = 100.0

            # Cenário 7: Óleo de soja 900 ml - 4 compras de 100 un = 400 un
            elif pid == 10:
                if p_date in [date(2026, 4, 15), date(2026, 5, 8), date(2026, 5, 30), date(2026, 6, 18)]:
                    qty = 100.0
                else:
                    continue

            # Cenário 5: Banana Prata - compras regulares de 45 kg
            elif pid == 16:
                if p_date in purchase_dates[:8]: # 8 compras de 45 kg = 360 kg
                    qty = 45.0
                else:
                    continue

            # Produtos normais
            else:
                if random.random() < 0.60:
                    qty = round(p["ideal"] * random.uniform(0.6, 1.1), 0 if p["unit"] == "UN" else 1)
                else:
                    continue

            supp_id = random.choice(matriz_fornecedores[pid])
            unit_cost = p["base_cost"]
            cost_factor = random.uniform(0.98, 1.03)

            # Cenário 4: Arroz 5 kg com aumento de 29% na última compra (26/06)
            if pid == 8:
                if p_date == date(2026, 6, 26):
                    unit_cost = 23.90  # Aumento relevante de 29% frente aos R$ 18.50 habituais
                else:
                    unit_cost = 18.50 * cost_factor
            else:
                unit_cost = unit_cost * cost_factor

            unit_cost = round(unit_cost, 2)
            total_cost = round(qty * unit_cost, 2)

            icms_rate = 0.12 if p["cat"] in ["Mercearia Seca", "Hortifrúti", "Açougue e Carnes"] else 0.18
            icms_base = total_cost
            icms_amount = round(icms_base * icms_rate, 2)

            compras_rows.append({
                "purchase_id": purchase_id_seq,
                "nfe_number": current_nfe,
                "purchase_date": p_date.strftime("%Y-%m-%d"),
                "supplier_id": supp_id,
                "product_id": pid,
                "quantity": f"{qty:.3f}",
                "unit_cost": f"{unit_cost:.2f}",
                "total_cost": f"{total_cost:.2f}",
                "cfop": "1102",
                "icms_base": f"{icms_base:.2f}",
                "icms_rate": f"{icms_rate:.4f}",
                "icms_amount": f"{icms_amount:.2f}"
            })
            purchase_id_seq += 1
            total_purchased[pid] += qty

    # Desvio ETL intencional em compras.csv: 1 linha duplicada
    linha_dup_compras = compras_rows[10].copy()
    compras_rows.insert(11, linha_dup_compras)

    with open(os.path.join(output_dir, 'compras.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "purchase_id", "nfe_number", "purchase_date", "supplier_id", "product_id",
            "quantity", "unit_cost", "total_cost", "cfop", "icms_base", "icms_rate", "icms_amount"
        ])
        writer.writeheader()
        writer.writerows(compras_rows)
    print(f"[OK] compras.csv gerado com {len(compras_rows)} registros de entrada.")

    # =========================================================================
    # 5. PERDAS (perdas.csv)
    # =========================================================================
    perdas_rows = []
    loss_id_seq = 701
    total_lost = {p["id"]: 0.0 for p in produtos_base}

    # Cenário 5: Banana Prata (ID 16) - perdas sistemáticas
    banana_loss_dates = [
        date(2026, 4, 5), date(2026, 4, 12), date(2026, 4, 19), date(2026, 4, 26),
        date(2026, 5, 3), date(2026, 5, 10), date(2026, 5, 17), date(2026, 5, 24), date(2026, 5, 31),
        date(2026, 6, 5), date(2026, 6, 11), date(2026, 6, 16), date(2026, 6, 21), date(2026, 6, 25), date(2026, 6, 28)
    ]
    for b_date in banana_loss_dates:
        qty = round(random.uniform(7.0, 11.0), 1)
        reason = random.choice(["Deterioração", "Avaria", "Quebra Física"])
        cost = prod_dict[16]["base_cost"]
        total_val = round(qty * cost, 2)
        perdas_rows.append({
            "loss_id": loss_id_seq,
            "loss_date": b_date.strftime("%Y-%m-%d"),
            "product_id": 16,
            "quantity": f"{qty:.3f}",
            "loss_reason": reason,
            "unit_cost_at_loss": f"{cost:.2f}",
            "total_loss_value": f"{total_val:.2f}"
        })
        loss_id_seq += 1
        total_lost[16] += qty

    # Perdas pontuais para outros perecíveis (Tomate, Queijo, Frango, Maçã, Alface)
    outros_pereciveis = [3, 17, 18, 21, 24]
    for pid in outros_pereciveis:
        for _ in range(random.randint(2, 4)):
            rand_day = random.randint(0, days_count - 1)
            l_date = start_date + timedelta(days=rand_day)
            qty = round(random.uniform(1.0, 3.0), 1 if prod_dict[pid]["unit"] == "KG" else 0)
            cost = prod_dict[pid]["base_cost"]
            total_val = round(qty * cost, 2)
            perdas_rows.append({
                "loss_id": loss_id_seq,
                "loss_date": l_date.strftime("%Y-%m-%d"),
                "product_id": pid,
                "quantity": f"{qty:.3f}",
                "loss_reason": random.choice(["Avaria", "Vencimento", "Deterioração"]),
                "unit_cost_at_loss": f"{cost:.2f}",
                "total_loss_value": f"{total_val:.2f}"
            })
            loss_id_seq += 1
            total_lost[pid] += qty

    # Desvio ETL intencional em perdas.csv: 1 registro com texto em minúsculas
    perdas_rows.append({
        "loss_id": loss_id_seq,
        "loss_date": "2026-06-20",
        "product_id": 18,
        "quantity": "2.000",
        "loss_reason": "avaria", # Desvio ETL: minúsculo
        "unit_cost_at_loss": "4.80",
        "total_loss_value": "9.60"
    })
    total_lost[18] += 2.0
    loss_id_seq += 1

    with open(os.path.join(output_dir, 'perdas.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "loss_id", "loss_date", "product_id", "quantity", "loss_reason",
            "unit_cost_at_loss", "total_loss_value"
        ])
        writer.writeheader()
        writer.writerows(perdas_rows)
    print(f"[OK] perdas.csv gerado com {len(perdas_rows)} apontamentos de perda.")

    # =========================================================================
    # 6. DEFINIÇÃO EXATA DE ESTOQUE FINAL ALVO E TOTAL DE VENDAS
    # =========================================================================
    target_final_stock = {}
    for p in produtos_base:
        pid = p["id"]
        # Normal baseline: saldo final entre 75% e 95% do ideal
        target_final_stock[pid] = round(p["ideal"] * random.uniform(0.75, 0.95), 0 if p["unit"] == "UN" else 1)

    # Cenários Específicos:
    target_final_stock[1] = 14.0   # Cenário 1: Leite Integral -> Estoque Crítico (14 < min 60)
    target_final_stock[9] = 118.0  # Cenário 2: Café 500 g -> Estoque Alto / Parado (118 > ideal 80)
    target_final_stock[10] = 160.0 # Cenário 7: Óleo de soja -> calculado 160 (gravado será 128 = 20% divergência)
    target_final_stock[16] = 80.0  # Cenário 5: Banana -> estoque final saudável pós-perdas

    # Cenário 6: Itens com necessidade de cotação por estarem abaixo do min_stock
    target_final_stock[18] = 19.0  # Tomate: min 25 -> faltam 6 para min, 51 para ideal 70 (FOR-003)
    target_final_stock[24] = 21.0  # Peito de frango: min 30 -> faltam 9 para min, 69 para ideal 90 (FOR-004)
    target_final_stock[33] = 62.0  # Cerveja Pilsen: min 80 -> faltam 18 para min, 178 para ideal 240 (FOR-005)

    # Total exato de vendas exigido pela equação:
    # Estoque Inicial + Compras - Vendas - Perdas = Estoque Final
    # => Vendas = Estoque Inicial + Compras - Perdas - Estoque Final
    target_total_sales = {}
    for p in produtos_base:
        pid = p["id"]
        needed = initial_stock[pid] + total_purchased[pid] - total_lost[pid] - target_final_stock[pid]
        target_total_sales[pid] = round(needed, 0 if p["unit"] == "UN" else 1)

    # =========================================================================
    # 7. VENDAS DIÁRIAS NORMALIZADAS (vendas.csv)
    # =========================================================================
    vendas_rows = []
    sale_id_seq = 10001
    total_sold = {p["id"]: 0.0 for p in produtos_base}

    payment_methods = ["Cartão Débito", "Cartão Crédito", "PIX", "Dinheiro"]
    payment_weights = [0.40, 0.35, 0.15, 0.10]

    # Para cada produto, calculamos pesos diários normalizados
    for p in produtos_base:
        pid = p["id"]
        needed_qty = target_total_sales[pid]

        raw_weights = []
        for d in range(days_count):
            curr_date = start_date + timedelta(days=d)
            weekday = curr_date.weekday()
            
            # Fator dia da semana
            w = 1.45 if weekday in [4, 5] else (1.15 if weekday in [3, 6] else 0.85)
            # Fator início de mês
            if curr_date.day <= 10:
                w *= 1.25

            # Cenário 2: Café 500 g desacelera drasticamente após 15/05
            if pid == 9:
                if curr_date >= date(2026, 5, 15):
                    w *= 0.08 # Redução drástica de vendas
                else:
                    w *= 1.60

            # Ruído aleatório
            w *= random.uniform(0.85, 1.15)
            raw_weights.append(w)

        sum_w = sum(raw_weights)
        norm_weights = [w / sum_w for w in raw_weights]

        # Distribuir vendas por dia
        daily_allocations = []
        accum = 0.0
        for d in range(days_count):
            if d == days_count - 1:
                # Último dia recebe o resíduo para fechar exato
                day_qty = needed_qty - accum
            else:
                raw_day_qty = needed_qty * norm_weights[d]
                day_qty = round(raw_day_qty, 0 if p["unit"] == "UN" else 1)
                accum += day_qty
            daily_allocations.append(day_qty)

        # Gerar cupons ao longo do dia para o produto
        for d in range(days_count):
            curr_date = start_date + timedelta(days=d)
            day_qty = daily_allocations[d]
            if day_qty <= 0:
                continue

            num_tx = 1 if day_qty <= 2 else random.randint(1, min(4, int(day_qty)))
            rem_tx_qty = day_qty

            for tx_i in range(num_tx):
                if tx_i == num_tx - 1:
                    tx_qty = rem_tx_qty
                else:
                    tx_qty = round(rem_tx_qty / (num_tx - tx_i), 0 if p["unit"] == "UN" else 1)
                    if tx_qty <= 0:
                        tx_qty = 1.0 if p["unit"] == "UN" else 0.5
                    rem_tx_qty -= tx_qty

                if tx_qty <= 0:
                    continue

                hour = random.choice([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                dt_str = f"{curr_date.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}:{second:02d}"

                pos_id = f"PDV 0{random.randint(1, 6)}"
                pay_method = random.choices(payment_methods, weights=payment_weights)[0]

                u_price = p["price"]
                tot_amount = round(tx_qty * u_price, 2)
                cfop = "5102"
                icms_rate = 0.18
                icms_amount = round(tot_amount * icms_rate, 2)

                vendas_rows.append({
                    "sale_id": sale_id_seq,
                    "date_time": dt_str,
                    "pos_id": pos_id,
                    "product_id": pid,
                    "quantity": f"{tx_qty:.3f}",
                    "unit_price": f"{u_price:.2f}",
                    "total_amount": f"{tot_amount:.2f}",
                    "payment_method": pay_method,
                    "cfop": cfop,
                    "icms_rate": f"{icms_rate:.4f}",
                    "icms_amount": f"{icms_amount:.2f}"
                })
                sale_id_seq += 1
                total_sold[pid] += tx_qty

    # Desvios ETL intencionais em vendas.csv:
    # 1) Duas linhas duplicadas
    vendas_rows.insert(200, vendas_rows[200].copy())
    vendas_rows.insert(800, vendas_rows[800].copy())

    # 2) Uma chave órfã (product_id = 999)
    vendas_rows.append({
        "sale_id": 99999,
        "date_time": "2026-06-15 11:20:00",
        "pos_id": "PDV 02",
        "product_id": 999, # Desvio ETL: Chave inexistente
        "quantity": "1.000",
        "unit_price": "10.00",
        "total_amount": "10.00",
        "payment_method": "Dinheiro",
        "cfop": "5102",
        "icms_rate": "0.1800",
        "icms_amount": "1.80"
    })

    with open(os.path.join(output_dir, 'vendas.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "sale_id", "date_time", "pos_id", "product_id", "quantity", "unit_price",
            "total_amount", "payment_method", "cfop", "icms_rate", "icms_amount"
        ])
        writer.writeheader()
        writer.writerows(vendas_rows)
    print(f"[OK] vendas.csv gerado com {len(vendas_rows)} transações de caixa.")

    # =========================================================================
    # 8. ESTOQUE FINAL (estoque.csv - Foto em 29/06/2026)
    # =========================================================================
    estoque_rows = []
    
    for p in produtos_base:
        pid = p["id"]
        # Equação fundamental:
        calc_stock = initial_stock[pid] + total_purchased[pid] - total_sold[pid] - total_lost[pid]
        calc_stock = round(calc_stock, 3)

        # Cenário 7: Óleo de soja 900 ml (ID 10)
        # Divergência intencional: calculado é 160.0, gravado é 128.0 (divergência de 20.0% > 15%)
        # Parâmetro gerencial interno e configurável do projeto. Não representa uma regra tributária.
        if pid == 10:
            final_qty = 128.000
        else:
            final_qty = calc_stock

        estoque_rows.append({
            "product_id": pid,
            "current_quantity": f"{final_qty:.3f}",
            "reserved_quantity": "0.000",
            "last_count_date": "2026-06-29",
            "storage_location": "Loja"
        })

    # Desvio ETL intencional em estoque.csv: 1 registro com saldo negativo em depósito
    estoque_rows.append({
        "product_id": 21, # Alface Crespa
        "current_quantity": "-2.000", # Desvio ETL: Saldo negativo em depósito
        "reserved_quantity": "0.000",
        "last_count_date": "2026-06-29",
        "storage_location": "Depósito"
    })

    with open(os.path.join(output_dir, 'estoque.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "product_id", "current_quantity", "reserved_quantity", "last_count_date", "storage_location"
        ])
        writer.writeheader()
        writer.writerows(estoque_rows)
    print(f"[OK] estoque.csv gerado com {len(estoque_rows)} posições de inventário.")

    # =========================================================================
    # 9. VALIDADE DE LOTES (validade.csv)
    # =========================================================================
    validade_rows = []

    # Cenário 3: Iogurte natural 170 g (ID 2)
    # Lote de 28 un que vence em 03/07/2026 (faltam 4 dias em relação a 29/06).
    # Vendas diárias são ~2 a 3 un/dia. Em 4 dias vende ~10 un, restando 18 un que vencerão!
    validade_rows.append({
        "batch_id": "LOT-IOG-20260618",
        "product_id": 2,
        "expiration_date": "2026-07-03",
        "batch_quantity": "28.000",
        "entry_date": "2026-06-18"
    })

    # Lotes para outros itens perecíveis
    lotes_pereciveis = [
        {"batch_id": "LOT-LEI-20260608", "pid": 1, "exp": "2026-07-20", "qty": 14.0, "entry": "2026-06-08"},
        {"batch_id": "LOT-QUE-20260618", "pid": 3, "exp": "2026-08-15", "qty": 55.0, "entry": "2026-06-18"},
        {"batch_id": "LOT-REQ-20260608", "pid": 4, "exp": "2026-09-10", "qty": 35.0, "entry": "2026-06-08"},
        {"batch_id": "LOT-PRE-20260626", "pid": 6, "exp": "2026-07-28", "qty": 40.0, "entry": "2026-06-26"},
        {"batch_id": "LOT-BOV-20260626", "pid": 22, "exp": "2026-07-06", "qty": 45.0, "entry": "2026-06-26"},
        {"batch_id": "LOT-FRA-20260626", "pid": 24, "exp": "2026-07-05", "qty": 21.0, "entry": "2026-06-26"},
        {"batch_id": "LOT-SUI-20260626", "pid": 26, "exp": "2026-07-08", "qty": 38.0, "entry": "2026-06-26"},
    ]

    for l in lotes_pereciveis:
        validade_rows.append({
            "batch_id": l["batch_id"],
            "product_id": l["pid"],
            "expiration_date": l["exp"],
            "batch_quantity": f"{l['qty']:.3f}",
            "entry_date": l["entry"]
        })

    # Desvio ETL intencional em validade.csv: 1 registro com formato de data brasileiro (DD/MM/YYYY)
    validade_rows.append({
        "batch_id": "LOT-MAN-20260608",
        "product_id": 5, # Manteiga
        "expiration_date": "15/08/2026", # Desvio ETL: data DD/MM/YYYY em vez de YYYY-MM-DD
        "batch_quantity": "22.000",
        "entry_date": "2026-06-08"
    })

    with open(os.path.join(output_dir, 'validade.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "batch_id", "product_id", "expiration_date", "batch_quantity", "entry_date"
        ])
        writer.writeheader()
        writer.writerows(validade_rows)
    print(f"[OK] validade.csv gerado com {len(validade_rows)} lotes de perecíveis.")

    print("\n--- GERAÇÃO CONCLUÍDA COM SUCESSO! ---")

if __name__ == '__main__':
    main()
