# Cenário de Negócio e Estrutura de Dados (Consolidado)

---

## 1. Registro de Decisões Humanas Aprovadas

As seguintes diretrizes fundamentais foram definidas e aprovadas pela gestão do projeto, constituindo premissas fixadas:

1.  **Estrutura de Dados em 7 Arquivos CSV:**
    *   Aprovada a eliminação do arquivo isolado `fiscal.csv`.
    *   As informações fiscais foram incorporadas diretamente às operações:
        *   `compras.csv`: Incorpora campos fiscais de entrada (CFOP, base de cálculo, alíquota e valor do ICMS).
        *   `vendas.csv`: Incorpora campos fiscais de saída (CFOP, alíquota e ICMS quando aplicáveis).
2.  **Horizonte Temporal de 90 Dias:**
    *   A simulação conterá uma janela contínua de 90 dias de movimentações fictícias.
    *   Abrangerá o ciclo completo de compras, vendas, perdas, giro de estoque, sazonalidade semanal e flutuações de preços.
3.  **Catálogo Fechado em 40 Produtos Fictícios:**
    *   *Mercearia Seca:* 8 produtos;
    *   *Laticínios e Frios:* 7 produtos;
    *   *Hortifrúti:* 6 produtos;
    *   *Açougue e Carnes:* 6 produtos;
    *   *Bebidas:* 7 produtos;
    *   *Higiene e Limpeza:* 6 produtos;
    *   **Total exato:** 40 produtos.

---

## 2. Cenário do Supermercado Fictício

*   **Razão Social / Nome Fantasia:** *Supermercado Alvorada Ltda.*
*   **Perfil:** Supermercado de médio porte (varejo de proximidade).
*   **Operação:** 4 a 6 caixas de atendimento (PDVs), recebimento de mercadorias com conferência via NF-e, depósito de retaguarda e reposição diária de loja.
*   **Mix Ativo na Simulação:** Exatamente 40 itens cadastrados, distribuídos estrategicamente nas 6 categorias principais para evidenciar comportamentos típicos de giro rápido, giro lento, alta perecibilidade e estabilidade.

---

## 3. Objetivo da Simulação

Gerar uma massa de dados fictícia e controlada cobrindo o período de 90 dias para abastecer a camada externa de Business Intelligence. O objetivo não é gerar dados aleatórios, mas estruturar um ambiente realista em que regras de negócio, cálculos e cruzamentos permitam ao BI identificar situações gerenciais concretas e emitir alertas acionáveis.

---

## 4. Cenários de Negócio e Casos de Teste

Para que o futuro sistema de BI demonstre valor prático à gestão, a massa de dados conterá situações propositais e controladas distribuídas entre produtos-chave, além de uma linha de base realista de comportamento normal.

### 4.1. Cenário 1 — Estoque Crítico
*   **Produto de Referência:** *Leite integral 1 L* (Categoria: Laticínios e Frios).
*   **Objetivo do Cenário:** Simular uma situação de desabastecimento iminente (ruptura) de um item de primeira necessidade e alto giro.
*   **Informações que Identificam o Problema:** Cruzamento do saldo disponível em `estoque.csv` com a média móvel de vendas diárias em `vendas.csv`, evidenciando que o estoque atual cobre menos dias do que o prazo de reposição (*lead time* em `fornecedores.csv`) ou está abaixo do `min_stock` cadastrado em `produtos.csv`.
*   **Resultado Esperado do Futuro BI:** Geração de alerta visual de "Risco Crítico de Ruptura / Estoque Baixo", com cálculo automático da quantidade sugerida para pedido de reposição.
*   **Parâmetros a Definir Posteriormente:** Estoque mínimo exato, prazo de entrega do fornecedor de laticínios e fórmula de cobertura de dias de segurança.

---

### 4.2. Cenário 2 — Candidato a Promoção
*   **Produto de Referência:** *Café 500 g* (Categoria: Mercearia Seca).
*   **Objetivo do Cenário:** Identificar capital de giro excessivamente imobilizado em um item com saída estagnada.
*   **Informações que Identificam o Problema:** Relação desproporcional entre a quantidade física elevada em `estoque.csv` e a desaceleração relevante no volume de unidades registradas em `vendas.csv` nas últimas semanas da simulação.
*   **Resultado Esperado do Futuro BI:** Sinalização gerencial do item como "Candidato a Ação Promocional / Queima de Estoque". O sistema indicará a oportunidade e o excedente em estoque, mas **não** decidirá o percentual de desconto ou o preço promocional (decisão que cabe ao gestor comercial).
*   **Parâmetros a Definir Posteriormente:** Índice de cobertura em dias considerado excessivo (ex.: estoque superior a 45 ou 60 dias de vendas médias).

---

### 4.3. Cenário 3 — Risco de Vencimento
*   **Produto de Referência:** *Iogurte natural* (Categoria: Laticínios e Frios).
*   **Objetivo do Cenário:** Evitar perdas materiais por expiração de shelf-life através da antecipação de ações na gôndola.
*   **Informações que Identificam o Problema:** Comparação entre a data de validade do lote em `validade.csv` e a data de referência, confrontada com a velocidade de saída em `vendas.csv`. O cálculo demonstrará que o saldo do lote não será absorvido pela demanda habitual antes do vencimento.
*   **Resultado Esperado do Futuro BI:** Emissão de "Alerta de Atenção: Vencimento Próximo", informando o número do lote, os dias restantes de validade e o volume projetado de perda caso nenhuma ação seja tomada.
*   **Parâmetros a Definir Posteriormente:** Régua de dias para corte do alerta (ex.: lotes com menos de 7 ou 10 dias) e critérios de priorização no painel de validade.

---

### 4.4. Cenário 4 — Aumento de Custo de Compra
*   **Produto de Referência:** *Arroz 5 kg* (Categoria: Mercearia Seca).
*   **Objetivo do Cenário:** Monitorar a evolução dos preços de aquisição junto aos fornecedores para proteger a margem bruta de lucro.
*   **Informações que Identificam o Problema:** Comparativo cronológico do campo `unit_cost` em `compras.csv` entre notas fiscais consecutivas de entrada do mesmo item ao longo dos 90 dias, revelando uma elevação atípica na compra mais recente.
*   **Resultado Esperado do Futuro BI:** Alerta de "Variação Relevante de Custo de Entrada", apresentando o custo anterior, o novo custo, o percentual de aumento e o impacto projetado na margem de comercialização atual.
*   **Parâmetros a Definir Posteriormente:** Percentual mínimo de variação de custo para disparar o alerta (ex.: aumentos acima de 5% ou 8%) e período de comparação.

---

### 4.5. Cenário 5 — Gestão e Registro de Perdas
*   **Produto de Referência:** *Banana* (Categoria: Hortifrúti).
*   **Objetivo do Cenário:** Mensurar o desperdício operacional de produtos perecíveis e apurar as causas predominantes de prejuízo.
*   **Informações que Identificam o Problema:** Lançamentos sistemáticos de baixas em `perdas.csv` discriminados por data, quantidade descartada, custo unitário e motivo da ocorrência (*Avaria/Embalagem*, *Deterioração*, *Vencimento*, *Quebra*).
*   **Resultado Esperado do Futuro BI:** Relatório e indicador visual de perdas (volume físico e valor monetário total), detalhando o impacto na rentabilidade da categoria Hortifrúti e o ranking de causas de descarte.
*   **Parâmetros a Definir Posteriormente:** Frequência dos lançamentos de perdas e limite aceitável de tolerância de perdas do setor (benchmark operacional).

---

### 4.6. Cenário 6 — Geração de Lista de Cotação
*   **Produtos Envolvidos:** Conjunto de itens do catálogo que atingirem necessidade simultânea de reposição.
*   **Objetivo do Cenário:** Otimizar o tempo operacional do comprador na consolidação de pedidos para cotação com os parceiros.
*   **Informações que Identificam o Problema:** Filtro automatizado que varre `estoque.csv`, identifica itens abaixo do ponto de reposição, agrupa-os por `supplier_id` em `compras.csv` / `produtos.csv` e calcula a quantidade faltante para atingir o estoque ideal.
*   **Resultado Esperado do Futuro BI:** Emissão de relatório e formatação de um bloco de texto estruturado contendo: fornecedor, código, descrição do item, quantidade sugerida e unidade de medida. O texto estará pronto para **cópia e colagem manual no WhatsApp** pelo comprador (sem integração direta via API nesta etapa).
*   **Parâmetros a Definir Posteriormente:** Layout exato do texto estruturado e critérios de cálculo da quantidade a pedir (ex.: cobertura para 15 ou 21 dias).

---

### 4.7. Cenário 7 — Divergência Gerencial de 15%
*   **Produto de Referência:** *Óleo de soja 900 ml* (Categoria: Mercearia Seca).
*   **Objetivo do Cenário:** Identificar anomalias e descompassos relevantes entre os fluxos de entrada e saída para investigação interna de inventário ou faturamento.
*   **Informações que Identificam o Problema:** Apuração da relação percentual calculada entre o volume total comprado em `compras.csv` e o volume vendido em `vendas.csv` (ajustado pela variação de saldo em `estoque.csv`). O cálculo revelará uma disparidade superior ao limite de 15%.
*   **Resultado Esperado do Futuro BI:** Emissão de "Alerta Gerencial de Divergência Compra x Venda", indicando a necessidade de conferência física e auditoria de registros.
*   **Ressalva Fundamental:** O percentual de 15% é **exclusivamente um parâmetro gerencial configurável** do supermercado. Não representa nem deve ser tratado como regra fiscal, legal ou tributária.
*   **Parâmetros a Definir Posteriormente:** Janela de fechamento do cálculo (mensal ou consolidado dos 90 dias) e fórmula exata de conciliação.

---

### 4.8. Linha de Base: Cenários de Comportamento Normal
Para garantir o realismo da massa de dados e evitar que o BI apresente alertas para todos os itens indiscriminadamente, os demais produtos do catálogo (aproximadamente 33 itens) apresentarão comportamento operacional equilibrado:
*   **Giro e Demanda:** Produtos de alta rotação com reposição regular e sem rupturas; produtos de rotação média com vendas previsíveis; e itens de baixa rotatividade sem estoque excessivo.
*   **Estabilidade de Preços:** Compras com custos estáveis ou oscilações marginais típicas de mercado (abaixo da régua de alerta).
*   **Estoque Saudável:** Níveis de inventário compatíveis com os estoques mínimo e ideal.
*   **Perdas Naturais:** Produtos com perdas nulas e produtos com níveis residuais normais de avaria.
*   **Relacionamento Comercial:** Fornecedores com pontualidade de entrega e condições comerciais homogêneas.

> **Princípio Metodológico:** Os casos de teste devem ser plenamente detectáveis pelo BI, mas construídos com sutileza e coerência interna, sem números artificiais ou distorções simplistas.

---

## 5. Fontes de Dados Aprovadas (7 Arquivos CSV)

1.  `produtos.csv`: Cadastro mestre dos 40 itens com parâmetros gerenciais.
2.  `fornecedores.csv`: Cadastro dos parceiros de suprimentos e contatos de cotação.
3.  `vendas.csv`: Transações analíticas de saída nos caixas, acrescidas de dados fiscais de venda.
4.  `compras.csv`: Entradas de mercadorias via notas fiscais, integrando custos e dados fiscais de aquisição.
5.  `estoque.csv`: Foto do saldo físico em loja e depósito.
6.  `validade.csv`: Controle granular de lotes e datas de expiração para produtos perecíveis.
7.  `perdas.csv`: Apontamentos operacionais de quebra, avaria e descarte.

---

## 6. Estrutura Proposta dos Campos por Arquivo

### 6.1. `produtos.csv` (Cadastro de Produtos)
*   `product_id` (Texto/Numérico): Código interno do produto (1 a 40).
*   `barcode` (Texto): Código de barras padrão EAN-13.
*   `product_name` (Texto): Descrição comercial do produto.
*   `category` (Texto): Uma das 6 categorias oficiais.
*   `subcategory` (Texto): Classificação secundária.
*   `unit_of_measure` (Texto): UN, KG, CX ou LT.
*   `min_stock` (Numérico): Ponto crítico de reposição.
*   `ideal_stock` (Numérico): Nível desejável de cobertura.
*   `sale_price` (Decimal): Preço de venda padrão praticado na gôndola.
*   `active_flag` (Texto): Situação cadastral (S/N).

### 6.2. `fornecedores.csv` (Cadastro de Fornecedores)
*   `supplier_id` (Texto/Numérico): Código identificador do fornecedor.
*   `company_name` (Texto): Razão social.
*   `trade_name` (Texto): Nome fantasia habitual.
*   `cnpj` (Texto): CNPJ formatado (fictício).
*   `contact_name` (Texto): Nome do vendedor/representante.
*   `contact_whatsapp` (Texto): Telefone para envio das cotações em texto.
*   `lead_time_days` (Numérico): Prazo médio de entrega (em dias).
*   `city_state` (Texto): Município e UF de faturamento.

### 6.3. `vendas.csv` (Saídas Operacionais e Fiscais)
*   `sale_id` (Texto/Numérico): Identificador único do cupom fiscal.
*   `date_time` (Data/Hora): Data e horário da transação (ao longo dos 90 dias).
*   `pos_id` (Texto): Número do caixa (PDV 1 a PDV 6).
*   `product_id` (Texto/Numérico): Código do item vendido.
*   `quantity` (Decimal/Numérico): Quantidade ou peso faturado.
*   `unit_price` (Decimal): Preço unitário praticado na venda.
*   `total_amount` (Decimal): Valor total bruto da linha de venda.
*   `payment_method` (Texto): Dinheiro, Cartão Débito, Cartão Crédito, PIX.
*   `cfop` (Texto): CFOP da venda (ex.: 5102).
*   `icms_rate` (Decimal): Alíquota incidente de ICMS na saída.
*   `icms_amount` (Decimal): Valor do imposto apurado na venda.

### 6.4. `compras.csv` (Entradas de Mercadorias e Fiscal)
*   `purchase_id` (Texto/Numérico): Identificador interno da entrada.
*   `nfe_number` (Texto): Número da Nota Fiscal de entrada.
*   `purchase_date` (Data): Data de emissão/recebimento.
*   `supplier_id` (Texto/Numérico): Fornecedor emissor da nota.
*   `product_id` (Texto/Numérico): Item adquirido.
*   `quantity` (Decimal/Numérico): Quantidade comprada.
*   `unit_cost` (Decimal): Custo unitário de aquisição.
*   `total_cost` (Decimal): Valor total da linha de compra.
*   `cfop` (Texto): CFOP de entrada (ex.: 1102).
*   `icms_base` (Decimal): Base de cálculo do ICMS de entrada.
*   `icms_rate` (Decimal): Alíquota destacada na nota de compra.
*   `icms_amount` (Decimal): Valor do ICMS destacado.

### 6.5. `estoque.csv` (Posição Física Atual)
*   `product_id` (Texto/Numérico): Código do produto.
*   `current_quantity` (Decimal/Numérico): Saldo físico total disponível.
*   `reserved_quantity` (Decimal/Numérico): Quantidade indisponível para venda.
*   `last_count_date` (Data): Data do último inventário físico.
*   `storage_location` (Texto): Loja/Gôndola ou Depósito.

### 6.6. `validade.csv` (Controle de Lotes Críticos)
*   `batch_id` (Texto): Identificador do lote.
*   `product_id` (Texto/Numérico): Código do item associado.
*   `expiration_date` (Data): Data limite para consumo.
*   `batch_quantity` (Decimal/Numérico): Quantidade física remanescente no lote.
*   `entry_date` (Data): Data de entrada do lote.

### 6.7. `perdas.csv` (Apontamentos de Quebras e Descartes)
*   `loss_id` (Texto/Numérico): Código da baixa de perda.
*   `loss_date` (Data): Data da constatação da perda.
*   `product_id` (Texto/Numérico): Item descartado.
*   `quantity` (Decimal/Numérico): Quantidade perdida.
*   `loss_reason` (Texto): *Vencimento*, *Avaria*, *Quebra Física*, *Deterioração*.
*   `unit_cost_at_loss` (Decimal): Custo unitário do produto no momento do registro.
*   `total_loss_value` (Decimal): Prejuízo financeiro total da ocorrência.

---

## 7. Relacionamentos entre as Fontes

*   `product_id`: Chave primária em `produtos.csv` que conecta de forma relacional `vendas.csv`, `compras.csv`, `estoque.csv`, `validade.csv` e `perdas.csv`.
*   `supplier_id`: Chave primária em `fornecedores.csv` que se relaciona com `compras.csv`.
*   `sale_id` e `purchase_id`: Chaves transacionais para agregações de cupons de venda e notas de compra.
*   Dimensão Temporal (`date` / `date_time`): Presente em `vendas`, `compras`, `perdas` e `validade`, alinhando os 90 dias do horizonte temporal.

---

## 8. Simulação de Problemas de Qualidade (Para Validação do ETL)

1.  **Linhas duplicadas pontuais** em `vendas.csv` ou `compras.csv`.
2.  **Valores nulos controlados** em campos não críticos (ex.: telefone de contato não informado em fornecedor).
3.  **Datas em padrões mistos** para checagem de padronização temporal.
4.  **Registros com saldo de estoque inconsistente** antes do tratamento de inventário.

---

## 9. Informações que Ainda Precisam Ser Definidas Antes da Geração dos CSVs

1.  **Catálogo Nominal dos 40 Produtos:** Nome exato de cada um dos 40 itens e suas respectivas unidades de medida e categorias.
2.  **Lista dos Fornecedores Fictícios:** Razão social, dados de contato e categorias atendidas para os parceiros de compras.
3.  **Data de Início e Término do Período de 90 Dias:** Definição do intervalo de datas do calendário fictício.
4.  **Parâmetros de Alerta:** Valores de tolerância (margem de dias para vencimento, percentual exato de aumento de arroz, etc.).
