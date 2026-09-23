# Especificação Técnica de Dados: Fontes CSV para Camada de BI

---

## 1. Visão Geral

Este documento apresenta o detalhamento arquitetural e a especificação técnica das **7 fontes de dados em formato CSV** que sustentarão a camada de Business Intelligence e Automações do **Supermercado Alvorada Ltda.**

O modelo foi projetado com base estrita nas diretrizes consolidadas em `PLANEJAMENTO_INICIAL.md` e `CENARIO_E_DADOS.md`, atuando como ponte entre a extração operacional simulada e os futuros cálculos gerenciais de BI.

---

## 2. Detalhamento dos 7 Arquivos CSV

### 2.1. `produtos.csv`
*   **Finalidade:** Cadastro mestre dos 40 itens ativos comercializados pelo supermercado. Serve como dimensão central de produto para todas as métricas gerenciais.
*   **Granularidade:** Cada linha representa um produto único (SKU).
*   **Lista de Campos:**

| Campo | Significado | Tipo de Dado | Obrigatório / Opcional | Exemplo de Valor Fictício |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | Identificador único interno do produto | Inteiro | Obrigatório | `1` |
| `barcode` | Código de barras padrão EAN-13 | Texto | Obrigatório | `7891000100101` |
| `product_name` | Descrição comercial completa do item | Texto | Obrigatório | `Leite Integral 1L` |
| `category` | Categoria mercadológica principal | Texto | Obrigatório | `Laticínios e Frios` |
| `subcategory` | Classificação secundária do item | Texto | Obrigatório | `Leites` |
| `unit_of_measure` | Unidade de comercialização | Texto | Obrigatório | `UN` |
| `min_stock` | Ponto crítico mínimo de segurança | Decimal / Inteiro | Obrigatório | `30` |
| `ideal_stock` | Nível de estoque desejável para cobertura | Decimal / Inteiro | Obrigatório | `80` |
| `sale_price` | Preço de venda padrão praticado na gôndola | Decimal (10,2) | Obrigatório | `5.49` |
| `active_flag` | Indicador de produto ativo no mix | Texto (S/N) | Obrigatório | `S` |

*   **Chave Primária (PK):** `product_id`.
*   **Chaves Estrangeiras (FK):** Nenhuma nesta tabela (dimensão mestre).
*   **Regras de Consistência:** 
    *   `product_id` e `barcode` devem ser únicos;
    *   `min_stock` deve ser maior ou igual a zero;
    *   `ideal_stock` deve ser estritamente maior que `min_stock`;
    *   `sale_price` deve ser maior que zero;
    *   `category` deve pertencer a uma das 6 categorias oficiais aprovadas.
*   **Problemas de Qualidade a Simular (ETL):** Linhas com campos de texto com espaçamento extra ou inconsistência de caixa (maiúscula/minúscula), registros pontuais com `min_stock` em branco para tratamento de nulos.
*   **Uso nos Cruzamentos do BI:** Tabela dimensional primária conectada a todas as tabelas de movimentação (`vendas`, `compras`, `estoque`, `validade`, `perdas`). Provê os nomes, categorias e parâmetros de reposição para comparar com o estoque físico e calcular a cobertura de dias.

---

### 2.2. `fornecedores.csv`
*   **Finalidade:** Cadastro mestre dos fornecedores homologados para cotação e compras de reposição.
*   **Granularidade:** Cada linha representa uma empresa fornecedora parceira.
*   **Lista de Campos:**

| Campo | Significado | Tipo de Dado | Obrigatório / Opcional | Exemplo de Valor Fictício |
| :--- | :--- | :--- | :--- | :--- |
| `supplier_id` | Identificador único interno do fornecedor | Inteiro | Obrigatório | `101` |
| `company_name` | Razão social da empresa fornecedora | Texto | Obrigatório | `Laticínios da Serra Distribuidora Ltda` |
| `trade_name` | Nome fantasia comercial habitual | Texto | Obrigatório | `Da Serra Laticínios` |
| `cnpj` | CNPJ fictício da empresa | Texto | Obrigatório | `12.345.678/0001-90` |
| `contact_name` | Nome do vendedor ou representante | Texto | Obrigatório | `Carlos Silva` |
| `contact_whatsapp` | Telefone com DDD para envio de cotação | Texto | Opcional | `(11) 98765-4321` |
| `lead_time_days` | Prazo médio de entrega (em dias) | Inteiro | Obrigatório | `3` |
| `city_state` | Praça de faturamento (Município/UF) | Texto | Obrigatório | `Bragança Paulista/SP` |

*   **Chave Primária (PK):** `supplier_id`.
*   **Chaves Estrangeiras (FK):** Nenhuma nesta tabela.
*   **Regras de Consistência:** 
    *   `supplier_id` e `cnpj` devem ser únicos;
    *   `lead_time_days` deve ser maior ou igual a zero.
*   **Problemas de Qualidade a Simular (ETL):** Fornecedor com telefone de WhatsApp não cadastrado (nulo) para testar validação antes da geração da lista de cotação.
*   **Uso nos Cruzamentos do BI:** Conecta-se a `compras.csv` via `supplier_id`. Permite agrupar histórico de compras por parceiro, calcular tempo de ressuprimento e gerar o cabeçalho das mensagens de cotação para o WhatsApp.

---

### 2.3. `vendas.csv`
*   **Finalidade:** Registro transacional detalhado de todas as saídas ocorridas nos caixas de atendimento (PDVs), contendo também os dados fiscais de saída.
*   **Granularidade:** Cada linha representa um item vendido em um cupom fiscal de venda.
*   **Lista de Campos:**

| Campo | Significado | Tipo de Dado | Obrigatório / Opcional | Exemplo de Valor Fictício |
| :--- | :--- | :--- | :--- | :--- |
| `sale_id` | Identificador único da transação / cupom | Inteiro / Texto | Obrigatório | `10001` |
| `date_time` | Data e horário exato da venda | Data/Hora (ISO) | Obrigatório | `2026-04-05 14:32:10` |
| `pos_id` | Identificador do caixa que emitiu o cupom | Texto | Obrigatório | `PDV 01` |
| `product_id` | Código do item comercializado | Inteiro | Obrigatório | `1` |
| `quantity` | Quantidade ou peso faturado | Decimal (10,3) | Obrigatório | `2.000` |
| `unit_price` | Preço unitário praticado na transação | Decimal (10,2) | Obrigatório | `5.49` |
| `total_amount` | Valor total bruto do item na venda | Decimal (10,2) | Obrigatório | `10.98` |
| `payment_method` | Meio de pagamento utilizado | Texto | Obrigatório | `Cartão Débito` |
| `cfop` | Código Fiscal de Operações e Prestações | Texto | Obrigatório | `5102` |
| `icms_rate` | Alíquota de ICMS incidente na saída | Decimal (5,4) | Obrigatório | `0.1800` |
| `icms_amount` | Valor de ICMS apurado no item | Decimal (10,2) | Obrigatório | `1.98` |

*   **Chave Primária (PK):** Chave composta por (`sale_id`, `product_id`) ou identificador sequencial de item.
*   **Chaves Estrangeiras (FK):** `product_id` referenciando `produtos.csv`.
*   **Regras de Consistência:** 
    *   `quantity` deve ser maior que zero;
    *   `unit_price` deve ser maior ou igual a zero;
    *   `total_amount` deve corresponder a `quantity * unit_price` (com arredondamento padrão);
    *   `date_time` deve estar contido estritamente na janela temporal dos 90 dias (01/04/2026 a 29/06/2026).
*   **Problemas de Qualidade a Simular (ETL):** Linhas duplicadas de cupons, datas em formatos textuais diferentes para conversão, pequenas discrepâncias de arredondamento.
*   **Uso nos Cruzamentos do BI:** Fonte fundamental para apuração de faturamento diário, velocidade média de vendas (giro por dia), identificação de itens em desabastecimento (Leite), produtos parados (Café), e apuração do ICMS de saída para conciliação contábil.

---

### 2.4. `compras.csv`
*   **Finalidade:** Registro transacional das notas fiscais de entrada emitidas por fornecedores para reposição de mercadorias, incluindo custos e impostos destacados.
*   **Granularidade:** Cada linha representa um item adquirido em uma Nota Fiscal Eletrônica (NF-e) de entrada.
*   **Lista de Campos:**

| Campo | Significado | Tipo de Dado | Obrigatório / Opcional | Exemplo de Valor Fictício |
| :--- | :--- | :--- | :--- | :--- |
| `purchase_id` | Identificador interno do registro de entrada | Inteiro / Texto | Obrigatório | `501` |
| `nfe_number` | Número da Nota Fiscal de entrada | Texto | Obrigatório | `12345` |
| `purchase_date` | Data de emissão/recebimento da NF-e | Data (YYYY-MM-DD) | Obrigatório | `2026-04-02` |
| `supplier_id` | Código do fornecedor emissor | Inteiro | Obrigatório | `101` |
| `product_id` | Código do item adquirido | Inteiro | Obrigatório | `1` |
| `quantity` | Quantidade ou peso adquirido | Decimal (10,3) | Obrigatório | `100.000` |
| `unit_cost` | Custo unitário de aquisição do item | Decimal (10,2) | Obrigatório | `3.80` |
| `total_cost` | Valor total de custo do item | Decimal (10,2) | Obrigatório | `380.00` |
| `cfop` | CFOP de entrada de mercadoria | Texto | Obrigatório | `1102` |
| `icms_base` | Base de cálculo destacada de ICMS | Decimal (10,2) | Obrigatório | `380.00` |
| `icms_rate` | Alíquota de ICMS da nota de entrada | Decimal (5,4) | Obrigatório | `0.1800` |
| `icms_amount` | Valor de ICMS destacado na nota | Decimal (10,2) | Obrigatório | `68.40` |

*   **Chave Primária (PK):** Chave composta por (`purchase_id`, `product_id`) ou identificador de linha de compra.
*   **Chaves Estrangeiras (FK):** `supplier_id` referenciando `fornecedores.csv`; `product_id` referenciando `produtos.csv`.
*   **Regras de Consistência:** 
    *   `quantity` > 0 e `unit_cost` > 0;
    *   `total_cost` deve corresponder a `quantity * unit_cost`;
    *   `purchase_date` deve estar no intervalo de 01/04/2026 a 29/06/2026.
*   **Problemas de Qualidade a Simular (ETL):** Registros pontuais com duplicidade de nota fiscal, ou custos com separador decimal inadequado (vírgula vs. ponto).
*   **Uso nos Cruzamentos do BI:** Monitoramento histórico de variações de custo unitário (Cenário 4 - Arroz), consolidação do ICMS de entrada para relatório contábil, e cálculo de divergência entre compras e vendas (Cenário 7 - Óleo de soja).

---

### 2.5. `estoque.csv`
*   **Finalidade:** Retrato estático (*snapshot*) da posição física do estoque apurada ao final da janela de simulação.
*   **Granularidade:** Cada linha representa o saldo físico consolidado de um produto em uma determinada localização física da loja.
*   **Lista de Campos:**

| Campo | Significado | Tipo de Dado | Obrigatório / Opcional | Exemplo de Valor Fictício |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | Código do produto inventariado | Inteiro | Obrigatório | `1` |
| `current_quantity` | Quantidade física total apurada em saldo | Decimal (10,3) | Obrigatório | `12.000` |
| `reserved_quantity` | Quantidade avariada ou separada para troca | Decimal (10,3) | Obrigatório | `0.000` |
| `last_count_date` | Data da última contagem física | Data (YYYY-MM-DD) | Obrigatório | `2026-06-29` |
| `storage_location` | Localização do estoque (Loja ou Depósito) | Texto | Obrigatório | `Loja` |

*   **Chave Primária (PK):** Chave composta (`product_id`, `storage_location`).
*   **Chaves Estrangeiras (FK):** `product_id` referenciando `produtos.csv`.
*   **Regras de Consistência:** 
    *   `reserved_quantity` deve ser menor ou igual a `current_quantity`;
    *   `last_count_date` coerente com a data de corte do inventário.
*   **Problemas de Qualidade a Simular (ETL):** Simulação de um saldo de estoque negativo antes do tratamento (para evidenciar a detecção de inconsistências pelo BI).
*   **Uso nos Cruzamentos do BI:** Comparado com `min_stock` e `ideal_stock` em `produtos.csv` para apontar ruptura (Leite) ou excesso (Café); usado para calcular dias de cobertura juntamente com a média de vendas de `vendas.csv`.

---

### 2.6. `validade.csv`
*   **Finalidade:** Controle de shelf-life e datas de expiração de lotes para mercadorias perecíveis (especialmente Laticínios, Carnes e Hortifrúti).
*   **Granularidade:** Cada linha representa um lote específico de um produto com sua data de vencimento.
*   **Lista de Campos:**

| Campo | Significado | Tipo de Dado | Obrigatório / Opcional | Exemplo de Valor Fictício |
| :--- | :--- | :--- | :--- | :--- |
| `batch_id` | Identificador único do lote de fabricação | Texto | Obrigatório | `LOT-2026-0402` |
| `product_id` | Código do produto pertencente ao lote | Inteiro | Obrigatório | `2` |
| `expiration_date` | Data limite para consumo (vencimento) | Data (YYYY-MM-DD) | Obrigatório | `2026-07-05` |
| `batch_quantity` | Quantidade física remanescente no lote | Decimal (10,3) | Obrigatório | `25.000` |
| `entry_date` | Data de recebimento do lote no supermercado | Data (YYYY-MM-DD) | Obrigatório | `2026-06-15` |

*   **Chave Primária (PK):** `batch_id`.
*   **Chaves Estrangeiras (FK):** `product_id` referenciando `produtos.csv`.
*   **Regras de Consistência:** 
    *   `expiration_date` deve ser maior ou igual a `entry_date`;
    *   `batch_quantity` deve ser maior ou igual a zero.
*   **Problemas de Qualidade a Simular (ETL):** Registro pontual com formato de data invertido ou lote zerado mantido na base ativa para teste de filtragem.
*   **Uso nos Cruzamentos do BI:** Confronta a data de vencimento com a data de referência e com a média diária de vendas de `vendas.csv`, gerando o alerta de risco de vencimento (Cenário 3 - Iogurte natural).

---

### 2.7. `perdas.csv`
*   **Finalidade:** Registro operacional de baixas de estoque motivadas por quebras, avarias no manuseio, transporte, deterioração física e descarte de produtos vencidos.
*   **Granularidade:** Cada linha representa uma ocorrência formal de perda/descarte.
*   **Lista de Campos:**

| Campo | Significado | Tipo de Dado | Obrigatório / Opcional | Exemplo de Valor Fictício |
| :--- | :--- | :--- | :--- | :--- |
| `loss_id` | Identificador único do lançamento de perda | Inteiro / Texto | Obrigatório | `701` |
| `loss_date` | Data em que a ocorrência foi registrada | Data (YYYY-MM-DD) | Obrigatório | `2026-05-10` |
| `product_id` | Código do produto descartado | Inteiro | Obrigatório | `3` |
| `quantity` | Quantidade ou peso total descartado | Decimal (10,3) | Obrigatório | `8.500` |
| `loss_reason` | Motivo operacional da perda | Texto | Obrigatório | `Deterioração` |
| `unit_cost_at_loss` | Custo unitário do item no momento da baixa | Decimal (10,2) | Obrigatório | `2.10` |
| `total_loss_value` | Prejuízo financeiro total apurado da perda | Decimal (10,2) | Obrigatório | `17.85` |

*   **Chave Primária (PK):** `loss_id`.
*   **Chaves Estrangeiras (FK):** `product_id` referenciando `produtos.csv`.
*   **Regras de Consistência:** 
    *   `quantity` > 0 e `unit_cost_at_loss` >= 0;
    *   `total_loss_value` deve corresponder a `quantity * unit_cost_at_loss`;
    *   `loss_reason` deve estar restrito a valores padronizados (*Vencimento*, *Avaria*, *Quebra Física*, *Deterioração*);
    *   `loss_date` dentro do horizonte de 90 dias da simulação.
*   **Problemas de Qualidade a Simular (ETL):** Motivo de perda digitado com variação de grafia (ex.: "quebra", "QUEBRA", "Quebra") para testar padronização no BI.
*   **Uso nos Cruzamentos do BI:** Quantificação financeira do prejuízo operacional por categoria (Cenário 5 - Banana) e abatimento do lucro bruto para cálculo da margem líquida por família de produtos.

---

## 3. Relacionamentos entre os Arquivos

O modelo arquitetural adota uma topologia relacional analítica centralizada, onde o identificador do produto atua como elo de integração unificado entre estoques, vendas, compras, perdas e validades:

```
                  +-------------------+
                  |  fornecedores.csv |
                  +---------+---------+
                            |
                   supplier_id (1:N)
                            |
                            v
+-------------------+   compras.csv   <-- (purchase_id, datas)
|   produtos.csv    +-------+
+---------+---------+       |
          |                 |
   product_id (1:N)         |
          |                 |
          +---------------->+ (product_id)
          |
          +----------------> vendas.csv   <-- (sale_id, datas)
          |
          +----------------> estoque.csv
          |
          +----------------> validade.csv <-- (batch_id, datas)
          |
          +----------------> perdas.csv   <-- (loss_id, datas)
```

### Explicação das Chaves de Relacionamento:

*   **`product_id` (Chave Dimensional Central):**
    *   Origem: Chave Primária (PK) em `produtos.csv`.
    *   Destino: Chave Estrangeira (FK) em `vendas.csv`, `compras.csv`, `estoque.csv`, `validade.csv` e `perdas.csv`.
    *   *Finalidade no BI:* Permite conectar vendas passadas ao saldo em estoque atual, checar compras históricas, correlacionar lotes perecíveis e apurar perdas acumuladas de cada item individualmente.
*   **`supplier_id` (Chave de Suprimentos):**
    *   Origem: Chave Primária (PK) em `fornecedores.csv`.
    *   Destino: Chave Estrangeira (FK) em `compras.csv`.
    *   *Finalidade no BI:* Agrupa o histórico de entradas e custos por fornecedor, analisa variações de preços praticados e identifica o contato de WhatsApp para envio de cotações automáticas.
*   **`sale_id` (Chave Transacional de Saída):**
    *   Origem: Identificador de cupom fiscal em `vendas.csv`.
    *   *Finalidade no BI:* Agrupa os itens comprados na mesma transação para permitir o cálculo de ticket médio, produtos comprados em conjunto e volume de atendimentos por caixa.
*   **`purchase_id` / `nfe_number` (Chave Transacional de Entrada):**
    *   Origem: Identificador de nota fiscal em `compras.csv`.
    *   *Finalidade no BI:* Permite a auditoria de faturas de compras inteiras, verificação de impostos destacados (ICMS) e confronto de volumes recebidos por nota.
*   **`batch_id` (Chave de Controle de Lote):**
    *   Origem: Identificador de lote em `validade.csv`.
    *   *Finalidade no BI:* Rastreia frações de produtos perecíveis com datas de vencimento distintas, permitindo agir preventivamente antes da data de expiração.
*   **Dimensão Temporal (`datas` / `date_time`):**
    *   Presente em: `vendas.csv` (`date_time`), `compras.csv` (`purchase_date`), `estoque.csv` (`last_count_date`), `validade.csv` (`expiration_date`, `entry_date`) e `perdas.csv` (`loss_date`).
    *   *Finalidade no BI:* Sincroniza todas as métricas em uma linha do tempo unificada de 90 dias, viabilizando médias móveis, análises de sazonalidade semanal e comparativos cronológicos.

---

## 4. Regras para Geração Futura dos Dados Fictícios

Para garantir coerência, estabilidade e total aderência às decisões já aprovadas, a futura geração de registros fictícios deverá observar as seguintes regras previamente fixadas:

1.  **Horizonte Temporal Estrito:**
    *   Período compreendido entre **01/04/2026 e 29/06/2026** (janela contínua de 90 dias).
2.  **Catálogo Fechado em 40 Produtos Fictícios:**
    *   Mercearia Seca: 8 produtos;
    *   Laticínios e Frios: 7 produtos;
    *   Hortifrúti: 6 produtos;
    *   Açougue e Carnes: 6 produtos;
    *   Bebidas: 7 produtos;
    *   Higiene e Limpeza: 6 produtos.
3.  **Fornecedores Homologados:**
    *   Exatamente 8 empresas fornecedoras fictícias cadastradas em `fornecedores.csv`.
4.  **Linha de Base de Comportamento Normal:**
    *   Cerca de 33 produtos deverão apresentar comportamento operacional equilibrado (vendas estáveis, estoque suficiente, custos de aquisição homogêneos e perdas normais ou nulas) para que a massa de dados não gere alertas generalizados irreais.
5.  **Garantia dos 7 Cenários de Teste Específicos:**
    *   *Cenário 1 (Estoque Crítico):* `Leite Integral 1L` com estoque insuficiente frente à demanda de vendas.
    *   *Cenário 2 (Candidato a Promoção):* `Café 500g` com saldo físico elevado e vendas em desaceleração.
    *   *Cenário 3 (Risco de Vencimento):* `Iogurte Natural` com lote com data de validade próxima e giro insuficiente.
    *   *Cenário 4 (Aumento de Custo de Compra):* `Arroz 5kg` com histórico de compras demonstrando elevação expressiva de preço na nota mais recente.
    *   *Cenário 5 (Perdas):* `Banana` com lançamentos detalhados de descarte, quebra e avaria por motivo.
    *   *Cenário 6 (Lista de Cotação):* Conjunto de itens em desabastecimento agrupados para montagem de texto para WhatsApp.
    *   *Cenário 7 (Divergência Gerencial de 15%):* `Óleo de Soja 900ml` com discrepância superior a 15% entre compras e saídas (parâmetro estritamente gerencial).
6.  **Habilitação de Cruzamentos Analíticos:**
    *   Os volumes transacionados devem permitir a conciliação completa entre entradas, saídas, perdas e saldos remanescentes de inventário sem gerar incoerências matemáticas absurdas.

---

## 5. Itens Pendentes de Definição (Antes da Geração dos Registros)

Conforme orientação metodológica, registram-se abaixo os pontos cuja definição exata **permanece pendente** e deverá ser deliberada antes da criação dos arquivos CSV reais:

*   **[PENDENTE DE DEFINIÇÃO]** Nomes comerciais definitivos, códigos de barras e subcategorias dos 40 produtos do catálogo.
*   **[PENDENTE DE DEFINIÇÃO]** Razões sociais, nomes fantasia, CNPJs fictícios e números de WhatsApp dos 8 fornecedores.
*   **[PENDENTE DE DEFINIÇÃO]** Matriz de vínculo entre fornecedores e produtos (quais produtos são fornecidos por quais parceiros).
*   **[PENDENTE DE DEFINIÇÃO]** Volumes exatos de vendas diárias por caixa e ticket médio para cada produto.
*   **[PENDENTE DE DEFINIÇÃO]** Preços médios de custo e preços de venda de cada um dos 40 itens.
*   **[PENDENTE DE DEFINIÇÃO]** Percentual exato do aumento de custo do Arroz 5kg na última compra.
*   **[PENDENTE DE DEFINIÇÃO]** Dias exatos para corte do alerta de validade do Iogurte e número de dias restantes do lote.
*   **[PENDENTE DE DEFINIÇÃO]** Volume exato e quantidades dos registros de perdas da Banana e de outros itens.
