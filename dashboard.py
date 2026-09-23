"""
================================================================================
  SUPERMERCADO BI — SISTEMA DE BUSINESS INTELLIGENCE E AUTOMAÇÃO GERENCIAL
  Empresa de Referência: Supermercado Alvorada Ltda.
  Slogan: "Dados organizados. Decisões inteligentes."
  Tecnologias: Streamlit | Plotly | SQLite | Pandas
================================================================================
"""

import os
import sqlite3
from datetime import date, datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# 0. FUNÇÕES AUXILIARES DE FORMATAÇÃO NUMÉRICA E MONETÁRIA
# ─────────────────────────────────────────────────────────────────────────────
def fmt_brl(val):
    if pd.isna(val) or val is None:
        return "R$ 0,00"
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_int(val):
    if pd.isna(val) or val is None:
        return "0"
    return f"{int(val):,}".replace(",", ".")

def fmt_qtd(val, dec=1):
    if pd.isna(val) or val is None:
        return "0"
    if dec == 0:
        return f"{val:,.0f}".replace(",", ".")
    return f"{val:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIGURAÇÃO GLOBAL DA PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SUPERMERCADO BI — Supermercado Alvorada",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. DESIGN SYSTEM & ESTILOS CSS PERSONALIZADOS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Fundo da Aplicação */
    [data-testid="stAppViewContainer"] {
        background-color: #0b1120;
        color: #f1f5f9;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Sidebar personalizada */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090e1a 0%, #111a2e 100%);
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #94a3b8 !important;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Brand Header Sidebar */
    .brand-container {
        padding: 16px 8px 20px 8px;
        text-align: center;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 20px;
    }
    .brand-title {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        color: #10b981 !important;
        margin-top: 6px;
        line-height: 1.2;
    }
    .brand-subtitle {
        font-size: 0.85rem;
        font-weight: 600;
        color: #f8fafc !important;
        margin-top: 4px;
    }
    .brand-slogan {
        font-size: 0.72rem;
        font-style: italic;
        color: #94a3b8 !important;
        margin-top: 6px;
    }

    /* Header Principal */
    .main-header {
        background: linear-gradient(135deg, #131d31 0%, #0f172a 100%);
        border: 1px solid #24334a;
        border-radius: 16px;
        padding: 22px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .main-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #f8fafc;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-title-badge {
        background: #065f46;
        color: #34d399;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 1px solid #059669;
    }
    .main-subtitle {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .context-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 14px;
    }
    .chip {
        background: #1e293b;
        color: #cbd5e1;
        font-size: 0.75rem;
        padding: 4px 12px;
        border-radius: 8px;
        border: 1px solid #334155;
    }
    .chip-accent {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border-color: rgba(16, 185, 129, 0.3);
    }

    /* Cards de KPI Modernos */
    .kpi-card {
        background: linear-gradient(145deg, #152033 0%, #0f1829 100%);
        border: 1px solid #24334a;
        border-radius: 14px;
        padding: 18px 20px;
        text-align: left;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
        margin-bottom: 12px;
        height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px -6px rgba(0, 0, 0, 0.45);
        border-color: #38bdf8;
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.1;
    }
    .kpi-value.green  { color: #34d399; }
    .kpi-value.blue   { color: #60a5fa; }
    .kpi-value.yellow { color: #fbbf24; }
    .kpi-value.red    { color: #f87171; }
    .kpi-subtext {
        font-size: 0.72rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Boxes de Alerta */
    .alert-box {
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        font-size: 0.86rem;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        line-height: 1.45;
    }
    .alert-red {
        background: rgba(239, 68, 68, 0.12);
        border-left: 4px solid #ef4444;
        color: #fca5a5;
        border-top: 1px solid rgba(239, 68, 68, 0.2);
        border-right: 1px solid rgba(239, 68, 68, 0.2);
        border-bottom: 1px solid rgba(239, 68, 68, 0.2);
    }
    .alert-yellow {
        background: rgba(245, 158, 11, 0.12);
        border-left: 4px solid #f59e0b;
        color: #fde047;
        border-top: 1px solid rgba(245, 158, 11, 0.2);
        border-right: 1px solid rgba(245, 158, 11, 0.2);
        border-bottom: 1px solid rgba(245, 158, 11, 0.2);
    }
    .alert-blue {
        background: rgba(59, 130, 246, 0.12);
        border-left: 4px solid #3b82f6;
        color: #93c5fd;
        border-top: 1px solid rgba(59, 130, 246, 0.2);
        border-right: 1px solid rgba(59, 130, 246, 0.2);
        border-bottom: 1px solid rgba(59, 130, 246, 0.2);
    }
    .alert-green {
        background: rgba(16, 185, 129, 0.12);
        border-left: 4px solid #10b981;
        color: #86efac;
        border-top: 1px solid rgba(16, 185, 129, 0.2);
        border-right: 1px solid rgba(16, 185, 129, 0.2);
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
    }

    /* Aviso Gerencial / Disclaimer Fiscal */
    .disclaimer-card {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 16px 0 24px 0;
        font-size: 0.82rem;
        color: #cbd5e1;
        line-height: 1.55;
    }
    .disclaimer-card b {
        color: #fbbf24;
    }

    /* Títulos de Seção */
    .section-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 24px 0 14px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #1e293b;
    }

    /* Mini Card de Cenário de Negócio */
    .scenario-card {
        background: #131d2e;
        border: 1px solid #24334a;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }
    .scenario-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .scenario-name {
        font-size: 0.85rem;
        font-weight: 700;
        color: #f1f5f9;
    }
    .scenario-badge {
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        text-transform: uppercase;
    }
    .badge-critico { background: #7f1d1d; color: #fca5a5; }
    .badge-atencao { background: #78350f; color: #fde047; }
    .badge-ok      { background: #064e3b; color: #86efac; }
    .badge-info    { background: #1e3a8a; color: #93c5fd; }
    .scenario-desc {
        font-size: 0.77rem;
        color: #94a3b8;
        line-height: 1.4;
    }

    /* WhatsApp button card */
    .whatsapp-box {
        background: #0f241d;
        border: 1px solid #059669;
        border-radius: 12px;
        padding: 16px;
        margin-top: 14px;
    }

    /* Estilização das Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #111a2d;
        border-radius: 12px;
        padding: 6px;
        gap: 6px;
        border: 1px solid #1e293b;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 0.84rem;
        padding: 8px 16px;
        transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #1e293b;
        color: #f8fafc !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #10b981 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
    }

    /* Tabelas e Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid #24334a;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Botões personalizados */
    div.stButton > button {
        background: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background: #10b981;
        border-color: #10b981;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. CAMADA DE DADOS: CONEXÃO E CARREGAMENTO DO BANCO SQLITE
# ─────────────────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "supermercado.db")

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_connection()

@st.cache_data(ttl=300)
def load_vendas():
    df = pd.read_sql("SELECT * FROM vendas", conn)
    df["date_time"] = pd.to_datetime(df["date_time"])
    df["date"] = df["date_time"].dt.date
    return df

@st.cache_data(ttl=300)
def load_compras():
    df = pd.read_sql("SELECT * FROM compras", conn)
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    df["date"] = df["purchase_date"].dt.date
    if "total_cost" not in df.columns:
        df["total_cost"] = df["unit_cost"] * df["quantity"]
    return df

@st.cache_data(ttl=300)
def load_produtos():
    return pd.read_sql("SELECT * FROM produtos", conn)

@st.cache_data(ttl=300)
def load_fornecedores():
    return pd.read_sql("SELECT * FROM fornecedores", conn)

@st.cache_data(ttl=300)
def load_estoque():
    return pd.read_sql("SELECT * FROM estoque", conn)

@st.cache_data(ttl=300)
def load_perdas():
    df = pd.read_sql("SELECT * FROM perdas", conn)
    df["loss_date"] = pd.to_datetime(df["loss_date"])
    df["date"] = df["loss_date"].dt.date
    return df

@st.cache_data(ttl=300)
def load_validade():
    df = pd.read_sql("SELECT * FROM validade", conn)
    if "expiration_date" in df.columns:
        df["expiration_date"] = pd.to_datetime(df["expiration_date"]).dt.date
    if "entry_date" in df.columns:
        df["entry_date"] = pd.to_datetime(df["entry_date"]).dt.date
    return df

@st.cache_data(ttl=300)
def load_auditoria():
    return pd.read_sql("SELECT * FROM auditoria_etl ORDER BY id ASC", conn)

@st.cache_data(ttl=300)
def load_alerta_reposicao():
    return pd.read_sql("SELECT * FROM vw_alerta_reposicao", conn)

@st.cache_data(ttl=300)
def load_alerta_validade():
    return pd.read_sql("SELECT * FROM vw_alerta_validade", conn)

@st.cache_data(ttl=300)
def load_divergencia():
    return pd.read_sql("SELECT * FROM vw_divergencia_inventario", conn)

# Carga de todas as fontes
vendas_all   = load_vendas()
compras_all  = load_compras()
produtos     = load_produtos()
fornecedores = load_fornecedores()
estoque_raw  = load_estoque()
perdas_all   = load_perdas()
validade_raw = load_validade()
auditoria    = load_auditoria()
alerta_rep   = load_alerta_reposicao()
alerta_val   = load_alerta_validade()
divergencia  = load_divergencia()

# ─────────────────────────────────────────────────────────────────────────────
# 4. ENRIQUECIMENTO DOS DADOS E ASSOCIAÇÕES RELACIONAIS
# ─────────────────────────────────────────────────────────────────────────────
# Mapeamento do fornecedor habitual de cada produto a partir do histórico de compras
mapa_fornec_prod = (
    compras_all.groupby(["product_id", "supplier_id"])
    .size()
    .reset_index(name="compras_count")
    .sort_values(["product_id", "compras_count"], ascending=[True, False])
    .drop_duplicates(subset=["product_id"])
    .merge(fornecedores[["supplier_id", "trade_name", "contact_name", "contact_whatsapp", "lead_time_days"]], on="supplier_id", how="left")
)

# Enriquecimento de Produtos com dados cadastrais e de estoque
produtos_enriched = produtos.merge(
    mapa_fornec_prod[["product_id", "supplier_id", "trade_name", "contact_name", "contact_whatsapp", "lead_time_days"]],
    on="product_id",
    how="left",
)

# Enriquecimento de Estoque
estoque_enriched = estoque_raw.merge(
    produtos_enriched[["product_id", "product_name", "category", "unit_of_measure", "min_stock", "ideal_stock", "sale_price", "trade_name", "contact_whatsapp", "lead_time_days"]],
    on="product_id",
    how="left",
)

# Enriquecimento de Compras
compras_enriched = compras_all.merge(
    produtos[["product_id", "product_name", "category", "unit_of_measure"]],
    on="product_id",
    how="left",
).merge(
    fornecedores[["supplier_id", "trade_name", "contact_name", "contact_whatsapp", "lead_time_days"]],
    on="supplier_id",
    how="left",
)

# Enriquecimento de Vendas
vendas_enriched = vendas_all.merge(
    produtos_enriched[["product_id", "product_name", "category", "subcategory", "unit_of_measure", "trade_name"]],
    on="product_id",
    how="left",
)

# Enriquecimento de Perdas
perdas_enriched = perdas_all.merge(
    produtos_enriched[["product_id", "product_name", "category", "unit_of_measure", "trade_name"]],
    on="product_id",
    how="left",
)

# Enriquecimento da View de Reposição
alerta_rep_enriched = alerta_rep.merge(
    mapa_fornec_prod[["product_id", "supplier_id", "trade_name", "contact_name", "contact_whatsapp", "lead_time_days"]],
    on="product_id",
    how="left",
)
# Custo unitário mais recente de cada produto para estimar custo de reposição
ultimo_custo = compras_all.sort_values("purchase_date").groupby("product_id")["unit_cost"].last().reset_index()
alerta_rep_enriched = alerta_rep_enriched.merge(ultimo_custo, on="product_id", how="left")
alerta_rep_enriched["custo_estimado_reposicao"] = (
    alerta_rep_enriched["quantidade_sugerida"].clip(lower=0) * alerta_rep_enriched["unit_cost"]
)

# Enriquecimento da View de Validade
alerta_val_enriched = alerta_val.merge(
    mapa_fornec_prod[["product_id", "trade_name"]],
    on="product_id",
    how="left",
)

# Enriquecimento da View de Divergência
divergencia_enriched = divergencia.merge(
    produtos_enriched[["product_id", "category", "trade_name"]],
    on="product_id",
    how="left",
)

# Identificação Analítica de Candidatos a Promoção (Estoque Elevado + Baixa Saída)
# Vendas nos últimos 30 dias da simulação (2026-05-30 a 2026-06-29)
data_corte_30d = date(2026, 5, 30)
vendas_ultimos_30d = (
    vendas_all[vendas_all["date"] >= data_corte_30d]
    .groupby("product_id")
    .agg(qtd_30d=("quantity", "sum"), trans_30d=("sale_id", "count"))
    .reset_index()
)
estoque_loja = estoque_enriched[estoque_enriched["storage_location"] == "Loja"].copy()
promocoes_candidatos = estoque_loja.merge(vendas_ultimos_30d, on="product_id", how="left").fillna({"qtd_30d": 0, "trans_30d": 0})
promocoes_candidatos["excesso_estoque"] = promocoes_candidatos["current_quantity"] - promocoes_candidatos["ideal_stock"]
promocoes_candidatos["venda_diaria_recente"] = promocoes_candidatos["qtd_30d"] / 30.0
# Dias de cobertura projetada
promocoes_candidatos["dias_cobertura"] = promocoes_candidatos.apply(
    lambda r: round(r["current_quantity"] / r["venda_diaria_recente"], 1) if r["venda_diaria_recente"] > 0 else 999.0,
    axis=1,
)
# Flag de candidato: excesso físico (> 0) e giro lento (cobertura > 45 dias ou venda recente quase nula)
promocoes_candidatos["is_promo_candidate"] = (
    (promocoes_candidatos["excesso_estoque"] > 0) & 
    ((promocoes_candidatos["dias_cobertura"] > 45) | (promocoes_candidatos["qtd_30d"] <= 5))
)

# ─────────────────────────────────────────────────────────────────────────────
# 5. SIDEBAR: IDENTIDADE VISUAL E FILTROS DINÂMICOS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="brand-container">
          <div style="font-size: 2.2rem; line-height: 1;">🛒</div>
          <div class="brand-title">SUPERMERCADO BI</div>
          <div class="brand-subtitle">Supermercado Alvorada Ltda.</div>
          <div class="brand-slogan">"Dados organizados. Decisões inteligentes."</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎛️ Filtros Globais")

    # 1. Filtro de Período
    datas_vendas = vendas_all["date"].dropna().tolist()
    min_date_base = min(datas_vendas)
    max_date_base = max(datas_vendas)

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        data_inicio = st.date_input("De", value=min_date_base, min_value=min_date_base, max_value=max_date_base)
    with col_d2:
        data_fim = st.date_input("Até", value=max_date_base, min_value=min_date_base, max_value=max_date_base)

    if data_inicio > data_fim:
        st.error("Data inicial maior que a data final.")
        data_inicio = min_date_base

    # 2. Filtro de Categoria
    categorias_lista = sorted(produtos["category"].dropna().unique().tolist())
    cat_sel = st.multiselect("Categoria", options=categorias_lista, default=[])

    # 3. Filtro de Fornecedor
    fornecedores_lista = sorted(fornecedores["trade_name"].dropna().unique().tolist())
    fornec_sel = st.multiselect("Fornecedor", options=fornecedores_lista, default=[])

    # 4. Filtro de Produto
    # Filtrar produtos dinamicamente baseado na categoria selecionada se houver
    prods_disp = produtos.copy()
    if cat_sel:
        prods_disp = prods_disp[prods_disp["category"].isin(cat_sel)]
    if fornec_sel:
        ids_fornec = fornecedores[fornecedores["trade_name"].isin(fornec_sel)]["supplier_id"].tolist()
        prods_com_fornec = compras_all[compras_all["supplier_id"].isin(ids_fornec)]["product_id"].unique()
        prods_disp = prods_disp[prods_disp["product_id"].isin(prods_com_fornec)]

    produtos_lista = sorted(prods_disp["product_name"].dropna().unique().tolist())
    prod_sel = st.multiselect("Produto", options=produtos_lista, default=[])

    # 5. Filtro de Situação / Alerta
    alerta_opcoes = [
        "Todas as Situações",
        "🚨 Ruptura Crítica (Estoque < Mínimo)",
        "⚠️ Reposição Necessária (Estoque < Ideal)",
        "⏰ Validade Próxima (≤ 7 dias)",
        "📋 Divergência de Inventário (> 15%)",
        "🏷️ Candidato a Promoção (Excesso/Baixo Giro)",
        "📈 Aumento Relevante de Custo (> 10%)",
    ]
    alerta_sel = st.selectbox("Situação / Alerta", options=alerta_opcoes, index=0)

    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Redefinir Todos os Filtros", width="stretch"):
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.72rem; color: #64748b; line-height: 1.5;">
          <b>Parâmetros do Sistema:</b><br>
          • Período Histórico: 90 dias (01/04 a 29/06/2026)<br>
          • Data de Referência: 29/06/2026<br>
          • Produtos no Mix: 40 cadastrados<br>
          • Fornecedores Homologados: 8 parceiros<br>
          • Motor Analítico: SQLite + Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# 6. FUNÇÕES DE FILTRAGEM MULTIDIMENSIONAL
# ─────────────────────────────────────────────────────────────────────────────
# Determinar produtos que atendem ao filtro de alerta
produtos_alerta_ids = None
if alerta_sel == "🚨 Ruptura Crítica (Estoque < Mínimo)":
    produtos_alerta_ids = set(alerta_rep[alerta_rep["status_estoque"] == "CRITICO_RUPTURA"]["product_id"])
elif alerta_sel == "⚠️ Reposição Necessária (Estoque < Ideal)":
    produtos_alerta_ids = set(alerta_rep[alerta_rep["status_estoque"].isin(["CRITICO_RUPTURA", "REPOSICAO_NECESSARIA"])]["product_id"])
elif alerta_sel == "⏰ Validade Próxima (≤ 7 dias)":
    produtos_alerta_ids = set(alerta_val[alerta_val["dias_restantes"] <= 7]["product_id"])
elif alerta_sel == "📋 Divergência de Inventário (> 15%)":
    produtos_alerta_ids = set(divergencia[divergencia["divergencia_pct"].abs() > 15]["product_id"])
elif alerta_sel == "🏷️ Candidato a Promoção (Excesso/Baixo Giro)":
    produtos_alerta_ids = set(promocoes_candidatos[promocoes_candidatos["is_promo_candidate"]]["product_id"])
elif alerta_sel == "📈 Aumento Relevante de Custo (> 10%)":
    # Produtos com aumento > 10% entre a primeira e última compra
    prod_var_cost = []
    for pid, grp in compras_all.sort_values("purchase_date").groupby("product_id"):
        if len(grp) >= 2:
            c_ini = grp.iloc[0]["unit_cost"]
            c_fim = grp.iloc[-1]["unit_cost"]
            if ((c_fim - c_ini) / c_ini) > 0.10:
                prod_var_cost.append(pid)
    produtos_alerta_ids = set(prod_var_cost)

def filtrar_dataframe(df, date_col=None, prod_name_col="product_name", cat_col="category", prod_id_col="product_id", trade_name_col="trade_name"):
    df_filtered = df.copy()
    if date_col and date_col in df_filtered.columns:
        df_filtered = df_filtered[(df_filtered[date_col] >= data_inicio) & (df_filtered[date_col] <= data_fim)]
    if cat_sel and cat_col in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[cat_col].isin(cat_sel)]
    if fornec_sel and trade_name_col in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[trade_name_col].isin(fornec_sel)]
    if prod_sel and prod_name_col in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[prod_name_col].isin(prod_sel)]
    if produtos_alerta_ids is not None and prod_id_col in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[prod_id_col].isin(produtos_alerta_ids)]
    return df_filtered

# Aplicação dos filtros em todas as tabelas
vendas_fil   = filtrar_dataframe(vendas_enriched, date_col="date")
compras_fil  = filtrar_dataframe(compras_enriched, date_col="date")
perdas_fil   = filtrar_dataframe(perdas_enriched, date_col="date")
estoque_fil  = filtrar_dataframe(estoque_enriched)
alerta_rep_fil = filtrar_dataframe(alerta_rep_enriched)
alerta_val_fil = filtrar_dataframe(alerta_val_enriched)
divergencia_fil = filtrar_dataframe(divergencia_enriched)
promocoes_fil = filtrar_dataframe(promocoes_candidatos)

# ─────────────────────────────────────────────────────────────────────────────
# 7. CABEÇALHO PRINCIPAL DO DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
filtros_ativos_texto = []
if cat_sel:
    filtros_ativos_texto.append(f"Categorias: {', '.join(cat_sel)}")
if fornec_sel:
    filtros_ativos_texto.append(f"Fornecedores: {', '.join(fornec_sel)}")
if prod_sel:
    filtros_ativos_texto.append(f"Produtos: {len(prod_sel)} selecionado(s)")
if alerta_sel != "Todas as Situações":
    filtros_ativos_texto.append(f"Filtro de Alerta: {alerta_sel}")

st.markdown(
    f"""
    <div class="main-header">
      <div class="main-title">
        <span>🛒 SUPERMERCADO BI</span>
        <span class="main-title-badge">Painel de Decisão Estratégica</span>
      </div>
      <p class="main-subtitle">
        Supermercado Alvorada Ltda. &nbsp;|&nbsp; <em>"Dados organizados. Decisões inteligentes."</em>
      </p>
      <div class="context-chips">
        <span class="chip chip-accent">📅 Período: {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}</span>
        <span class="chip">📌 Referência de Validade/Estoque: 29/06/2026</span>
        <span class="chip">🔍 {len(vendas_fil):,} transações analisadas</span>
        {f'<span class="chip" style="background:#78350f; color:#fde047;">⚡ Filtros Ativos: {" | ".join(filtros_ativos_texto)}</span>' if filtros_ativos_texto else ''}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 8. ESTRUTURAÇÃO DAS 10 ABAS DO DASHBOARD (Conforme Requisitos do Projeto)
# ─────────────────────────────────────────────────────────────────────────────
tab_visao, tab_compras_int, tab_estoque, tab_validade, tab_promocoes, tab_fornecedores, tab_perdas, tab_alertas, tab_fiscal, tab_detalhes = st.tabs([
    "🏠 Visão Geral",
    "🛒 Compras Inteligentes",
    "📦 Estoque",
    "⏰ Validade",
    "🏷️ Promoções",
    "🤝 Fornecedores",
    "⚠️ Perdas",
    "🔔 Alertas",
    "📑 Fiscal & Gerencial",
    "📋 Detalhamento",
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1: VISÃO GERAL
# ═════════════════════════════════════════════════════════════════════════════
with tab_visao:
    # Métricas Globais
    fat_total_periodo = vendas_fil["total_amount"].sum()
    qtd_transacoes    = len(vendas_fil)
    total_compras     = compras_fil["total_cost"].sum()
    total_perdas_val  = perdas_fil["total_loss_value"].sum()
    
    # Estoque atual físico consolidado na Loja
    est_loja_tab1 = estoque_fil[estoque_fil["storage_location"] == "Loja"]
    valor_estoque_venda = (est_loja_tab1["current_quantity"] * est_loja_tab1["sale_price"]).sum()
    
    # Contadores Críticos
    criticos_ruptura_count = int((alerta_rep_fil["status_estoque"] == "CRITICO_RUPTURA").sum())
    vencem_7d_count        = int((alerta_val_fil["dias_restantes"] <= 7).sum()) if "dias_restantes" in alerta_val_fil.columns else 0
    candidatos_promo_count = int(promocoes_fil["is_promo_candidate"].sum())

    # Linha 1 de KPIs: Faturamento, Vendas, Compras, Valor em Estoque
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">💰 Faturamento Total</div>
                  <div class="kpi-value green">{fmt_brl(fat_total_periodo)}</div>
                  <div class="kpi-subtext">Período Selecionado</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        tkt_medio = (fat_total_periodo / qtd_transacoes) if qtd_transacoes > 0 else 0
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🧾 Vendas (Transações)</div>
                  <div class="kpi-value blue">{fmt_int(qtd_transacoes)}</div>
                  <div class="kpi-subtext">Ticket Médio: {fmt_brl(tkt_medio)}</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🛍️ Compras de Mercadoria</div>
                  <div class="kpi-value blue">{fmt_brl(total_compras)}</div>
                  <div class="kpi-subtext">{fmt_int(len(compras_fil))} pedidos de entrada</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🏪 Valor do Estoque Atual</div>
                  <div class="kpi-value green">{fmt_brl(valor_estoque_venda)}</div>
                  <div class="kpi-subtext">Avaliado a Preço de Venda</div>
                </div>""",
            unsafe_allow_html=True,
        )

    # Linha 2 de KPIs: Perdas, Produtos Críticos, Validade Iminente, Promoções
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        pct_perda_fat = (total_perdas_val / fat_total_periodo * 100) if fat_total_periodo > 0 else 0
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">⚠️ Perdas Operacionais</div>
                  <div class="kpi-value red">{fmt_brl(total_perdas_val)}</div>
                  <div class="kpi-subtext">{pct_perda_fat:.2f}% do Faturamento</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with c6:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🚨 Produtos em Ruptura</div>
                  <div class="kpi-value red">{fmt_int(criticos_ruptura_count)}</div>
                  <div class="kpi-subtext">Abaixo do Estoque Mínimo</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with c7:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">⏰ Vencimento em até 7 Dias</div>
                  <div class="kpi-value red">{fmt_int(vencem_7d_count)}</div>
                  <div class="kpi-subtext">Lotes perecíveis sob risco</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with c8:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🏷️ Candidatos a Promoção</div>
                  <div class="kpi-value yellow">{fmt_int(candidatos_promo_count)}</div>
                  <div class="kpi-subtext">Estoque Alto + Baixa Saída</div>
                </div>""",
            unsafe_allow_html=True,
        )

    # Painel dos 7 Cenários do Projeto Acadêmico
    st.markdown('<div class="section-title">🎯 Status dos Cenários de Negócio Criados</div>', unsafe_allow_html=True)
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.markdown(
            """
            <div class="scenario-card">
              <div class="scenario-card-header">
                <span class="scenario-name">🥛 Leite Integral 1L</span>
                <span class="scenario-badge badge-critico">Ruptura</span>
              </div>
              <div class="scenario-desc">Estoque atual (14 un) abaixo do mínimo (60 un). Necessidade urgente de 166 un.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="scenario-card">
              <div class="scenario-card-header">
                <span class="scenario-name">☕ Café 500g</span>
                <span class="scenario-badge badge-atencao">Promoção</span>
              </div>
              <div class="scenario-desc">Estoque elevado (118 un vs 80 ideal) com forte estagnação de vendas recentes.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with sc2:
        st.markdown(
            """
            <div class="scenario-card">
              <div class="scenario-card-header">
                <span class="scenario-name">🥣 Iogurte Natural</span>
                <span class="scenario-badge badge-critico">Vencimento</span>
              </div>
              <div class="scenario-desc">Lote LOT-IOG com 28 un vence em apenas 4 dias. Exige queima imediata.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="scenario-card">
              <div class="scenario-card-header">
                <span class="scenario-name">🍚 Arroz 5kg</span>
                <span class="scenario-badge badge-atencao">Salto Custo</span>
              </div>
              <div class="scenario-desc">Custo de compra subiu de R$ 18,23 para R$ 23,90 (+31,1%) na última NF-e.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with sc3:
        st.markdown(
            """
            <div class="scenario-card">
              <div class="scenario-card-header">
                <span class="scenario-name">🍌 Banana Prata</span>
                <span class="scenario-badge badge-critico">Perda Crítica</span>
              </div>
              <div class="scenario-desc">15 baixas operacionais por deterioração rápida, totalizando 143 kg (R$ 514,80).</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="scenario-card">
              <div class="scenario-card-header">
                <span class="scenario-name">📝 Lista de Cotação</span>
                <span class="scenario-badge badge-ok">Automação</span>
              </div>
              <div class="scenario-desc">4 itens críticos agrupados para cotação e envio automático para WhatsApp.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with sc4:
        st.markdown(
            """
            <div class="scenario-card">
              <div class="scenario-card-header">
                <span class="scenario-name">🌻 Óleo de Soja 900ml</span>
                <span class="scenario-badge badge-atencao">Desvio 20%</span>
              </div>
              <div class="scenario-desc">Divergência física/calculada de 20,0% superando o limite gerencial interno de 15%.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="scenario-card">
              <div class="scenario-card-header">
                <span class="scenario-name">🛡️ Auditoria do ETL</span>
                <span class="scenario-badge badge-info">Governança</span>
              </div>
              <div class="scenario-desc">8 saneamentos registrados (TRIM, quarentena de chaves órfãs e saldos negativos).</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Gráficos da Visão Geral
    st.markdown('<div class="section-title">📈 Evolução das Operações no Período</div>', unsafe_allow_html=True)
    col_vg1, col_vg2 = st.columns([3, 2])

    with col_vg1:
        # Faturamento Diário vs Compras Diárias
        vendas_dia = vendas_fil.groupby("date")["total_amount"].sum().reset_index()
        compras_dia = compras_fil.groupby("date")["total_cost"].sum().reset_index()
        df_fluxo = pd.merge(vendas_dia, compras_dia, on="date", how="outer").fillna(0).sort_values("date")

        fig_fluxo = go.Figure()
        fig_fluxo.add_trace(go.Scatter(
            x=df_fluxo["date"], y=df_fluxo["total_amount"],
            name="Faturamento (Vendas)",
            line=dict(color="#10b981", width=2.5),
            fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.12)'
        ))
        fig_fluxo.add_trace(go.Bar(
            x=df_fluxo["date"], y=df_fluxo["total_cost"],
            name="Compras (Entradas)",
            marker_color="rgba(59, 130, 246, 0.65)"
        ))
        fig_fluxo.update_layout(
            title="Fluxo Operacional Diário: Faturamento vs. Compras",
            plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
            font_color="#e2e8f0", title_font_size=13,
            legend=dict(orientation="h", y=1.1, x=0),
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b", title="R$"),
        )
        st.plotly_chart(fig_fluxo, width="stretch")

    with col_vg2:
        # Faturamento por Categoria
        cat_fat = vendas_fil.groupby("category")["total_amount"].sum().sort_values().reset_index()
        fig_cat = px.bar(
            cat_fat, x="total_amount", y="category", orientation="h",
            title="Faturamento por Categoria",
            labels={"category": "", "total_amount": "R$"},
            color="total_amount",
            color_continuous_scale=["#1e3a8a", "#10b981"],
        )
        fig_cat.update_layout(
            plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
            font_color="#e2e8f0", title_font_size=13,
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(gridcolor="#1e293b", title="R$"),
            yaxis=dict(gridcolor="#1e293b"),
        )
        st.plotly_chart(fig_cat, width="stretch")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2: COMPRAS INTELIGENTES (Com Lista de Cotação para WhatsApp)
# ═════════════════════════════════════════════════════════════════════════════
with tab_compras_int:
    st.markdown('<div class="section-title">🛒 Planejamento e Reposição Inteligente de Estoque</div>', unsafe_allow_html=True)

    # Filtrar produtos que exigem reposição
    rep_critica = alerta_rep_fil[alerta_rep_fil["status_estoque"] == "CRITICO_RUPTURA"].copy()
    rep_geral   = alerta_rep_fil[alerta_rep_fil["status_estoque"].isin(["CRITICO_RUPTURA", "REPOSICAO_NECESSARIA"])].copy()

    # KPIs de compras inteligentes
    custo_total_reposicao = rep_geral["custo_estimado_reposicao"].sum()
    itens_comprar_count   = len(rep_geral)
    fornecedores_acionar  = rep_geral["trade_name"].nunique()

    kc1, kc2, kc3, kc4 = st.columns(4)
    with kc1:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🚨 Itens em Ruptura Imediata</div>
                  <div class="kpi-value red">{fmt_int(len(rep_critica))}</div>
                  <div class="kpi-subtext">Abaixo do Estoque Mínimo</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kc2:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">📦 Total de Itens a Repor</div>
                  <div class="kpi-value yellow">{fmt_int(itens_comprar_count)}</div>
                  <div class="kpi-subtext">Abaixo do Estoque Ideal</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kc3:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">💵 Custo Estimado Reposição</div>
                  <div class="kpi-value blue">{fmt_brl(custo_total_reposicao)}</div>
                  <div class="kpi-subtext">Com base no último custo</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kc4:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🤝 Fornecedores Envolvidos</div>
                  <div class="kpi-value blue">{fmt_int(fornecedores_acionar)}</div>
                  <div class="kpi-subtext">Contatos cadastrados para pedido</div>
                </div>""",
            unsafe_allow_html=True,
        )

    # Tabela de Reposição Inteligente
    st.markdown("#### 📋 Sugestão Analítica de Compras por Item")
    if len(rep_geral) > 0:
        rep_display = rep_geral[[
            "product_name", "category", "unit_of_measure", "current_quantity",
            "min_stock", "ideal_stock", "quantidade_sugerida", "trade_name",
            "lead_time_days", "unit_cost", "custo_estimado_reposicao", "status_estoque"
        ]].copy().sort_values(["status_estoque", "quantidade_sugerida"], ascending=[True, False])

        rep_display["current_quantity"] = rep_display["current_quantity"].map("{:,.1f}".format)
        rep_display["min_stock"] = rep_display["min_stock"].map("{:,.1f}".format)
        rep_display["ideal_stock"] = rep_display["ideal_stock"].map("{:,.1f}".format)
        rep_display["quantidade_sugerida"] = rep_display["quantidade_sugerida"].map("{:,.1f}".format)
        rep_display["unit_cost"] = rep_display["unit_cost"].map("R$ {:,.2f}".format)
        rep_display["custo_estimado_reposicao"] = rep_display["custo_estimado_reposicao"].map("R$ {:,.2f}".format)

        rep_display.columns = [
            "Produto", "Categoria", "UN", "Estoque Atual", "Mínimo", "Ideal",
            "Qtd Sugerida", "Fornecedor", "Lead Time (dias)", "Último Custo",
            "Total Estimado", "Status"
        ]
        st.dataframe(rep_display, width="stretch", hide_index=True)
    else:
        st.success("✅ Todos os produtos filtrados estão com estoque adequado.")

    # ─────────────────────────────────────────────────────────────────────────
    # CENÁRIO 6: GERADOR AUTOMATIZADO DE LISTA DE COTAÇÃO PARA WHATSAPP
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📲 Cenário 6: Gerador de Lista de Cotação (Envio via WhatsApp)</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">
          Esta ferramenta agrupa os itens com necessidade de compra por fornecedor, calcula as quantidades sugeridas e formata o texto pronto para cópia ou envio direto para o WhatsApp do representante comercial.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_cot1, col_cot2 = st.columns([1, 1])

    with col_cot1:
        # Seleção do fornecedor para cotação
        fornecedores_com_pedidos = sorted(rep_geral["trade_name"].dropna().unique().tolist())
        if fornecedores_com_pedidos:
            fornec_escolhido = st.selectbox("Selecione o Fornecedor para Gerar Cotação:", options=fornecedores_com_pedidos)
            
            # Dados do fornecedor selecionado
            dados_fornec = fornecedores[fornecedores["trade_name"] == fornec_escolhido].iloc[0]
            itens_fornec = rep_geral[rep_geral["trade_name"] == fornec_escolhido].copy()

            # Opção de cotar apenas críticos ou todos abaixo do ideal
            apenas_criticos = st.checkbox("Incluir somente itens em RUPTURA CRÍTICA", value=False)
            if apenas_criticos:
                itens_fornec = itens_fornec[itens_fornec["status_estoque"] == "CRITICO_RUPTURA"]

            st.markdown(
                f"""
                <div class="whatsapp-box">
                  <div style="font-size: 0.95rem; font-weight: 700; color: #34d399;">
                    🏢 {dados_fornec['trade_name']} ({dados_fornec['company_name']})
                  </div>
                  <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 4px;">
                    👤 <b>Contato:</b> {dados_fornec['contact_name']} | 📱 <b>WhatsApp:</b> {dados_fornec['contact_whatsapp']}<br>
                    🚚 <b>Prazo de Entrega:</b> {dados_fornec['lead_time_days']} dias úteis | 📍 <b>Localização:</b> {dados_fornec['city_state']}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            fornec_escolhido = None
            st.info("Nenhum item pendente de reposição para os filtros atuais.")

    with col_cot2:
        if fornecedores_com_pedidos and fornec_escolhido and len(itens_fornec) > 0:
            # Formatação do texto estruturado
            linhas_itens = []
            for _, r in itens_fornec.iterrows():
                linhas_itens.append(f"• {r['product_name']}: {r['quantidade_sugerida']:.1f} {r['unit_of_measure']}")

            texto_cotacao = (
                f"Olá, {dados_fornec['contact_name']}! Tudo bem?\n\n"
                f"Aqui é do setor de compras do *Supermercado Alvorada Ltda.* (CNPJ: 12.345.678/0001-90).\n"
                f"Gostaríamos de solicitar cotação urgente e previsão de faturamento para os seguintes itens:\n\n"
                + "\n".join(linhas_itens) + "\n\n"
                f"Prazo habitual acordado: {dados_fornec['lead_time_days']} dias.\n"
                f"Por favor, nos confirme valores unitários e disponibilidade.\n"
                f"Obrigado!"
            )

            st.text_area("Mensagem Formatada (Pronta para Cópia):", value=texto_cotacao, height=190)

            # Link WhatsApp
            num_clean = "".join(filter(str.isdigit, str(dados_fornec["contact_whatsapp"])))
            if num_clean and len(num_clean) >= 10:
                link_wa = f"https://wa.me/55{num_clean}?text={texto_cotacao.replace(' ', '%20').replace(chr(10), '%0A')}"
                st.markdown(
                    f"""
                    <a href="{link_wa}" target="_blank" style="text-decoration:none;">
                      <div style="background:#10b981; color:#ffffff; padding:10px; border-radius:8px; text-align:center; font-weight:700; font-size:0.88rem; margin-top:8px;">
                        📲 Abrir Conversa no WhatsApp com {dados_fornec['contact_name']}
                      </div>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.warning("Número de WhatsApp do fornecedor não cadastrado para disparo automático.")
        elif fornecedores_com_pedidos and fornec_escolhido:
            st.info("Nenhum item atende ao critério de ruptura crítica para este fornecedor.")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3: ESTOQUE (Posições, Ruptura e Cobertura)
# ═════════════════════════════════════════════════════════════════════════════
with tab_estoque:
    st.markdown('<div class="section-title">📦 Gestão e Monitoramento de Estoque Físico</div>', unsafe_allow_html=True)

    est_loja = estoque_fil[estoque_fil["storage_location"] == "Loja"].copy()
    est_dep  = estoque_fil[estoque_fil["storage_location"] == "Depósito"].copy()

    total_unidades_loja = est_loja["current_quantity"].sum()
    itens_zerados       = int((est_loja["current_quantity"] <= 0).sum())
    itens_em_ruptura    = int((est_loja["current_quantity"] < est_loja["min_stock"]).sum())
    itens_adequados     = int((est_loja["current_quantity"] >= est_loja["min_stock"]).sum())

    ke1, ke2, ke3, ke4 = st.columns(4)
    with ke1:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🏪 Saldo em Loja (Gôndola)</div>
                  <div class="kpi-value green">{total_unidades_loja:,.0f} un</div>
                  <div class="kpi-subtext">{len(est_loja)} SKUs ativos na área de vendas</div>
                </div>""".replace(",", "."),
            unsafe_allow_html=True,
        )
    with ke2:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🚨 Risco Crítico de Ruptura</div>
                  <div class="kpi-value red">{itens_em_ruptura}</div>
                  <div class="kpi-subtext">Abaixo do estoque de segurança</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with ke3:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">✅ Estoque Adequado</div>
                  <div class="kpi-value green">{itens_adequados}</div>
                  <div class="kpi-subtext">Acima do mínimo operacional</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with ke4:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🏬 Posições no Depósito</div>
                  <div class="kpi-value blue">{len(est_dep)}</div>
                  <div class="kpi-subtext">{est_dep['current_quantity'].sum():,.0f} un em estoque pulmão</div>
                </div>""".replace(",", "."),
            unsafe_allow_html=True,
        )

    # Gráficos de Estoque
    st.markdown('<div class="section-title">📊 Diagnóstico Visual de Inventário</div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns([1, 1])

    with col_e1:
        # Scatter Estoque Atual vs Mínimo e Ideal
        def categorizar_estoque(r):
            if r["current_quantity"] <= 0:
                return "Zerado"
            elif r["current_quantity"] < r["min_stock"]:
                return "Crítico (Ruptura)"
            elif r["current_quantity"] < r["ideal_stock"]:
                return "Abaixo do Ideal"
            elif r["current_quantity"] <= r["ideal_stock"] * 1.25:
                return "Adequado"
            else:
                return "Excesso de Estoque"

        est_loja["status_detalhado"] = est_loja.apply(categorizar_estoque, axis=1)
        cores_status = {
            "Zerado": "#ef4444",
            "Crítico (Ruptura)": "#f87171",
            "Abaixo do Ideal": "#fbbf24",
            "Adequado": "#34d399",
            "Excesso de Estoque": "#60a5fa",
        }

        fig_scat = px.scatter(
            est_loja, x="min_stock", y="current_quantity",
            color="status_detalhado",
            hover_name="product_name",
            color_discrete_map=cores_status,
            labels={"min_stock": "Estoque Mínimo", "current_quantity": "Estoque Atual"},
            title="Estoque Atual vs. Estoque Mínimo (Por Produto)",
        )
        max_limit = max(est_loja["current_quantity"].max(), est_loja["min_stock"].max()) * 1.1 if len(est_loja) > 0 else 100
        fig_scat.add_shape(type="line", x0=0, y0=0, x1=max_limit, y1=max_limit, line=dict(color="#64748b", dash="dash"))
        fig_scat.update_layout(
            plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
            font_color="#e2e8f0", title_font_size=13,
            legend=dict(orientation="h", y=1.15, x=0),
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="#1e293b"),
        )
        st.plotly_chart(fig_scat, width="stretch")

    with col_e2:
        # Produtos em ruptura: Comparativo Atual vs Mínimo
        prod_ruptura = est_loja[est_loja["status_detalhado"].isin(["Zerado", "Crítico (Ruptura)"])].copy()
        if len(prod_ruptura) > 0:
            fig_rup = go.Figure()
            fig_rup.add_trace(go.Bar(
                x=prod_ruptura["product_name"], y=prod_ruptura["current_quantity"],
                name="Estoque Físico Atual", marker_color="#ef4444"
            ))
            fig_rup.add_trace(go.Bar(
                x=prod_ruptura["product_name"], y=prod_ruptura["min_stock"],
                name="Estoque Mínimo de Segurança", marker_color="#475569"
            ))
            fig_rup.update_layout(
                title=f"Itens Críticos ({len(prod_ruptura)} produtos abaixo do mínimo de segurança)",
                plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
                font_color="#e2e8f0", title_font_size=13,
                barmode="group",
                legend=dict(orientation="h", y=1.15, x=0),
                margin=dict(l=10, r=10, t=35, b=10),
                xaxis=dict(gridcolor="#1e293b", tickangle=-25),
                yaxis=dict(gridcolor="#1e293b", title="Unidades"),
            )
            st.plotly_chart(fig_rup, width="stretch")
        else:
            st.success("✅ Não há produtos em situação de ruptura sob os filtros atuais.")

    # Tabela de Posição Consolidada
    st.markdown("#### 📋 Posição Detalhada de Estoque por SKU")
    tabela_est_show = est_loja[[
        "product_name", "category", "unit_of_measure", "current_quantity",
        "min_stock", "ideal_stock", "sale_price", "trade_name", "status_detalhado"
    ]].copy().sort_values("current_quantity")

    tabela_est_show["sale_price"] = tabela_est_show["sale_price"].map("R$ {:,.2f}".format)
    tabela_est_show.columns = [
        "Produto", "Categoria", "UN", "Saldo em Loja", "Mínimo", "Ideal",
        "Preço Venda", "Fornecedor Habitual", "Classificação"
    ]
    st.dataframe(tabela_est_show, width="stretch", hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4: VALIDADE (Controle de Lotes e Shelf-Life)
# ═════════════════════════════════════════════════════════════════════════════
with tab_validade:
    st.markdown('<div class="section-title">⏰ Controle de Validade e Gestão de Shelf-Life</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 14px;">
          Monitoramento preventivo de lotes perecíveis calculados em relação à data de referência do sistema (<b>29/06/2026</b>).
        </div>
        """,
        unsafe_allow_html=True,
    )

    val_df = alerta_val_fil.copy()

    # Contadores
    lotes_criticos = val_df[val_df["dias_restantes"] <= 7] if "dias_restantes" in val_df.columns else pd.DataFrame()
    lotes_atencao  = val_df[(val_df["dias_restantes"] > 7) & (val_df["dias_restantes"] <= 15)] if "dias_restantes" in val_df.columns else pd.DataFrame()
    lotes_regular  = val_df[val_df["dias_restantes"] > 15] if "dias_restantes" in val_df.columns else pd.DataFrame()

    total_unidades_risco_7d = lotes_criticos["batch_quantity"].sum() if len(lotes_criticos) > 0 else 0

    kv1, kv2, kv3, kv4 = st.columns(4)
    with kv1:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🚨 Lotes Críticos (≤ 7 dias)</div>
                  <div class="kpi-value red">{len(lotes_criticos)}</div>
                  <div class="kpi-subtext">{total_unidades_risco_7d:.0f} unidades sob risco imediato</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kv2:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">⚠️ Lotes em Atenção (8-15 dias)</div>
                  <div class="kpi-value yellow">{len(lotes_atencao)}</div>
                  <div class="kpi-subtext">Monitorar giro no PDV</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kv3:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">✅ Lotes Regulares (> 15 dias)</div>
                  <div class="kpi-value green">{len(lotes_regular)}</div>
                  <div class="kpi-subtext">Validade segura</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kv4:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">📦 Total de Lotes Ativos</div>
                  <div class="kpi-value blue">{len(val_df)}</div>
                  <div class="kpi-subtext">{val_df['batch_quantity'].sum():,.0f} unidades controladas</div>
                </div>""".replace(",", "."),
            unsafe_allow_html=True,
        )

    # Destaque do Cenário 3 (Iogurte Natural)
    st.markdown(
        """
        <div class="alert-box alert-red">
          <span style="font-size:1.4rem;">🚨</span>
          <div>
            <b>CENÁRIO 3 IDENTIFICADO: Iogurte natural 170 g (Lote: LOT-IOG-20260618)</b><br>
            Validade em <b>03/07/2026</b> (apenas <b>4 dias restantes</b> para vencimento). Volume físico em risco: <b>28 unidades</b>.<br>
            <b>Ação Preventiva Recomendada:</b> Aplicar etiqueta promocional de desconto imediato ou realocar na ponta de gôndola para esgotamento em 48h.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Gráfico de Dias Restantes por Lote
    if len(val_df) > 0:
        val_df_sorted = val_df.sort_values("dias_restantes").copy()
        cores_validade = []
        for d in val_df_sorted["dias_restantes"]:
            if d <= 7:
                cores_validade.append("#ef4444")
            elif d <= 15:
                cores_validade.append("#f59e0b")
            else:
                cores_validade.append("#10b981")

        fig_val = go.Figure(go.Bar(
            x=val_df_sorted["dias_restantes"],
            y=val_df_sorted["product_name"] + " (" + val_df_sorted["batch_id"] + ")",
            orientation="h",
            marker_color=cores_validade,
            text=val_df_sorted["dias_restantes"].astype(str) + " dias",
            textposition="auto",
        ))
        fig_val.update_layout(
            title="Dias Restantes até o Vencimento por Lote Perecível",
            plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
            font_color="#e2e8f0", title_font_size=13,
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(gridcolor="#1e293b", title="Dias até Vencimento"),
            yaxis=dict(gridcolor="#1e293b", autorange="reversed"),
        )
        st.plotly_chart(fig_val, width="stretch")

        # Tabela Detalhada de Lotes
        st.markdown("#### 📋 Matriz Detalhada de Controle de Validades")
        val_show_table = val_df_sorted[[
            "batch_id", "product_name", "category", "expiration_date",
            "batch_quantity", "dias_restantes", "status_vencimento"
        ]].copy()

        def definir_prioridade(dias):
            if dias <= 7:
                return "1 - URGENTE (Desconto/Queima)"
            elif dias <= 15:
                return "2 - ATENÇÃO (Ponta de Gôndola)"
            return "3 - REGULAR (Monitoramento)"

        val_show_table["Ação Recomendada"] = val_show_table["dias_restantes"].apply(definir_prioridade)
        val_show_table.columns = [
            "Código do Lote", "Produto", "Categoria", "Data de Vencimento",
            "Quantidade em Lote", "Dias Restantes", "Status", "Prioridade de Ação"
        ]
        st.dataframe(val_show_table, width="stretch", hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5: PROMOÇÕES (Estoque Elevado + Baixa Saída)
# ═════════════════════════════════════════════════════════════════════════════
with tab_promocoes:
    st.markdown('<div class="section-title">🏷️ Oportunidades Promocionais: Estoque Elevado & Baixo Giro</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 14px;">
          Identificação gerencial de capital de giro imobilizado em itens com volume físico acima do ideal e desaceleração relevante nas vendas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    promo_cand_df = promocoes_fil[promocoes_fil["is_promo_candidate"]].copy()

    # Destaque do Cenário 2 (Café 500g)
    st.markdown(
        """
        <div class="alert-box alert-yellow">
          <span style="font-size:1.4rem;">🏷️</span>
          <div>
            <b>CENÁRIO 2 IDENTIFICADO: Café 500 g (Mercearia Seca)</b><br>
            • Estoque Físico Atual: <b>118 unidades</b> vs Estoque Ideal de <b>80 unidades</b> (Excesso de <b>38 unidades</b>).<br>
            • Desaceleração de Vendas: Em abril foram vendidas 74 unidades; em maio 37 unidades; e em junho <b>apenas 1 unidade</b> registrada!<br>
            • <b>Diagnóstico Gerencial:</b> Capital de giro imobilizado em produto estagnado. Recomendada queima promocional para recomposição de fluxo de caixa.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpr1, kpr2, kpr3 = st.columns(3)
    with kpr1:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🏷️ SKUs Candidatos a Promoção</div>
                  <div class="kpi-value yellow">{len(promo_cand_df)}</div>
                  <div class="kpi-subtext">Estoque Alto + Giro Estagnado</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kpr2:
        val_excesso_capital = (promo_cand_df["excesso_estoque"] * promo_cand_df["sale_price"]).sum() if len(promo_cand_df) > 0 else 0
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">💰 Capital Imobilizado em Excesso</div>
                  <div class="kpi-value yellow">{fmt_brl(val_excesso_capital)}</div>
                  <div class="kpi-subtext">Excedente avaliado a preço de venda</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kpr3:
        qtd_total_excedente = promo_cand_df["excesso_estoque"].sum() if len(promo_cand_df) > 0 else 0
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">📦 Volume Físico Excedente</div>
                  <div class="kpi-value blue">{qtd_total_excedente:,.0f} un</div>
                  <div class="kpi-subtext">Acima do estoque ideal</div>
                </div>""".replace(",", "."),
            unsafe_allow_html=True,
        )

    # Tabela Analítica de Candidatos
    st.markdown("#### 📋 Relação de Itens com Cobertura Excessiva")
    if len(promo_cand_df) > 0:
        show_promo_t = promo_cand_df[[
            "product_name", "category", "current_quantity", "ideal_stock",
            "excesso_estoque", "qtd_30d", "dias_cobertura", "sale_price"
        ]].copy().sort_values("excesso_estoque", ascending=False)

        show_promo_t["dias_cobertura"] = show_promo_t["dias_cobertura"].apply(lambda d: f"{d:.0f} dias" if d < 999 else "Estagnado (> 1 ano)")
        show_promo_t["sale_price"] = show_promo_t["sale_price"].map("R$ {:,.2f}".format)
        show_promo_t.columns = [
            "Produto", "Categoria", "Estoque Atual", "Estoque Ideal",
            "Excesso Físico", "Vendas Últimos 30d", "Cobertura Projetada", "Preço Normal"
        ]
        st.dataframe(show_promo_t, width="stretch", hide_index=True)

        # Simulador de Ação Promocional
        st.markdown("#### 🧮 Simulador Gerencial de Elasticidade e Desconto Promocional")
        st.markdown(
            """
            <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 8px;">
              <em>Nota de Governança:</em> O BI identifica o problema e projeta os cenários. A decisão da margem e desconto promocional cabe exclusivamente à gerência comercial.
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_sim1, col_sim2 = st.columns([1, 1])
        with col_sim1:
            prod_sim = st.selectbox("Selecione o Produto para Simulação:", options=promo_cand_df["product_name"].tolist())
            row_sim = promo_cand_df[promo_cand_df["product_name"] == prod_sim].iloc[0]
            pct_desc = st.slider("Percentual de Desconto Simulado (%):", min_value=5, max_value=40, value=15, step=5)

        with col_sim2:
            preco_normal = row_sim["sale_price"]
            preco_promo  = preco_normal * (1 - (pct_desc / 100))
            recuperacao_capital = row_sim["excesso_estoque"] * preco_promo

            st.markdown(
                f"""
                <div style="background:#131d2e; border:1px solid #334155; border-radius:10px; padding:14px;">
                  <b>Simulação Comercial: {prod_sim}</b><br>
                  • Preço de Venda Regular: <b>{fmt_brl(preco_normal)}</b><br>
                  • Preço Promocional Sugerido (-{pct_desc}%): <b style="color:#34d399;">{fmt_brl(preco_promo)}</b><br>
                  • Capital Liberado com a Venda do Excesso ({row_sim['excesso_estoque']:.0f} un): <b style="color:#60a5fa;">{fmt_brl(recuperacao_capital)}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Nenhum produto atende aos critérios de estoque excessivo com baixo giro no momento.")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 6: FORNECEDORES (Histórico de Custos e Variação de Preços)
# ═════════════════════════════════════════════════════════════════════════════
with tab_fornecedores:
    st.markdown('<div class="section-title">🤝 Análise de Fornecedores & Monitoramento de Custos de Aquisição</div>', unsafe_allow_html=True)

    # Identificação do Cenário 4: Arroz 5kg
    st.markdown(
        """
        <div class="alert-box alert-yellow">
          <span style="font-size:1.4rem;">📈</span>
          <div>
            <b>CENÁRIO 4 IDENTIFICADO: Variação Relevante de Custo no Arroz 5 kg (ID 8)</b><br>
            • Fornecedor: <b>Distribuidora MixSul (FOR-008)</b>.<br>
            • Evolução do Custo Unitário: Manteve-se estável em média a <b>R$ 18,30</b> durante abril, maio e início de junho.<br>
            • <b>Salto em 26/06/2026:</b> Custo unitário saltou para <b>R$ 23,90</b> (+31,1% de aumento atípico na nota de compra).<br>
            • <b>Impacto Gerencial:</b> Necessidade urgente de reajuste do preço final na gôndola ou cotação de marcas concorrentes para preservar a margem.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Gráfico de Variação de Preço de Custo ao Longo do Tempo
    st.markdown("#### 💹 Histórico e Oscilação de Preços de Compra por Produto")
    prods_com_historico = sorted(compras_fil["product_name"].dropna().unique().tolist())

    if prods_com_historico:
        # Default: Arroz 5 kg se presente, ou top produto
        default_prod = ["Arroz 5 kg"] if "Arroz 5 kg" in prods_com_historico else [prods_com_historico[0]]
        prods_escolhidos_graf = st.multiselect(
            "Selecione o(s) Produto(s) para comparar a série de custos:",
            options=prods_com_historico,
            default=default_prod,
        )

        if prods_escolhidos_graf:
            df_custo_tempo = (
                compras_fil[compras_fil["product_name"].isin(prods_escolhidos_graf)]
                .sort_values("purchase_date")
            )
            fig_custo = px.line(
                df_custo_tempo, x="purchase_date", y="unit_cost", color="product_name",
                markers=True,
                title="Evolução do Custo Unitário de Entrada nas Notas Fiscais (NF-e)",
                labels={"purchase_date": "Data da Compra", "unit_cost": "Custo Unitário (R$)", "product_name": "Produto"},
            )
            fig_custo.update_layout(
                plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
                font_color="#e2e8f0", title_font_size=13,
                legend=dict(orientation="h", y=1.1, x=0),
                margin=dict(l=10, r=10, t=35, b=10),
                xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="#1e293b", title="R$"),
            )
            st.plotly_chart(fig_custo, width="stretch")

        # Tabela consolidada de evolução de custos
        var_custo_rows = []
        for pid, grp in compras_fil.sort_values("purchase_date").groupby("product_id"):
            if len(grp) >= 2:
                c_ini = grp.iloc[0]["unit_cost"]
                c_fim = grp.iloc[-1]["unit_cost"]
                var_pct = ((c_fim - c_ini) / c_ini) * 100
                var_custo_rows.append({
                    "Produto": grp.iloc[0]["product_name"],
                    "Categoria": grp.iloc[0]["category"],
                    "Fornecedor": grp.iloc[0]["trade_name"],
                    "Custo Inicial": fmt_brl(c_ini),
                    "Custo Recente": fmt_brl(c_fim),
                    "Variação (%)": f"{var_pct:+.1f}%",
                    "Situação": "⚠️ Aumento Relevante" if var_pct > 10.0 else ("🔻 Redução" if var_pct < -5.0 else "Estável"),
                })
        if var_custo_rows:
            st.markdown("##### 📊 Comparativo de Variação de Preços (Primeira vs. Última Compra)")
            df_var_tab = pd.DataFrame(var_custo_rows).sort_values("Variação (%)", ascending=False)
            st.dataframe(df_var_tab, width="stretch", hide_index=True)

    # Ranking de Fornecedores por Volume Comprado
    st.markdown("#### 🏆 Comparativo de Fornecimento no Período")
    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        rank_fornec = compras_fil.groupby("trade_name").agg(
            total_gasto=("total_cost", "sum"),
            pedidos=("purchase_id", "nunique"),
            volume_itens=("quantity", "sum")
        ).reset_index().sort_values("total_gasto", ascending=False)

        fig_fornec = px.bar(
            rank_fornec, x="total_gasto", y="trade_name", orientation="h",
            title="Volume Financeiro Comprado por Fornecedor (R$)",
            labels={"trade_name": "", "total_gasto": "Total Comprado (R$)"},
            color="total_gasto",
            color_continuous_scale=["#1e3a8a", "#3b82f6"],
        )
        fig_fornec.update_layout(
            plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
            font_color="#e2e8f0", title_font_size=13,
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="#1e293b", autorange="reversed"),
        )
        st.plotly_chart(fig_fornec, width="stretch")

    with col_f2:
        # Tabela Cadastral dos Fornecedores
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#f8fafc; margin-bottom:8px;'>Catálogo de Fornecedores Homologados</div>", unsafe_allow_html=True)
        tab_fornec_disp = fornecedores[[
            "trade_name", "company_name", "cnpj", "contact_name",
            "contact_whatsapp", "lead_time_days", "city_state"
        ]].copy()
        tab_fornec_disp.columns = ["Nome Fantasia", "Razão Social", "CNPJ", "Representante", "WhatsApp", "Lead Time (dias)", "Cidade/UF"]
        st.dataframe(tab_fornec_disp, width="stretch", hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 7: PERDAS (Quebras, Avarias e Desperdício)
# ═════════════════════════════════════════════════════════════════════════════
with tab_perdas:
    st.markdown('<div class="section-title">⚠️ Gestão de Perdas, Avarias e Desperdício Operacional</div>', unsafe_allow_html=True)

    val_total_perdas = perdas_fil["total_loss_value"].sum()
    qtd_total_perdas = perdas_fil["quantity"].sum()
    registros_perdas = len(perdas_fil)
    cat_mais_afetada = perdas_fil.groupby("category")["total_loss_value"].sum().idxmax() if len(perdas_fil) > 0 else "—"

    kp1, kp2, kp3, kp4 = st.columns(4)
    with kp1:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">💸 Prejuízo Total com Perdas</div>
                  <div class="kpi-value red">{fmt_brl(val_total_perdas)}</div>
                  <div class="kpi-subtext">Acumulado no período</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kp2:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">📦 Quantidade Física Baixada</div>
                  <div class="kpi-value yellow">{qtd_total_perdas:,.1f}</div>
                  <div class="kpi-subtext">Kg / Unidades descartadas</div>
                </div>""".replace(",", "."),
            unsafe_allow_html=True,
        )
    with kp3:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🥬 Categoria Mais Afetada</div>
                  <div class="kpi-value yellow" style="font-size:1.35rem;">{cat_mais_afetada}</div>
                  <div class="kpi-subtext">Maior volume de descarte</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kp4:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">📋 Apontamentos Operacionais</div>
                  <div class="kpi-value blue">{registros_perdas}</div>
                  <div class="kpi-subtext">Baixas registradas</div>
                </div>""",
            unsafe_allow_html=True,
        )

    # Destaque do Cenário 5 (Banana Prata)
    st.markdown(
        """
        <div class="alert-box alert-red">
          <span style="font-size:1.4rem;">🍌</span>
          <div>
            <b>CENÁRIO 5 IDENTIFICADO: Desperdício Elevado em Banana Prata (Hortifrúti)</b><br>
            • Foram registrados <b>15 apontamentos de perdas</b> para o item, somando <b>143,0 kg descartados</b>.<br>
            • Prejuízo financeiro acumulado: <b>R$ 514,80</b> (motivo principal: deterioração acelerada por acondicionamento inadequado).<br>
            • <b>Ação Recomendada:</b> Ajuste na climatização da câmara fria de hortifrúti e revisão da frequência de compra (pedidos mais frequentes em menor volume).
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Gráficos de Perdas
    col_p1, col_p2 = st.columns([1, 1])

    with col_p1:
        # Perdas por Motivo
        motivos_df = perdas_fil.groupby("loss_reason")["total_loss_value"].sum().reset_index().sort_values("total_loss_value", ascending=False)
        fig_mot = px.pie(
            motivos_df, values="total_loss_value", names="loss_reason",
            title="Distribuição do Valor de Perdas por Motivo",
            hole=0.45,
            color_discrete_sequence=["#ef4444", "#f59e0b", "#3b82f6", "#64748b"],
        )
        fig_mot.update_layout(
            plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
            font_color="#e2e8f0", title_font_size=13,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(l=10, r=10, t=35, b=10),
        )
        fig_mot.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig_mot, width="stretch")

    with col_p2:
        # Top 8 Produtos com Maiores Perdas
        top_perdas = perdas_fil.groupby("product_name")["total_loss_value"].sum().nlargest(8).reset_index().sort_values("total_loss_value")
        fig_tp = px.bar(
            top_perdas, x="total_loss_value", y="product_name", orientation="h",
            title="Top 8 Produtos com Maior Prejuízo por Perdas",
            labels={"product_name": "", "total_loss_value": "R$ Perdido"},
            color="total_loss_value",
            color_continuous_scale="Reds",
        )
        fig_tp.update_layout(
            plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
            font_color="#e2e8f0", title_font_size=13,
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(gridcolor="#1e293b", title="R$"), yaxis=dict(gridcolor="#1e293b"),
        )
        st.plotly_chart(fig_tp, width="stretch")

    # Detalhamento de Perdas
    st.markdown("#### 📋 Detalhamento dos Registros de Perdas")
    tabela_perdas_show = perdas_fil[[
        "date", "product_name", "category", "quantity", "unit_of_measure",
        "loss_reason", "unit_cost_at_loss", "total_loss_value"
    ]].copy().sort_values("date", ascending=False)

    tabela_perdas_show["unit_cost_at_loss"] = tabela_perdas_show["unit_cost_at_loss"].map("R$ {:,.2f}".format)
    tabela_perdas_show["total_loss_value"]  = tabela_perdas_show["total_loss_value"].map("R$ {:,.2f}".format)
    tabela_perdas_show.columns = [
        "Data", "Produto", "Categoria", "Qtd Descartada", "UN",
        "Motivo do Descarte", "Custo Unitário", "Valor do Prejuízo"
    ]
    st.dataframe(tabela_perdas_show, width="stretch", hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 8: ALERTAS GERENCIAIS (Críticos, Atenção e Informativos)
# ═════════════════════════════════════════════════════════════════════════════
with tab_alertas:
    st.markdown('<div class="section-title">🔔 Central de Alertas & Notificações Acionáveis</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 16px;">
          Painel centralizador que consolida todas as anomalias e oportunidades detectadas nos cruzamentos de dados, categorizadas por severidade.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_al1, col_al2, col_al3 = st.columns(3)

    # 1. ALERTAS CRÍTICOS (Ação Imediata)
    with col_al1:
        st.markdown("#### 🔴 Alertas Críticos (Ação Imediata)")
        
        # Ruptura
        itens_rup = alerta_rep_fil[alerta_rep_fil["status_estoque"] == "CRITICO_RUPTURA"]
        if len(itens_rup) > 0:
            st.markdown(
                f"""
                <div class="alert-box alert-red">
                  <b>🚨 Ruptura Crítica ({len(itens_rup)} produtos):</b><br>
                  {", ".join(itens_rup["product_name"].tolist())}.<br>
                  <em>Estoque atual abaixo do limite de segurança. Risco iminente de falta.</em>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Validade <= 7 dias
        itens_venc_crit = alerta_val_fil[alerta_val_fil["dias_restantes"] <= 7] if "dias_restantes" in alerta_val_fil.columns else pd.DataFrame()
        if len(itens_venc_crit) > 0:
            for _, r in itens_venc_crit.iterrows():
                st.markdown(
                    f"""
                    <div class="alert-box alert-red">
                      <b>⏰ Vencimento Próximo ({r['dias_restantes']} dias):</b><br>
                      {r['product_name']} (Lote: {r['batch_id']}) — {r['batch_quantity']:.0f} unidades vencem em {r['expiration_date']}.<br>
                      <em>Aplicar queima de estoque imediata.</em>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if len(itens_rup) == 0 and len(itens_venc_crit) == 0:
            st.markdown(
                """
                <div class="alert-box alert-green">
                  <b>✅ Nenhum Alerta Crítico Ativo:</b><br>
                  Não há produtos em ruptura ou com validade inferior a 7 dias sob os filtros selecionados.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # 2. ALERTAS DE ATENÇÃO (Planejamento)
    with col_al2:
        st.markdown("#### 🟡 Alertas de Atenção (Planejamento)")

        # Reposição necessária (estoque < ideal)
        itens_rep_nec = alerta_rep_fil[alerta_rep_fil["status_estoque"] == "REPOSICAO_NECESSARIA"]
        if len(itens_rep_nec) > 0:
            st.markdown(
                f"""
                <div class="alert-box alert-yellow">
                  <b>⚠️ Reposição Necessária ({len(itens_rep_nec)} SKUs):</b><br>
                  Itens operando abaixo do estoque ideal. Programar compras antes de atingir o mínimo.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Validade entre 8 e 15 dias
        itens_venc_atencao = alerta_val_fil[(alerta_val_fil["dias_restantes"] > 7) & (alerta_val_fil["dias_restantes"] <= 15)] if "dias_restantes" in alerta_val_fil.columns else pd.DataFrame()
        if len(itens_venc_atencao) > 0:
            st.markdown(
                f"""
                <div class="alert-box alert-yellow">
                  <b>⏰ Atenção de Shelf-Life ({len(itens_venc_atencao)} lotes):</b><br>
                  Lotes com validade entre 8 e 15 dias. Destacar na área de vendas.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Divergência de Inventário > 15%
        itens_div_15 = divergencia_fil[divergencia_fil["divergencia_pct"].abs() > 15] if "divergencia_pct" in divergencia_fil.columns else pd.DataFrame()
        if len(itens_div_15) > 0:
            for _, r in itens_div_15.iterrows():
                st.markdown(
                    f"""
                    <div class="alert-box alert-yellow">
                      <b>📋 Divergência de Inventário ({r['divergencia_pct']:.1f}%):</b><br>
                      {r['product_name']} — Estoque Físico ({r['estoque_registrado']:.0f}) diverge do Calculado ({r['estoque_calculado']:.0f}).<br>
                      <em>Parâmetro gerencial excedido. Recomenda-se recontagem física.</em>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Salto de Custo de Compra > 10%
        custos_elevados = []
        for pid, grp in compras_fil.sort_values("purchase_date").groupby("product_id"):
            if len(grp) >= 2:
                c_ini = grp.iloc[0]["unit_cost"]
                c_fim = grp.iloc[-1]["unit_cost"]
                var_c = ((c_fim - c_ini) / c_ini) * 100
                if var_c > 10.0:
                    custos_elevados.append((grp.iloc[0]["product_name"], c_ini, c_fim, var_c))
        
        if custos_elevados:
            for pname, c_ini, c_fim, var_c in custos_elevados:
                st.markdown(
                    f"""
                    <div class="alert-box alert-yellow">
                      <b>📈 Aumento no Custo de Aquisição:</b><br>
                      {pname} teve elevação de <b>+{var_c:.1f}%</b> na última compra ({fmt_brl(c_ini)} ➔ {fmt_brl(c_fim)}).
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        elif len(itens_rep_nec) == 0 and len(itens_venc_atencao) == 0 and len(itens_div_15) == 0:
            st.markdown(
                """
                <div class="alert-box alert-green">
                  <b>✅ Situação Regular:</b><br>
                  Nenhuma anomalia de atenção detectada sob os filtros atuais.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # 3. ALERTAS INFORMATIVOS (Oportunidades e Governança)
    with col_al3:
        st.markdown("#### 🔵 Alertas Informativos (Oportunidades)")

        # Promoção (Café 500g e outros)
        itens_promo_info = promocoes_fil[promocoes_fil["is_promo_candidate"]] if "is_promo_candidate" in promocoes_fil.columns else pd.DataFrame()
        if len(itens_promo_info) > 0:
            st.markdown(
                f"""
                <div class="alert-box alert-blue">
                  <b>🏷️ Oportunidade Promocional ({len(itens_promo_info)} produtos):</b><br>
                  {", ".join(itens_promo_info["product_name"].tolist())}.<br>
                  <em>Estoque acima do ideal com demanda estagnada. Oportunidade de queima.</em>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Governança do ETL
        st.markdown(
            f"""
            <div class="alert-box alert-green">
              <b>🛡️ Governança de Dados Concluída:</b><br>
              O pipeline de ETL saneou 8 inconsistências operacionais e isolou registros anômalos em quarentena de inventário.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ═════════════════════════════════════════════════════════════════════════════
# TAB 9: FISCAL & GERENCIAL (Divergências e Análise Indicativa de ICMS)
# ═════════════════════════════════════════════════════════════════════════════
with tab_fiscal:
    st.markdown('<div class="section-title">📑 Indicadores Fiscais & Auditoria Gerencial de Estoque</div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # AVISO METODOLÓGICO OBRIGATÓRIO
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="disclaimer-card">
          <b>⚠️ NOTA DE ESCLARECIMENTO METODOLÓGICO E GERENCIAL:</b><br>
          1. <b>Parâmetro Interno de Divergência (15%):</b> A regra de corte de 15% utilizada neste painel é <b>exclusivamente um parâmetro interno de governança e auditoria operacional</b> adotado pela gestão do Supermercado Alvorada Ltda. para deflagrar recontagens físicas e averiguação de perdas não apontadas. <b>Não se trata nem deve ser interpretada como regra, presunção ou parâmetro fiscal/tributário oficial.</b><br>
          2. <b>Informações de ICMS:</b> Os valores de base de cálculo, alíquotas e montantes de ICMS refletem os registros de emissão contidos nos documentos fiscais de entrada (NF-e) e saída (NFC-e) para fins de acompanhamento gerencial e planejamento de compras. <b>Não configuram apuração contábil-tributária definitiva nem atestam automaticamente direito a crédito ou compensação tributária</b>, os quais exigem validação pelas regras do regime de tributação aplicável por profissional contábil habilitado.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SEÇÃO 1: AUDITORIA DE DIVERGÊNCIA DE INVENTÁRIO (Cenário 7)
    st.markdown("#### 1. Auditoria de Divergência de Inventário (Parâmetro Interno: 15%)")
    st.markdown(
        """
        <div style="font-size:0.83rem; color:#94a3b8; margin-bottom:10px;">
          Confronto contábil da equação de movimentações: <code>Estoque Calculado = Estoque Inicial + Compras − Vendas − Perdas</code> comparado com o <code>Estoque Registrado</code> na contagem física.
        </div>
        """,
        unsafe_allow_html=True,
    )

    div_acima_15 = divergencia_fil[divergencia_fil["divergencia_pct"].abs() > 15].copy() if "divergencia_pct" in divergencia_fil.columns else pd.DataFrame()
    maior_desvio = divergencia_fil["divergencia_pct"].abs().max() if len(divergencia_fil) > 0 and "divergencia_pct" in divergencia_fil.columns else 0
    icms_tot_comp = compras_fil["icms_amount"].sum() if "icms_amount" in compras_fil.columns else 0
    icms_tot_vend = vendas_fil["icms_amount"].sum() if "icms_amount" in vendas_fil.columns else 0

    kf1, kf2, kf3, kf4 = st.columns(4)
    with kf1:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">🔍 Itens c/ Desvio > 15%</div>
                  <div class="kpi-value yellow">{fmt_int(len(div_acima_15))}</div>
                  <div class="kpi-subtext">Parâmetro interno excedido</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kf2:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">📈 Maior Divergência</div>
                  <div class="kpi-value red">{maior_desvio:.2f}%</div>
                  <div class="kpi-subtext">Óleo de Soja 900ml (20,0%)</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kf3:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">📥 ICMS Entradas (NF-e)</div>
                  <div class="kpi-value blue">{fmt_brl(icms_tot_comp)}</div>
                  <div class="kpi-subtext">{fmt_int(len(compras_fil))} notas de compra</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with kf4:
        st.markdown(
            f"""<div class="kpi-card">
                  <div class="kpi-label">📤 ICMS Saídas (Vendas)</div>
                  <div class="kpi-value green">{fmt_brl(icms_tot_vend)}</div>
                  <div class="kpi-subtext">{fmt_int(len(vendas_fil))} cupons no período</div>
                </div>""",
            unsafe_allow_html=True,
        )

    if len(div_acima_15) > 0:
        st.markdown(
            f"""
            <div class="alert-box alert-yellow">
              <span style="font-size:1.4rem;">🌻</span>
              <div>
                <b>CENÁRIO 7 IDENTIFICADO: Divergência Acima do Parâmetro Interno no Óleo de soja 900 ml (ID 10)</b><br>
                • Estoque Físico Registrado no Sistema: <b>128,0 unidades</b>.<br>
                • Estoque Calculado Contábil (Inicial + Entradas − Saídas − Baixas): <b>160,0 unidades</b>.<br>
                • <b>Divergência Apurada: 20,00%</b> (superior ao limite de tolerância gerencial interna de 15%).<br>
                • <b>Encaminhamento Gerencial:</b> Abrir chamado de auditoria física de inventário e conferência de notas de recebimento.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Gráfico de Barras de Divergência com Linha de Tolerância de 15%
    if len(divergencia_fil) > 0 and "divergencia_pct" in divergencia_fil.columns:
        fig_div = px.bar(
            divergencia_fil.sort_values("divergencia_pct", ascending=False),
            x="product_name",
            y="divergencia_pct",
            color="divergencia_pct",
            color_continuous_scale=["#10b981", "#fbbf24", "#ef4444"],
            title="Divergência Percentual de Inventário por Produto (Confronto Físico vs. Calculado)",
            labels={"product_name": "Produto", "divergencia_pct": "Divergência (%)"},
        )
        fig_div.add_hline(y=15, line_dash="dash", line_color="#ef4444", annotation_text="Limite Interno (+15%)", annotation_position="top right")
        fig_div.add_hline(y=-15, line_dash="dash", line_color="#ef4444", annotation_text="Limite Interno (-15%)", annotation_position="bottom right")
        fig_div.update_layout(
            plot_bgcolor="#131d2e", paper_bgcolor="#131d2e",
            font_color="#e2e8f0", title_font_size=13,
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(gridcolor="#1e293b", tickangle=-45),
            yaxis=dict(gridcolor="#1e293b", title="Divergência (%)"),
        )
        st.plotly_chart(fig_div, width="stretch")

    tabela_div_show = divergencia_fil[[
        "product_id", "product_name", "estoque_registrado", "estoque_calculado", "divergencia_pct"
    ]].copy().sort_values("divergencia_pct", ascending=False)
    tabela_div_show["Situação"] = tabela_div_show["divergencia_pct"].apply(
        lambda x: "⚠️ Divergência > 15%" if abs(x) > 15 else "✅ Dentro do Parâmetro (≤ 15%)"
    )
    tabela_div_show["divergencia_pct"] = tabela_div_show["divergencia_pct"].map("{:.2f}%".format)
    tabela_div_show.columns = ["ID", "Produto", "Estoque Registrado", "Estoque Calculado", "Divergência (%)", "Status Gerencial"]
    st.dataframe(tabela_div_show, width="stretch", hide_index=True)

    st.markdown("---")

    # SEÇÃO 2: ANÁLISE INDICATIVA DE INFORMAÇÕES FISCAIS (ICMS)
    st.markdown("#### 2. Análise Indicativa de Informações Fiscais (ICMS)")

    # Agrupamentos de ICMS de Compras (Entradas)
    icms_compras = compras_fil.groupby(["cfop", "icms_rate"]).agg(
        notas=("purchase_id", "nunique"),
        base_calculo=("icms_base", "sum"),
        icms_destacado=("icms_amount", "sum"),
    ).reset_index()

    # Agrupamentos de ICMS de Vendas (Saídas)
    icms_vendas = vendas_fil.groupby(["cfop", "icms_rate"]).agg(
        cupons=("sale_id", "count"),
        faturamento=("total_amount", "sum"),
        icms_destacado=("icms_amount", "sum"),
    ).reset_index()

    col_icms1, col_icms2 = st.columns(2)

    with col_icms1:
        st.markdown("##### 📥 Documentos Fiscais de Entrada (Compras / NF-e)")
        st.markdown(
            f"""
            <div style="background:#131d2e; border:1px solid #24334a; border-radius:10px; padding:12px; margin-bottom:10px;">
              Total de ICMS Destacado na Entrada: <b style="color:#60a5fa;">{fmt_brl(compras_fil['icms_amount'].sum())}</b><br>
              <span style="font-size:0.75rem; color:#94a3b8;">CFOP 1102 (Compra para Comercialização)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        icms_comp_tab = icms_compras.copy()
        icms_comp_tab["icms_rate"] = icms_comp_tab["icms_rate"].apply(lambda r: f"{r*100:.0f}%")
        icms_comp_tab["base_calculo"] = icms_comp_tab["base_calculo"].map("R$ {:,.2f}".format)
        icms_comp_tab["icms_destacado"] = icms_comp_tab["icms_destacado"].map("R$ {:,.2f}".format)
        icms_comp_tab.columns = ["CFOP", "Alíquota", "Qtd Notas", "Base de Cálculo", "ICMS Destacado"]
        st.dataframe(icms_comp_tab, width="stretch", hide_index=True)

    with col_icms2:
        st.markdown("##### 📤 Documentos Fiscais de Saída (Vendas / NFC-e)")
        st.markdown(
            f"""
            <div style="background:#131d2e; border:1px solid #24334a; border-radius:10px; padding:12px; margin-bottom:10px;">
              Total de ICMS Indicativo nas Vendas: <b style="color:#34d399;">{fmt_brl(vendas_fil['icms_amount'].sum())}</b><br>
              <span style="font-size:0.75rem; color:#94a3b8;">CFOP 5102 (Venda de Mercadoria Adquirida de Terceiros)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        icms_vend_tab = icms_vendas.copy()
        icms_vend_tab["icms_rate"] = icms_vend_tab["icms_rate"].apply(lambda r: f"{r*100:.0f}%")
        icms_vend_tab["faturamento"] = icms_vend_tab["faturamento"].map("R$ {:,.2f}".format)
        icms_vend_tab["icms_destacado"] = icms_vend_tab["icms_destacado"].map("R$ {:,.2f}".format)
        icms_vend_tab.columns = ["CFOP", "Alíquota", "Cupons", "Valor Total Vendas", "ICMS Destacado"]
        st.dataframe(icms_vend_tab, width="stretch", hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 10: DETALHAMENTO & GOVERNANÇA (Tabelas Filtráveis e Auditoria ETL)
# ═════════════════════════════════════════════════════════════════════════════
with tab_detalhes:
    st.markdown('<div class="section-title">📋 Detalhamento Geral dos Dados & Auditoria de Engenharia</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 16px;">
          Navegue pelas tabelas consolidadas do sistema, aplique buscas e exporte os dados tratados para auditoria.
        </div>
        """,
        unsafe_allow_html=True,
    )

    visao_escolhida = st.radio(
        "Selecione o Conjunto de Dados:",
        options=[
            "Transações de Vendas",
            "Notas de Compras",
            "Inventário de Estoque",
            "Lotes e Validade",
            "Baixas de Perdas",
            "Fornecedores Homologados",
            "🛡️ Log de Auditoria do ETL",
        ],
        horizontal=True,
    )

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    if visao_escolhida == "Transações de Vendas":
        st.markdown(f"**Vendas Registradas ({len(vendas_fil):,} transações):**")
        vendas_view = vendas_fil[[
            "sale_id", "date_time", "pos_id", "product_name", "category",
            "quantity", "unit_price", "total_amount", "payment_method", "cfop"
        ]].copy().sort_values("date_time", ascending=False)
        st.dataframe(vendas_view.head(2000), width="stretch", hide_index=True)
        st.download_button(
            "📥 Baixar Vendas Filtradas (CSV)",
            data=vendas_view.to_csv(index=False).encode("utf-8"),
            file_name="vendas_filtradas.csv",
            mime="text/csv",
        )

    elif visao_escolhida == "Notas de Compras":
        st.markdown(f"**Compras e Entradas ({len(compras_fil):,} itens de pedidos):**")
        compras_view = compras_fil[[
            "purchase_id", "nfe_number", "purchase_date", "trade_name", "product_name",
            "category", "quantity", "unit_cost", "total_cost", "cfop", "icms_rate", "icms_amount"
        ]].copy().sort_values("purchase_date", ascending=False)
        st.dataframe(compras_view, width="stretch", hide_index=True)
        st.download_button(
            "📥 Baixar Compras Filtradas (CSV)",
            data=compras_view.to_csv(index=False).encode("utf-8"),
            file_name="compras_filtradas.csv",
            mime="text/csv",
        )

    elif visao_escolhida == "Inventário de Estoque":
        st.markdown(f"**Posições Físicas de Estoque ({len(estoque_fil):,} registros):**")
        estoque_view = estoque_fil[[
            "product_id", "product_name", "category", "storage_location",
            "current_quantity", "reserved_quantity", "min_stock", "ideal_stock", "sale_price"
        ]].copy()
        st.dataframe(estoque_view, width="stretch", hide_index=True)
        st.download_button(
            "📥 Baixar Estoque Filtrado (CSV)",
            data=estoque_view.to_csv(index=False).encode("utf-8"),
            file_name="estoque_filtrado.csv",
            mime="text/csv",
        )

    elif visao_escolhida == "Lotes e Validade":
        st.markdown(f"**Lotes de Perecíveis ({len(validade_raw):,} lotes):**")
        val_view = validade_raw.merge(produtos[["product_id", "product_name", "category"]], on="product_id", how="left")
        st.dataframe(val_view, width="stretch", hide_index=True)
        st.download_button(
            "📥 Baixar Validades (CSV)",
            data=val_view.to_csv(index=False).encode("utf-8"),
            file_name="validade.csv",
            mime="text/csv",
        )

    elif visao_escolhida == "Baixas de Perdas":
        st.markdown(f"**Histórico de Perdas Operacionais ({len(perdas_fil):,} registros):**")
        perdas_view = perdas_fil[[
            "loss_id", "date", "product_name", "category", "quantity",
            "loss_reason", "unit_cost_at_loss", "total_loss_value"
        ]].copy().sort_values("date", ascending=False)
        st.dataframe(perdas_view, width="stretch", hide_index=True)
        st.download_button(
            "📥 Baixar Perdas Filtradas (CSV)",
            data=perdas_view.to_csv(index=False).encode("utf-8"),
            file_name="perdas_filtradas.csv",
            mime="text/csv",
        )

    elif visao_escolhida == "Fornecedores Homologados":
        st.markdown(f"**Fornecedores Cadastrados ({len(fornecedores):,} parceiros):**")
        st.dataframe(fornecedores, width="stretch", hide_index=True)
        st.download_button(
            "📥 Baixar Fornecedores (CSV)",
            data=fornecedores.to_csv(index=False).encode("utf-8"),
            file_name="fornecedores.csv",
            mime="text/csv",
        )

    elif visao_escolhida == "🛡️ Log de Auditoria do ETL":
        st.markdown(
            """
            <div class="alert-box alert-green">
              <b>GOVERNANÇA E QUALIDADE DE DADOS:</b><br>
              A tabela abaixo comprova a aplicação rigorosa das regras de higienização de dados na camada de engenharia (pipeline <code>etl_pipeline.py</code>), assegurando que inconsistências operacionais fossem tratadas ou isoladas em quarentena sem adulterar os arquivos brutos.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(auditoria, width="stretch", hide_index=True)
        st.download_button(
            "📥 Baixar Log de Auditoria ETL (CSV)",
            data=auditoria.to_csv(index=False).encode("utf-8"),
            file_name="auditoria_etl.csv",
            mime="text/csv",
        )

# ─────────────────────────────────────────────────────────────────────────────
# 9. RODAPÉ INSTITUCIONAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <hr style="border-color: #1e293b; margin-top: 48px;">
    <div style="text-align: center; color: #64748b; font-size: 0.78rem; padding-bottom: 28px; line-height: 1.6;">
      <b>SUPERMERCADO BI</b> — Camada de Business Intelligence & Automação Gerencial<br>
      Empresa de Referência: <em>Supermercado Alvorada Ltda.</em> | Slogan: <em>"Dados organizados. Decisões inteligentes."</em><br>
      Projeto Acadêmico Integrado | Desenvolvido com Python 3.12, SQLite, Pandas, Streamlit e Plotly.
    </div>
    """,
    unsafe_allow_html=True,
)
