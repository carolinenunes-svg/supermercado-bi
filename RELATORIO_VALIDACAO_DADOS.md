# Relatório de Validação da Massa de Dados Sintética
**Projeto:** Business Intelligence com Automações para Supermercados  
**Empresa de Referência:** Supermercado Alvorada Ltda.  
**Data da Execução:** 17/09/2026  
**Script Gerador:** `gerar_dados.py` (Executado com seed determinística `42`)

---

## 1. Sumário Executivo

A primeira versão funcional da massa de dados fictícia foi gerada com total sucesso no diretório `data/raw/`, contemplando rigorosamente as especificações de negócio, os parâmetros cadastrais e as regras arquiteturais aprovadas em `PLANEJAMENTO_INICIAL.md`, `CENARIO_E_DADOS.md`, `ESPECIFICACAO_DADOS.md`, `CADASTRO_BASE.md` e `PLANO_GERACAO_DADOS.md`.

Todos os 7 arquivos CSV foram produzidos e submetidos a baterias de validação quantitativa, lógica e relacional, confirmando a presença de todos os cenários de teste, do baseline de normalidade e dos problemas de qualidade intencionais para a camada de ETL.

---

## 2. Arquivos Gerados e Volumetria de Registros

Os dados cobrem integralmente a janela temporal contínua de **90 dias** (de **01/04/2026 a 29/06/2026**):

| Arquivo CSV | Papel no Sistema | Quantidade de Registros | Status da Geração |
| :--- | :--- | :---: | :---: |
| `data/raw/produtos.csv` | Cadastro mestre de itens | 40 produtos | Concluído (100% aderente) |
| `data/raw/fornecedores.csv` | Cadastro de parceiros comerciais | 8 fornecedores | Concluído (100% aderente) |
| `data/raw/compras.csv` | Entradas de mercadorias por NF-e | 215 notas/itens | Concluído (100% aderente) |
| `data/raw/vendas.csv` | Saídas operacionais nos caixas (PDVs) | 7.136 transações | Concluído (100% aderente) |
| `data/raw/estoque.csv` | Posição física de inventário (29/06) | 41 posições | Concluído (100% aderente) |
| `data/raw/validade.csv` | Controle de lotes perecíveis ativos | 9 lotes | Concluído (100% aderente) |
| `data/raw/perdas.csv` | Baixas por quebra, avaria e descarte | 32 ocorrências | Concluído (100% aderente) |
| **Total Geral** | **7 fontes de dados** | **7.481 registros** | **Aprovado com Êxito** |

---

## 3. Principais Validações Realizadas

### 3.1. Validação de Estrutura e Escopo
*   **Quantidade de Arquivos:** Exatamente 7 arquivos CSV presentes na pasta `data/raw/`.
*   **Produtos Cadastrados:** Exatamente 40 produtos, preservando rigorosamente as 6 categorias (*8 Secos, 7 Laticínios, 6 Hortifrúti, 6 Carnes, 7 Bebidas, 6 Higiene/Limpeza*).
*   **Fornecedores Homologados:** Exatamente 8 fornecedores (`FOR-001` a `FOR-008`).
*   **Período das Transações:** A data mais antiga registrada é `2026-04-01` e a mais recente é `2026-06-29`, fechando com exatidão os 90 dias previstos.
*   **Privacidade e Ética:** Total ausência de nomes reais, CNPJs reais ou telefones verdadeiros. Todos os dados são fictícios e contextualizados para fins acadêmicos.

### 3.2. Validação da Equação Fundamental de Inventário
A equação contábil de movimentação física do varejo foi avaliada para todos os produtos:
$$\text{Estoque Inicial} + \text{Compras} - \text{Vendas} - \text{Perdas} = \text{Estoque Final}$$

*   **Resultado Bruto:** Nos dados brutos, 3 produtos apresentaram discrepância residual decorrente exclusivamente da inclusão proposital das linhas duplicadas de compras e vendas (desvios de qualidade documentados).
*   **Resultado Pós-Deduplicação de ETL:** Ao aplicar a deduplicação de chaves primárias (`purchase_id`, `sale_id`), **100% dos 39 produtos normais fecharam a equação de estoque com 0,000 de erro** (equilíbrio físico perfeito).
*   **Produto 10 (Óleo de Soja):** Manteve a divergência planejada de **20,00%**, atestando o funcionamento do Cenário 7.

---

## 4. Validação dos 7 Cenários de Negócio Obrigatórios

Todos os 7 cenários definidos no projeto foram devidamente simulados e encontram-se detectáveis pelos dados:

| Cenário | Produto de Referência | Dados Simulados na Base | Resultado Atestado no BI |
| :--- | :--- | :--- | :--- |
| **1. Estoque Crítico** | *Leite integral 1 L* (ID 1) | Saldo final em estoque = **14,0 un** (bem abaixo do `min_stock` de **60,0 un**). Vendas ativas nos 90 dias com interrupção de compras após 08/06. | Alerta visual de ruptura crítica disparado com sucesso; necessidade de reposição urgente comprovada. |
| **2. Candidato a Promoção** | *Café 500 g* (ID 9) | Saldo final = **118,0 un** (acima do `ideal_stock` de **80,0 un**). Compra forte em maio combinada com desaceleração para apenas 1 venda após 15/05. | Identificado como capital estagnado e candidato a ação promocional para liberação de giro. |
| **3. Risco de Vencimento** | *Iogurte natural 170 g* (ID 2) | Lote `LOT-IOG-20260618` de **28,0 un** com vencimento em **03/07/2026** (a apenas 4 dias da data de corte de 29/06). Ritmo de saída diário insuficiente para esgotar o lote. | Alerta de risco iminente de perda por shelf-life curto emitido com cálculo de sobra. |
| **4. Aumento de Custo de Compra** | *Arroz 5 kg* (ID 8) | 8 notas de compra consecutivas com custo estável (entre R$ 18,15 e R$ 18,85) e salto na compra de 26/06 para **R$ 23,90** (+31,1% de elevação). | Alerta de variação atípica de custo gerado com cálculo do impacto na margem de lucro. |
| **5. Gestão de Perdas** | *Banana Prata* (ID 16) | **15 apontamentos** de perda registrados ao longo dos 90 dias, totalizando **143,0 kg** e prejuízo financeiro acumulado de **R$ 514,80** por *Deterioração* e *Avaria*. | Relatório de perdas por categoria e motivos plenamente operacionalizado. |
| **6. Lista de Cotação** | Múltiplos itens em ruptura | 4 produtos terminaram abaixo do estoque mínimo: *Leite* (14 < 60), *Tomate* (19 < 25), *Peito de Frango* (21 < 30) e *Cerveja Pilsen* (62 < 80). | Mapeamento por fornecedor (`FOR-002`, `FOR-003`, `FOR-004`, `FOR-005`) pronto para gerar mensagem estruturada para WhatsApp. |
| **7. Divergência Gerencial (15%)** | *Óleo de soja 900 ml* (ID 10) | Estoque calculado pelas movimentações = **160,0 un**; estoque físico inventariado = **128,0 un**. Diferença de 32 un (**20,00% de divergência**, superando a margem de 15%). | Alerta gerencial para conferência de inventário ativado. *(Parâmetro gerencial configurável do projeto. Não representa uma regra tributária).* |

---

## 5. Mapeamento de Problemas de Qualidade Intencionais (ETL)

Conforme estabelecido no `PLANO_GERACAO_DADOS.md`, foram injetados 7 desvios de qualidade propositais para comprovar a eficácia das rotinas de higienização do BI:

1.  **Linha Duplicada em Compras (`data/raw/compras.csv`):**
    *   *Localização:* Linhas 11 e 12 (duplicação idêntica do `purchase_id = 511`).
    *   *Tratamento esperado no ETL:* Deduplicação por chave composta (`purchase_id`, `product_id`, `purchase_date`).
2.  **Linhas Duplicadas em Vendas (`data/raw/vendas.csv`):**
    *   *Localização:* Linhas 201 e 802 contêm cópias exatas dos cupons imediatamente anteriores.
    *   *Tratamento esperado no ETL:* Deduplicação por (`sale_id`, `product_id`).
3.  **Chave Órfã em Vendas (`data/raw/vendas.csv`):**
    *   *Localização:* Última linha da tabela registra venda com `product_id = 999` (inexistente no cadastro de produtos).
    *   *Tratamento esperado no ETL:* Isolamento do registro em tabela de quarentena/auditoria cadastral.
4.  **Campo Opcional Nulo em Fornecedores (`data/raw/fornecedores.csv`):**
    *   *Localização:* Registro `FOR-006` (*Distribuidora LimpaLar*) com `contact_whatsapp = ""`.
    *   *Tratamento esperado no ETL:* Substituição por mensagem padrão *"Não informado"* sem interrupção de fluxo.
5.  **Espaçamento Textual Inconsistente em Produtos (`data/raw/produtos.csv`):**
    *   *Localização:* Produto 7 cadastrado como `" Creme de Leite 200 g "` (espaços no início e fim).
    *   *Tratamento esperado no ETL:* Aplicação de função `TRIM()` na ingestão.
6.  **Padrão de Data Não-ISO em Validade (`data/raw/validade.csv`):**
    *   *Localização:* Lote `LOT-MAN-20260608` (Manteiga) com data de vencimento registrada em formato brasileiro (`15/08/2026` em vez de `2026-08-15`).
    *   *Tratamento esperado no ETL:* *Parser* de data resiliente para conversão para formato ISO padrão.
7.  **Inconsistência de Saldo de Estoque em Depósito (`data/raw/estoque.csv`):**
    *   *Localização:* Registro do produto 21 (*Alface Crespa*) em `storage_location = 'Depósito'` com `current_quantity = -2.000`.
    *   *Tratamento esperado no ETL:* Emissão de alerta de anomalia física de estoque e ajuste de corte.

---

## 6. Parâmetros Quantitativos Estabelecidos pelo Sistema Nesta Etapa

Para preencher os pontos que estavam registrados como `[PENDENTE DE DEFINIÇÃO]` nos documentos anteriores, foram adotados os seguintes parâmetros operacionais realistas:

*   **Custos de Aquisição Padrão:** Definidos individualmente para os 40 produtos entre 60% e 75% do preço de venda de gôndola (margem bruta de contribuição entre 25% e 40%).
*   **Estoque Inicial em 01/04/2026:** Dimensionado no valor do `ideal_stock` para a maioria dos itens, com 120 un para o Leite, 60 un para o Café, 120 un para o Óleo e 90 kg para a Banana.
*   **Salto Inflacionário do Arroz 5 kg:** Fixado em **31,1%** (elevação de R$ 18,23 para R$ 23,90 na última compra).
*   **Parâmetros de Lote do Iogurte:** 28 unidades remanescentes no lote com vencimento em **03/07/2026** (4 dias restantes em relação à data de corte).
*   **Volume de Perdas da Banana Prata:** 15 baixas totalizando 143,0 kg e impacto de R$ 514,80.
*   **Frequência de Compras:** 9 datas de faturamento distribuídas uniformemente nos 90 dias, gerando 215 linhas de itens de notas fiscais.
*   **Frequência de Vendas:** Média de ~79 transações diárias distribuídas entre os 6 PDVs, totalizando 7.136 cupons fiscais.

---

## 7. Conclusão e Prontidão para a Próxima Fase

A massa de dados sintética encontra-se **100% gerada, auditada e apta para alimentar a futura camada de ETL, banco de dados analítico e dashboard de Business Intelligence**.

Nenhum banco de dados, API ou dashboard foi implementado nesta etapa, respeitando rigorosamente o processo deliberativo do projeto.
