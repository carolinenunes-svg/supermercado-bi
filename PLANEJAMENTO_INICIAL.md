# Planejamento Inicial do Projeto

## 1. Nome Provisório do Projeto
**SuperBI: Camada Gerencial de Business Intelligence e Automação para Supermercados**

---

## 2. Conceito
O projeto consiste no desenvolvimento de uma camada gerencial de **Business Intelligence (BI) com automações** voltada para o setor supermercadista. 

A solução atuará de forma **complementar ao sistema operacional já existente** no supermercado. O sistema atual continuará sendo responsável pelas operações originais (registro de vendas no PDV, movimentações de estoque e entradas de mercadorias via notas fiscais).

O novo sistema terá como papel exclusivo:
- Receber dados gerados pelo sistema operacional;
- Tratar, higienizar e integrar essas informações;
- Transformar dados operacionais brutos em indicadores de desempenho (KPIs), alertas gerenciais, relatórios estruturados e ferramentas de apoio à tomada de decisão.

---

## 3. Contexto
- **Natureza:** Projeto acadêmico.
- **Curso:** Administração.
- **Disciplina:** Tecnologias e Automação na Indústria.
- **Contextualização prática:** Atendimento à orientação docente de conectar a teoria com a realidade próxima dos estudantes, tendo o supermercado como objeto de estudo devido à alta complexidade de suas operações, grande volume de movimentações diárias e margens operacionais reduzidas.

---

## 4. Problema de Negócio
Supermercados geram diariamente um volume expressivo de registros operacionais. No entanto, os sistemas convencionais de frente de loja e retaguarda operacional costumam armazenar os dados com foco imediato no processo transacional (registrar a venda, dar baixa no estoque, emitir o cupom fiscal).

Isso cria uma **lacuna entre a operação e a gestão estratégica**, resultando em:
- Dificuldade para saber com precisão e agilidade o que comprar e quando repor;
- Risco de rupturas de gôndola ou excesso de mercadoria estagnada;
- Perdas silenciosas causadas pelo vencimento de produtos sem alerta prévio;
- Falta de controle sobre a evolução de preços cobrados pelos fornecedores;
- Lentidão para identificar itens sem giro que deveriam entrar em promoção;
- Ausência de alertas gerenciais para divergências entre compras e vendas ou inconsistências cadastrais e fiscais.

---

## 5. Objetivo Geral
Desenvolver uma solução de Business Intelligence com automações para supermercados, utilizando dados operacionais já existentes para gerar indicadores, alertas, relatórios e informações gerenciais que apoiem a tomada de decisão em áreas como compras, estoque, prevenção de perdas, fornecedores, promoções e gestão geral.

---

## 6. Objetivos Específicos Preliminares
1. **Compras e Reposição:** Estruturar mecanismos de apoio à decisão de compra com base no histórico de vendas e saldo atual, além de gerar listas padronizadas para cotação com fornecedores.
2. **Estoque e Rotação:** Acompanhar níveis de estoque, calcular giro e identificar produtos com risco de desabastecimento ou excesso de capital imobilizado.
3. **Prevenção de Perdas e Validades:** Monitorar itens próximos ao vencimento e quantificar perdas registradas por motivos operacionais (avaria, quebra, descarte).
4. **Inteligência Comercial:** Cruzar volume em estoque com velocidade de saída para apontar candidatos a campanhas promocionais.
5. **Monitoramento de Fornecedores:** Analisar o histórico de preços de compras para identificar aumentos relevantes entre aquisições sucessivas.
6. **Apoio à Análise Fiscal:** Apresentar dados consolidados sobre operações com ICMS e apontar divergências compra/venda para posterior conferência contábil.
7. **Visão Panorâmica Executiva:** Centralizar os principais indicadores do supermercado em um dashboard gerencial acessível e intuitivo.

---

## 7. Módulos Preliminares
> **Aviso de Escopo:** Estes módulos são preliminares e deverão ser ajustados e validados de acordo com a disponibilidade real dos dados da empresa e com as exigências pedagógicas do professor orientador.

1. **Módulo de Compras e Reposição:** Sugestão de pedidos e elaboração de listas de cotação.
2. **Módulo de Estoque:** Monitoramento de saldos, giro e estoque mínimo de segurança.
3. **Módulo de Validade:** Acompanhamento de datas críticas de vencimento de lotes.
4. **Módulo de Promoções:** Identificação de produtos de baixo giro com alto estoque.
5. **Módulo de Fornecedores:** Histórico de custos, comparativo de compras e variação de preços.
6. **Módulo de Perdas e Desperdícios:** Classificação e apuração de custos decorrentes de quebras, avarias e vencimentos.
7. **Módulo de Indicadores para Análise Fiscal:** Visualização informativa de dados tributários e divergências para suporte contábil.
8. **Módulo de Dashboard Gerencial:** Painel com indicadores consolidados para a liderança.

---

## 8. Princípios e Limitações

1. **Não substituição:** O sistema operacional em uso pelo supermercado não será substituído.
2. **Não violação da base original:** Não haverá alteração direta de tabelas ou registros do sistema operacional de origem.
3. **Alimentação não invasiva:** O novo sistema trabalhará estritamente com base nos dados exportados ou fornecidos pela retaguarda.
4. **Tratamento prévio:** Todos os dados recebidos deverão passar por processos de validação, consistência e higienização antes do cálculo dos indicadores.
5. **Transparência de regras:** Toda regra de negócio deverá ser documentada com clareza e rastreabilidade.
6. **Parametrização flexível:** Regras que dependem da dinâmica específica do negócio deverão ser configuráveis pelos gestores.
7. **Critério gerencial de divergência (15%):** O percentual de 15% proposto inicialmente entre compras e vendas é exclusivamente um parâmetro gerencial configurável de alerta interno, sem caráter de regra tributária ou legal.
8. **Responsabilidade fiscal estrita:** Dados de ICMS e correlatos serão tratados como indicadores informativos para encaminhamento à assessoria contábil/fiscal. O sistema não declarará créditos tributários automáticos.
9. **Operacionalização sem integração complexa:** A geração de listas para cotação fornecerá texto estruturado para cópia e colagem no WhatsApp pelo usuário. Não será desenvolvida integração com APIs de mensageria nesta etapa.
10. **Segurança e Privacidade Acadêmica:** Proibido o uso de dados pessoais sensíveis ou dados corporativos confidenciais reais. O projeto utilizará massas de dados fictícias, anonimizadas ou mascaradas.

---

## 9. O que Ainda Precisa Ser Definido
Antes de avançar para qualquer etapa técnica, é necessário definir:
- **Formato de entrega dos dados:** Como o sistema atual gera as extrações (planilhas Excel/CSV, arquivos de texto delimitados, relatórios pré-formatados ou arquivos XML de NF-e).
- **Periodicidade da carga:** Se a importação dos dados para a camada analítica ocorrerá de forma diária, semanal ou mensal.
- **Presença de controle de validade:** Se o sistema operacional atual do supermercado efetivamente possui cadastro e baixa por lote/validade, ou se esse controle hoje ocorre de maneira física/informal.
- **Mapeamento de motivos de perdas:** Como o supermercado registra internamente as avarias, quebras e descartes.
- **Fórmulas de reposição adotadas:** Critérios aceitos pelo negócio ou pela disciplina para definição de estoque mínimo, estoque de segurança e ponto de pedido.

---

## 10. Decisões que Dependem da Análise dos Dados (Reais ou Fictícios)
- **Validação de viabilidade dos módulos:** Confirmar quais dos 8 módulos preliminares possuem colunas e registros suficientes para serem calculados ou se algum precisará de dados simulados/adaptados.
- **Estratégia para o módulo de validade:** Caso a base de dados não contenha datas de vencimento por item/lote, decidir se o módulo será alimentado por uma estrutura complementar simulada ou se o escopo será readequado.
- **Definição dos campos fiscais disponíveis:** Avaliar se a base de entrada conta com dados discriminados de ICMS (base de cálculo, alíquota, valor, CST/CSOSN) para saber que nível de detalhe analítico poderá ser oferecido ao setor contábil.
- **Priorização do cronograma acadêmico:** Estabelecer quais módulos comporão o núcleo prioritário (MVP acadêmico) do projeto em função da complexidade e do prazo de entrega da disciplina.
