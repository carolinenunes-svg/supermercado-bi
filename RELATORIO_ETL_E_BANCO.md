# Relatório de Engenharia de Dados: ETL e Modelagem no SQLite
**Projeto:** Business Intelligence com Automações para Supermercados  
**Empresa de Referência:** Supermercado Alvorada Ltda.  
**Data da Execução:** 17/09/2026  
**Script de Pipeline:** `etl_pipeline.py`  
**Banco de Dados Analítico:** `data/supermercado.db` (SQLite)  
**Camada de Dados Tratados:** `data/processed/`

---

## 1. Fluxo dos Dados (Arquitetura de Dados)

O pipeline de dados foi projetado seguindo as melhores práticas de Engenharia de Dados, dividindo a arquitetura em camadas bem definidas e desacopladas:

```
[Camada Raw - Dados Brutos]
  data/raw/*.csv (7 fontes imutáveis)
         |
         v
[Camada de Processamento - ETL em Python/Pandas]
  etl_pipeline.py
  - Limpeza e Padronização (TRIM, Title Case, ISO Dates)
  - Deduplicação por Chaves Primárias
  - Isolamento de Chaves Órfãs e Inconsistências
         |
         +---------------------------------------+
         |                                       |
         v                                       v
[Camada Processed - CSVs Higienizados]  [Camada Analítica - SQLite]
  data/processed/*.csv                    data/supermercado.db
  + vendas_quarentena.csv                 - 7 tabelas dimensionais/fato
  + estoque_quarentena.csv                - 1 tabela de auditoria ETL
  + log_auditoria_etl.csv                 - 3 views analíticas para o BI
```

---

## 2. Tratamentos Realizados e Decisões de Engenharia

O processo de higienização tratou todos os desvios intencionais documentados na etapa anterior sem alterar ou excluir os arquivos originais em `data/raw/`:

| Tabela / Fonte | Problema Detectado | Tratamento Aplicado | Decisão Técnica |
| :--- | :--- | :--- | :--- |
| **`produtos.csv`** | Espaços extras no nome do produto 7 (`" Creme de Leite 200 g "`). | Aplicação de `str.strip()` em todas as colunas de texto (TRIM). | **Corrigido:** Texto padronizado para `"Creme de Leite 200 g"` garantindo integridade visual no dashboard. |
| **`fornecedores.csv`** | Campo opcional `contact_whatsapp` vazio/nulo no fornecedor `FOR-006` (*Distribuidora LimpaLar*). | Preenchimento com valor padrão `"Não informado"`. | **Tratado:** Permite geração de relatórios e cotações sem erros de execução por valores nulos. |
| **`compras.csv`** | 1 registro duplicado da nota de compra (`purchase_id = 511`). | Deduplicação baseada na chave composta (`purchase_id`, `product_id`, `purchase_date`). | **Descartado:** 1 duplicata removida; total ajustado de 215 para 214 registros válidos. |
| **`vendas.csv`** | 2 cupons de venda duplicados (linhas 201 e 802). | Deduplicação com `drop_duplicates(subset=['sale_id', 'product_id'])`. | **Descartado:** 2 duplicatas removidas, eliminando distorção artificial de faturamento. |
| **`vendas.csv`** | 1 transação com chave órfã (`product_id = 999`), inexistente no catálogo de produtos. | Filtro de integridade referencial com catálogo de produtos válidos. | **Isolado em Quarentena:** Registro salvo em `data/processed/vendas_quarentena.csv` e logado em `auditoria_etl`. |
| **`estoque.csv`** | Registro anômalo com saldo `-2.000` em `storage_location = 'Depósito'` para Alface Crespa (ID 21). | Filtro de saldos negativos (`current_quantity < 0`). | **Isolado em Quarentena:** Registro anômalo salvo em `data/processed/estoque_quarentena.csv`. A base ativa de estoque manteve apenas saldos físicos válidos. |
| **`validade.csv`** | Data de validade em padrão brasileiro (`15/08/2026`) no lote `LOT-MAN-20260608` (Manteiga). | *Parser* resiliente convertendo formato `DD/MM/YYYY` para formato ISO `YYYY-MM-DD`. | **Corrigido:** Data convertida com sucesso para `"2026-08-15"`, permitindo ordenação cronológica e cálculos de `julianday()` no SQLite. |
| **`perdas.csv`** | Motivo de perda digitado em minúsculas (`"avaria"`). | Padronização textual com `str.title()`. | **Corrigido:** Convertido para `"Avaria"`, padronizando agrupamentos e relatórios categóricos. |

---

## 3. Comparativo de Volumetria (Raw vs. Processed vs. SQLite)

| Fonte / Tabela | Registros Brutos (`data/raw/`) | Registros Tratados (`data/processed/`) | Registros no Banco SQLite | Observação de Ajuste |
| :--- | :---: | :---: | :---: | :--- |
| **`produtos`** | 40 | 40 | 40 | 100% íntegro (TRIM aplicado) |
| **`fornecedores`** | 8 | 8 | 8 | 100% íntegro (Nulo tratado) |
| **`compras`** | 215 | 214 | 214 | -1 duplicata descartada |
| **`vendas`** | 7.136 | 7.133 | 7.133 | -2 duplicatas descartadas, -1 órfã em quarentena |
| **`estoque`** | 41 | 40 | 40 | -1 posição negativa em quarentena |
| **`validade`** | 9 | 9 | 9 | 100% íntegro (Data padronizada) |
| **`perdas`** | 32 | 32 | 32 | 100% íntegro (Title Case aplicado) |
| **`auditoria_etl`** | — | 8 | 8 | Histórico formal das 8 ações de saneamento |

---

## 4. Modelagem e Estrutura do Banco de Dados SQLite

O banco foi implementado no arquivo físico `data/supermercado.db` com ativação de suporte a chaves estrangeiras (`PRAGMA foreign_keys = ON;`).

### 4.1. Esquema Físico das Tabelas (DDL)

```sql
-- Dimensão Produtos (Central)
CREATE TABLE produtos (
    product_id INTEGER PRIMARY KEY,
    barcode TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    unit_of_measure TEXT NOT NULL,
    min_stock REAL NOT NULL,
    ideal_stock REAL NOT NULL,
    sale_price REAL NOT NULL,
    active_flag TEXT NOT NULL
);

-- Dimensão Fornecedores
CREATE TABLE fornecedores (
    supplier_id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    trade_name TEXT NOT NULL,
    cnpj TEXT NOT NULL UNIQUE,
    contact_name TEXT NOT NULL,
    contact_whatsapp TEXT,
    lead_time_days INTEGER NOT NULL,
    city_state TEXT NOT NULL
);

-- Fato Compras (Entradas)
CREATE TABLE compras (
    purchase_id INTEGER NOT NULL,
    nfe_number TEXT NOT NULL,
    purchase_date TEXT NOT NULL,
    supplier_id TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    unit_cost REAL NOT NULL,
    total_cost REAL NOT NULL,
    cfop TEXT NOT NULL,
    icms_base REAL NOT NULL,
    icms_rate REAL NOT NULL,
    icms_amount REAL NOT NULL,
    PRIMARY KEY (purchase_id, product_id, purchase_date),
    FOREIGN KEY (supplier_id) REFERENCES fornecedores (supplier_id),
    FOREIGN KEY (product_id) REFERENCES produtos (product_id)
);

-- Fato Vendas (Saídas)
CREATE TABLE vendas (
    sale_id INTEGER NOT NULL,
    date_time TEXT NOT NULL,
    pos_id TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    unit_price REAL NOT NULL,
    total_amount REAL NOT NULL,
    payment_method TEXT NOT NULL,
    cfop TEXT NOT NULL,
    icms_rate REAL NOT NULL,
    icms_amount REAL NOT NULL,
    PRIMARY KEY (sale_id, product_id),
    FOREIGN KEY (product_id) REFERENCES produtos (product_id)
);

-- Estado do Estoque (Inventário)
CREATE TABLE estoque (
    product_id INTEGER NOT NULL,
    current_quantity REAL NOT NULL,
    reserved_quantity REAL NOT NULL,
    last_count_date TEXT NOT NULL,
    storage_location TEXT NOT NULL,
    PRIMARY KEY (product_id, storage_location),
    FOREIGN KEY (product_id) REFERENCES produtos (product_id)
);

-- Controle de Validade (Lotes Perecíveis)
CREATE TABLE validade (
    batch_id TEXT PRIMARY KEY,
    product_id INTEGER NOT NULL,
    expiration_date TEXT NOT NULL,
    batch_quantity REAL NOT NULL,
    entry_date TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES produtos (product_id)
);

-- Fato Perdas (Baixas Operacionais)
CREATE TABLE perdas (
    loss_id INTEGER PRIMARY KEY,
    loss_date TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    loss_reason TEXT NOT NULL,
    unit_cost_at_loss REAL NOT NULL,
    total_loss_value REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES produtos (product_id)
);

-- Tabela de Auditoria e Governança de Dados
CREATE TABLE auditoria_etl (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tabela TEXT NOT NULL,
    tipo_problema TEXT NOT NULL,
    detalhe TEXT NOT NULL,
    registros_afetados INTEGER NOT NULL,
    acao TEXT NOT NULL,
    data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 5. Views Analíticas Implementadas no SQLite

Para facilitar o consumo ágil pela futura camada de Dashboard, foram criadas 3 views gerenciais nativas:

1.  **`vw_alerta_reposicao`:** Compara saldo de `estoque` com `min_stock` e `ideal_stock` de `produtos`, classificando itens em `'CRITICO_RUPTURA'`, `'REPOSICAO_NECESSARIA'` ou `'ESTOQUE_ADEQUADO'`, calculando a quantidade sugerida de compra.
2.  **`vw_alerta_validade`:** Cruza datas de expiração dos lotes em relação à data de fechamento da simulação (`2026-06-29`), computando `dias_restantes` e emitindo classificação de criticidade (`'ALERTA_CRITICO'`, `'ATENCAO'`, `'REGULAR'`).
3.  **`vw_divergencia_inventario`:** Confronta o estoque físico registrado com a equação contábil de movimentações ($\text{Estoque Inicial} + \text{Compras} - \text{Vendas} - \text{Perdas}$), calculando a divergência percentual para aferição do parâmetro de 15%.

---

## 6. Validação dos 7 Cenários de Negócio no Banco de Dados

Consultas SQL diretas foram executadas para confirmar que os 7 cenários continuam 100% detectáveis e íntegros após o tratamento:

*   **Cenário 1 — Leite Integral 1 L (ID 1):**  
    *Consulta:* `SELECT * FROM vw_alerta_reposicao WHERE product_id = 1;`  
    *Resultado:* Estoque atual = **14,0 un**, Estoque Mínimo = **60,0 un**, Quantidade Sugerida = **166,0 un**, Status = `'CRITICO_RUPTURA'`.
*   **Cenário 2 — Café 500 g (ID 9):**  
    *Consulta:* `SELECT current_quantity FROM estoque WHERE product_id = 9;`  
    *Resultado:* Estoque atual = **118,0 un** (acima do ideal de 80,0 un), com apenas 1 venda registrada após 15/05. **Candidato a promoção confirmado.**
*   **Cenário 3 — Iogurte Natural 170 g (ID 2):**  
    *Consulta:* `SELECT * FROM vw_alerta_validade WHERE product_id = 2;`  
    *Resultado:* Lote `LOT-IOG-20260618` de 28 un, validade em `2026-07-03`, **4 dias restantes**, Status = `'ALERTA_CRITICO'`.
*   **Cenário 4 — Arroz 5 kg (ID 8):**  
    *Consulta:* `SELECT purchase_date, unit_cost FROM compras WHERE product_id = 8 ORDER BY purchase_date;`  
    *Resultado:* Histórico estável em R$ 18,30 e salto para **R$ 23,90** na compra de 26/06 (+30,6% pós-deduplicação).
*   **Cenário 5 — Banana Prata (ID 16):**  
    *Consulta:* `SELECT COUNT(*), SUM(quantity), SUM(total_loss_value) FROM perdas WHERE product_id = 16;`  
    *Resultado:* **15 registros**, **143,0 kg descartados**, prejuízo total de **R$ 514,80**.
*   **Cenário 6 — Lista de Cotação:**  
    *Consulta:* `SELECT product_id, product_name, quantidade_sugerida FROM vw_alerta_reposicao WHERE status_estoque = 'CRITICO_RUPTURA';`  
    *Resultado:* 4 produtos retornados: *Leite integral* (166 un), *Tomate* (51 kg), *Peito de Frango* (69 kg) e *Cerveja Pilsen* (178 un), mapeados para cotação.
*   **Cenário 7 — Óleo de Soja 900 ml (ID 10):**  
    *Consulta:* `SELECT estoque_registrado, estoque_calculado, divergencia_pct FROM vw_divergencia_inventario WHERE product_id = 10;`  
    *Resultado:* Registrado = **128,0 un**, Calculado = **160,0 un**, **Divergência = 20,00%** (superando o parâmetro de 15%).  
    *(Ressalva Formal: Parâmetro gerencial interno e configurável do projeto. Não representa uma regra tributária).*

---

## 7. Idempotência e Reprodutibilidade

O script `etl_pipeline.py` foi executado múltiplas vezes de forma sequencial.  
Graças ao uso de `DROP TABLE IF EXISTS` e recriação controlada das tabelas com inserção transacional atômica, **o processo é 100% idempotente**, mantendo exatamente a mesma contagem de linhas e integridade referencial a cada re-execução, sem gerar registros duplicados.
