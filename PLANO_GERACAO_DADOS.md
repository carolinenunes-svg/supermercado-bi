# Plano de Geração de Dados Fictícios

---

## 1. Estratégia de Geração

A geração da massa de dados fictícia para o **Supermercado Alvorada Ltda.** tem por finalidade construir um ecossistema de dados sintéticos consistente, controlado e matematicamente plausível, cobrindo o período de 90 dias compreendido entre **01/04/2026 e 29/06/2026**.

Para evitar discrepâncias numéricas que invalidem os cálculos de Business Intelligence, a geração seguirá o princípio contábil e físico da equação fundamental de inventário do varejo:

$$\text{Estoque Inicial} + \text{Compras (Entradas)} - \text{Vendas (Saídas)} - \text{Perdas (Baixas)} = \text{Estoque Final (Foto)}$$

### Princípios Norteadores:
*   **Controle Temporal e Sazonalidade:** As vendas serão distribuídas respeitando o padrão operacional do comércio (maior fluxo de clientes de quinta a sábado, picos nos primeiros dez dias do mês e horários de pico entre 11h-13h e 17h-20h).
*   **Compras Periódicas:** As reposições em `compras.csv` ocorrerão de forma escalonada ao longo dos 90 dias, simulando ciclos de pedidos coerentes com o *lead time* dos fornecedores e com a perecibilidade de cada categoria.
*   **Integridade Referencial Estrita:** Nenhuma transação será gerada sem vínculo a um produto oficial (IDs 1 a 40) ou a um fornecedor homologado (`FOR-001` a `FOR-008`).
*   **Isolamento Controlado dos Cenários de Teste:** Os cenários de exceção serão programados de forma cirúrgica na linha do tempo, garantindo que o BI consiga isolar cada problema sem poluir o comportamento padrão do restante do supermercado.

---

## 2. Dependências entre os Arquivos

A geração dos dados deverá seguir uma ordem cronológica e relacional estrita, onde cada camada depende da validação prévia da anterior:

```
[Etapa 1: Cadastros Mestres]
   produtos.csv + fornecedores.csv
          |
          v
[Etapa 2: Movimentações Temporais (01/04 a 29/06)]
   compras.csv (Entradas / NF-e)
   vendas.csv  (Saídas / PDVs)
   perdas.csv  (Baixas operacionais)
          |
          v
[Etapa 3: Posição de Inventário e Validades (Corte em 29/06)]
   estoque.csv  (Saldo consolidado pós-movimentações)
   validade.csv (Lotes ativos derivados das últimas compras)
```

### Ordem Lógica de Execução:
1.  **Etapa 1 — `produtos.csv` e `fornecedores.csv` (Dimensões Primárias):**
    *   Representam as tabelas dimensionais estáticas definidas em `CADASTRO_BASE.md`. Fornecem as chaves primárias (`product_id` e `supplier_id`) e os parâmetros de apoio (`min_stock`, `ideal_stock`, `sale_price`, `lead_time_days`).
2.  **Etapa 2 — `compras.csv` (Histórico de Entradas):**
    *   Gera as notas fiscais de reposição dos produtos, respeitando a Matriz Produto × Fornecedor. Define os custos históricos de aquisição (`unit_cost`) e o ICMS de entrada.
3.  **Etapa 3 — `vendas.csv` (Histórico de Saídas):**
    *   Simula o registro de cupons fiscais nos 6 caixas (PDV 1 a 6) ao longo dos 90 dias, consumindo os produtos com base na velocidade média esperada para cada categoria.
4.  **Etapa 4 — `perdas.csv` (Histórico de Baixas Operacionais):**
    *   Registra os eventos de descarte, quebra e avaria ocorridos pontualmente durante o trimestre, abatendo os saldos físicos.
5.  **Etapa 5 — `estoque.csv` (Snapshot de Posição Física em 29/06/2026):**
    *   Calcula o saldo remanescente em prateleira e depósito após o confronto exato entre entradas, saídas e perdas.
6.  **Etapa 6 — `validade.csv` (Lotes Perecíveis Ativos):**
    *   Derivado das últimas entradas de compras de itens perecíveis (Laticínios, Carnes e Hortifrúti), registrando os lotes que permanecem em estoque na data de corte e suas respectivas datas de vencimento.

---

## 3. Estratégia para os 7 Cenários de Negócio

Para que o futuro sistema de BI emita alertas e monte os relatórios planejados, a massa de dados conterá as condições operacionais estruturadas abaixo:

### 3.1. Cenário 1 — Estoque Crítico (Leite integral 1 L - ID 1)
*   **Arquivos Envolvidos:** `produtos.csv`, `vendas.csv`, `estoque.csv`, `fornecedores.csv`.
*   **Campos Principais:** `produtos.min_stock` (60), `produtos.ideal_stock` (180), `estoque.current_quantity`, `vendas.quantity`, `fornecedores.lead_time_days`.
*   **Comportamento dos Dados:** O produto apresentará vendas consistentes e diárias em volume expressivo. Nas últimas duas semanas de junho, as compras de reposição cessarão intencionalmente, fazendo com que o saldo final em `estoque.csv` resulte em um valor bem abaixo do `min_stock` (ex.: ~15 unidades).
*   **Resultado Esperado no BI:** Disparo de alerta visual imediato de "Risco Crítico de Ruptura" e cálculo da necessidade urgente de pedido de reposição.

### 3.2. Cenário 2 — Candidato a Promoção (Café 500 g - ID 9)
*   **Arquivos Envolvidos:** `produtos.csv`, `compras.csv`, `vendas.csv`, `estoque.csv`.
*   **Campos Principais:** `produtos.ideal_stock` (80), `estoque.current_quantity`, `vendas.quantity`, `vendas.date_time`.
*   **Comportamento dos Dados:** No primeiro mês, o produto terá vendas regulares. A partir de maio, a demanda de vendas cairá consideravelmente (desaceleração de giro), porém uma compra de grande volume terá sido recebida anteriormente, resultando em um saldo em `estoque.csv` bastante superior a 80 unidades, com cobertura para dezenas de dias.
*   **Resultado Esperado no BI:** Identificação do item como "Candidato a Ação Promocional / Queima de Estoque" para liberação de capital de giro estagnado.

### 3.3. Cenário 3 — Risco de Vencimento (Iogurte natural 170 g - ID 2)
*   **Arquivos Envolvidos:** `produtos.csv`, `validade.csv`, `vendas.csv`, `estoque.csv`.
*   **Campos Principais:** `validade.expiration_date`, `validade.batch_quantity`, `vendas.quantity`, `estoque.current_quantity`.
*   **Comportamento dos Dados:** A tabela `validade.csv` registrará um lote recebido no início de junho cuja data de expiração estará a poucos dias da data de corte (fim de junho / início de julho). A taxa diária de saída em `vendas.csv` projetará um consumo insuficiente para liquidar o lote antes do prazo.
*   **Resultado Esperado no BI:** Emissão de "Alerta de Atenção: Lote Próximo ao Vencimento" com cálculo do volume projetado de perda.

### 3.4. Cenário 4 — Aumento de Custo de Compra (Arroz 5 kg - ID 8)
*   **Arquivos Envolvidos:** `produtos.csv`, `compras.csv`, `fornecedores.csv`.
*   **Campos Principais:** `compras.purchase_date`, `compras.unit_cost`, `compras.supplier_id`, `produtos.sale_price` (R$ 26,90).
*   **Comportamento dos Dados:** Em abril e maio, as compras de Arroz junto aos fornecedores (`FOR-001` ou `FOR-007`) registrarão custos de aquisição homogêneos. Na última nota de entrada, emitida em meados de junho, o `unit_cost` sofrerá uma elevação atípica e expressiva.
*   **Resultado Esperado no BI:** Geração de alerta de "Variação Relevante de Preço de Entrada", indicando a inflação do item e a compressão da margem bruta de comercialização.

### 3.5. Cenário 5 — Gestão e Registro de Perdas (Banana Prata - ID 16)
*   **Arquivos Envolvidos:** `produtos.csv`, `perdas.csv`.
*   **Campos Principais:** `perdas.loss_date`, `perdas.quantity`, `perdas.loss_reason`, `perdas.unit_cost_at_loss`, `perdas.total_loss_value`.
*   **Comportamento dos Dados:** Ao longo dos 90 dias, a tabela `perdas.csv` conterá lançamentos recorrentes de baixas da Banana Prata, especificando motivos típicos como *Deterioração* e *Avaria*.
*   **Resultado Esperado no BI:** Demonstração no painel de perdas com o ranking financeiro de descartes da categoria Hortifrúti e a proporção de perdas sobre as compras.

### 3.6. Cenário 6 — Geração de Lista de Cotação (Múltiplos Itens)
*   **Arquivos Envolvidos:** `produtos.csv`, `estoque.csv`, `fornecedores.csv`.
*   **Campos Principais:** `produtos.product_id`, `produtos.product_name`, `produtos.ideal_stock`, `estoque.current_quantity`, `fornecedores.contact_whatsapp`, `fornecedores.trade_name`.
*   **Comportamento dos Dados:** Além do Leite integral, outros 2 ou 3 produtos de alto giro terminarão o período com saldo inferior ao `min_stock`.
*   **Resultado Esperado no BI:** Agrupamento automatizado das necessidades de reposição por `supplier_id` e formatação de um bloco textual estruturado pronto para cópia e envio manual pelo WhatsApp aos representantes.

### 3.7. Cenário 7 — Divergência Gerencial de 15% (Óleo de soja 900 ml - ID 10)
*   **Arquivos Envolvidos:** `compras.csv`, `vendas.csv`, `estoque.csv`.
*   **Campos Principais:** Soma de `compras.quantity`, soma de `vendas.quantity`, `estoque.current_quantity`.
*   **Comportamento dos Dados:** A relação volumétrica calculada entre o total adquirido e o total faturado (ponderado pela variação de inventário) resultará intencionalmente em uma diferença superior a 15%.
*   **Resultado Esperado no BI:** Emissão de "Alerta Gerencial de Divergência Compra x Venda" para orientação de auditoria de loja.
*   **Ressalva Formal Mandatória:** *15% é um parâmetro gerencial configurável do projeto e não representa uma regra tributária.*

---

## 4. Comportamento dos Demais Produtos (Linha de Base Normal)

Para assegurar o realismo do modelo e evitar um painel poluído por alertas generalizados e artificiais, os outros **33 produtos** apresentarão comportamento operacional equilibrado:

1.  **Produtos de Alto Giro e Alta Estabilidade:**
    *   *Exemplos:* Cerveja Pilsen 350 ml (ID 33), Refrigerante Cola 2 L (ID 28), Pão/Farinha de Trigo (ID 14).
    *   *Comportamento:* Vendas diárias robustas, entradas de compras regulares a cada 7 ou 10 dias, custos de aquisição sem oscilações abruptas e saldos de estoque sempre oscilando confortavelmente entre `min_stock` e `ideal_stock`.
2.  **Produtos de Giro Médio:**
    *   *Exemplos:* Detergente Líquido (ID 35), Sabão em Pó (ID 36), Feijão Preto (ID 11), Frango Resfriado (ID 24).
    *   *Comportamento:* Ciclo de compras quinzenal, vendas previsíveis sem rupturas e margens financeiras estáveis.
3.  **Produtos de Baixo Giro / Compra Esporádica:**
    *   *Exemplos:* Sal Refinado (ID 15), Amaciante de Roupas (ID 37), Suco de Uva Integral (ID 30).
    *   *Comportamento:* Saídas em menor volume diário, porém com estoque enxuto e dimensionado, não caracterizando estoque parado nem risco financeiro.
4.  **Flutuações Naturais de Mercado:**
    *   Pequenas oscilações rotineiras de preços de compra (entre -2% e +3%), que refletem a dinâmica comum do varejo sem atingir a régua de alerta de inflação de custo.
5.  **Perdas Operacionais Residuais:**
    *   Lançamentos pontuais de quebra ou avaria em outros itens perecíveis (ex.: Tomate ou Queijo), demonstrando que a perda é uma realidade sistêmica, mas sem a concentração crítica da Banana.

---

## 5. Qualidade dos Dados (Simulação de Desvios para Tratamento de ETL)

Em conformidade com a `ESPECIFICACAO_DADOS.md`, a massa de dados conterá intencionalmente problemas de qualidade controlados para comprovar a capacidade do processo de ETL de higienizar a informação antes de alimentar o BI:

| Tipo de Problema | Arquivo Afetado | Detalhe do Desvio Simulado | Ação Esperada na Camada de ETL |
| :--- | :--- | :--- | :--- |
| **Linha Duplicada** | `vendas.csv` | Mesma transação de venda repetida com os mesmos identificadores | Deduplicação baseada na chave composta |
| **Linha Duplicada** | `compras.csv` | Duplicação acidental de linha de item de nota fiscal | Identificação e descarte da duplicidade |
| **Campo Nulo Opcional** | `fornecedores.csv` | Fornecedor sem número de WhatsApp cadastrado | Tratamento de ausência sem falha na cotação |
| **Espaçamento / Caixa** | `produtos.csv` | Nome ou categoria com espaços extras ou caixa mista | Padronização textual (`TRIM`, `UPPER/LOWER`) |
| **Formato de Data** | `validade.csv` | Lançamento isolado com data em formato diferente (ex.: BR `DD/MM/YYYY`) | Conversão e padronização para ISO (`YYYY-MM-DD`) |
| **Chave Órfã Controlada** | `vendas.csv` | Registro de venda com código de produto inexistente (`product_id = 999`) | Isolamento em tabela de log/auditoria |
| **Inconsistência de Saldo** | `estoque.csv` | Registro de item com saldo temporariamente negativo antes da conciliação | Sinalização de inconsistência física de estoque |

> **Nota Técnica:** Todos os desvios de qualidade são planejados e documentados. O processo de ETL deverá tratá-los de forma elegante, garantindo que a base analítica final permaneça 100% íntegra.

---

## 6. Regras de Consistência Pós-Geração

Após a futura geração da massa de dados sintética, as seguintes regras lógicas deverão ser atendidas de forma rigorosa:

1.  **Integridade Chave-Estrangeira:** Todo `product_id` presente em `vendas.csv`, `compras.csv`, `estoque.csv`, `validade.csv` e `perdas.csv` deve existir em `produtos.csv` (com exceção da chave órfã proposital de teste).
2.  **Aderência à Matriz de Fornecimento:** Toda compra em `compras.csv` deve relacionar um produto a um fornecedor que esteja formalmente homologado na Matriz Produto × Fornecedor de `CADASTRO_BASE.md`.
3.  **Janela Temporal Fechada:** Toda data de transação em `compras`, `vendas`, `perdas` e `validade` deve estar contida rigorosamente entre **01/04/2026 e 29/06/2026**.
4.  **Consistência Aritmética de Linha:**
    *   `vendas.total_amount` = `quantity * unit_price`
    *   `compras.total_cost` = `quantity * unit_cost`
    *   `perdas.total_loss_value` = `quantity * unit_cost_at_loss`
5.  **Coerência de Lotes:** Nenhum lote em `validade.csv` poderá possuir `expiration_date` anterior à data de entrada `entry_date`.
6.  **Equilíbrio Físico:** O saldo em `estoque.csv` para cada um dos 40 itens deve guardar relação direta e coerente com o somatório de compras menos vendas e perdas do trimestre.
7.  **Valores Válidos:** Inexistência de preços negativos, alíquotas de ICMS fora dos padrões ou quantidades absurdas não planejadas.

---

## 7. Checklist de Validações Pós-Geração

Esta checklist servirá como guia formal de conferência imediata assim que os arquivos forem sintetizados:

- [ ] **1. Quantidade de Arquivos:** Exatamente 7 arquivos CSV gerados (`produtos.csv`, `fornecedores.csv`, `vendas.csv`, `compras.csv`, `estoque.csv`, `validade.csv`, `perdas.csv`).
- [ ] **2. Período:** Registros cronológicos contidos estritamente entre 01/04/2026 e 29/06/2026.
- [ ] **3. Catálogo de Produtos:** Exatamente 40 produtos cadastrados, distribuídos nas 6 categorias oficiais (*8 Secos, 7 Laticínios, 6 Hortifrúti, 6 Carnes, 7 Bebidas, 6 Higiene/Limpeza*).
- [ ] **4. Cadastro de Fornecedores:** Exatamente 8 fornecedores cadastrados (`FOR-001` a `FOR-008`).
- [ ] **5. Mapeamento de Fornecimento:** 100% dos 40 produtos possuem vínculo homologado com fornecedores.
- [ ] **6. Cenário 1 (Leite integral 1 L):** Saldo em estoque abaixo de 60 unidades com vendas ativas comprovadas.
- [ ] **7. Cenário 2 (Café 500 g):** Saldo em estoque elevado com desaceleração de saídas nas últimas semanas.
- [ ] **8. Cenário 3 (Iogurte natural 170 g):** Lote em `validade.csv` com expiração próxima e giro insuficiente.
- [ ] **9. Cenário 4 (Arroz 5 kg):** Compras demonstrando salto atípico no `unit_cost` na nota mais recente.
- [ ] **10. Cenário 5 (Banana Prata):** Registros expressivos em `perdas.csv` discriminados por motivo.
- [ ] **11. Cenário 6 (Lista de Cotação):** Presença de itens em ruptura com dados completos para montagem de mensagem de WhatsApp.
- [ ] **12. Cenário 7 (Óleo de soja 900 ml):** Disparidade entre entradas e saídas superior a 15% (*regra gerencial*).
- [ ] **13. Baseline de Normalidade:** Cerca de 33 produtos com fluxo estável sem geração de alertas indevidos.
- [ ] **14. Qualidade de Dados:** Presença documentada dos 7 desvios controlados para validação do ETL.
- [ ] **15. Conformidade Ética e Legal:** Total ausência de nomes reais, CPFs, CNPJs reais ou telefones verídicos.

---

## 8. Pontos que Permanecem Pendentes

Permanecem registrados como **[PENDENTE DE DEFINIÇÃO]** os seguintes parâmetros quantitativos e operacionais, cuja definição exata deverá ser deliberada antes da execução do gerador:

*   **[PENDENTE DE DEFINIÇÃO]** Custo de aquisição inicial padrão para cada um dos 40 produtos.
*   **[PENDENTE DE DEFINIÇÃO]** Volume volumétrico exato de transações de venda esperadas no total dos 90 dias (ex.: 5.000, 10.000 ou 15.000 linhas em `vendas.csv`).
*   **[PENDENTE DE DEFINIÇÃO]** Frequência exata das notas fiscais de entrada em `compras.csv` por fornecedor.
*   **[PENDENTE DE DEFINIÇÃO]** Percentual exato de aumento de custo no Arroz 5 kg na compra de fechamento.
*   **[PENDENTE DE DEFINIÇÃO]** Número exato do lote, data de vencimento e volume remanescente do Iogurte natural em `validade.csv`.
*   **[PENDENTE DE DEFINIÇÃO]** Quantidade de registros e quilogramas exatos de perdas acumuladas da Banana Prata.
