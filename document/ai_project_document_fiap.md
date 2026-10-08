<img src="../assets/logo-fiap.png" alt="FIAP" width="30%">

# AI Project Document — Fase 2 — CardioIA

**Grupo 100** · Felipe Bernardo Papaléo de Oliveira  
07/10/2026 · Versão 0.1.0 · Preparação com assistência de IA

## Sumário

1. [Introdução](#1-introdução)
2. [Visão geral](#2-visão-geral-do-projeto)
3. [Desenvolvimento](#3-desenvolvimento-do-projeto)
4. [Resultados](#4-resultados-e-avaliações)
5. [Conclusões](#5-conclusões-e-trabalhos-futuros)
6. [Referências](#6-referências)

## 1. Introdução

### 1.1. Escopo do projeto

#### 1.1.1. Contexto da inteligência artificial

O processamento de linguagem natural permite representar relatos textuais em estruturas que algoritmos podem analisar. Neste trabalho, o contexto de cardiologia serve como cenário de aprendizagem. O escopo limita-se à simulação acadêmica da Fase 2, sem pacientes reais e sem implantação assistencial.

#### 1.1.2. Solução desenvolvida

A primeira parte extrai sintomas de dez frases e os associa a hipóteses por regras. A segunda classifica 80 frases fictícias com TF-IDF e regressão logística. Os resultados são acompanhados de testes de linguagem, análise dos termos influentes e limites explícitos. Os desafios opcionais não estão incluídos.

## 2. Visão geral do projeto

### 2.1. Objetivos

Construir uma cadeia reproduzível de leitura de dados, representação textual, classificação e avaliação; registrar evidências das associações; identificar situações em que as regras e o modelo falham; relacionar esses limites à qualidade e à justiça dos dados.

### 2.2. Público-alvo

Estudantes e docentes que avaliam os conceitos de NLP e aprendizado supervisionado. O projeto não é destinado a pacientes ou a profissionais em decisões de atendimento.

### 2.3. Metodologia

Criar dados sintéticos documentados, implementar o extrator, fixar o protocolo de aprendizagem, separar treino/teste, executar a Pipeline, comparar com baseline e analisar desafios fora do treino. Os parâmetros não foram ajustados após ver o teste. A estrutura documental foi adaptada do template oficial indicado na atividade.

## 3. Desenvolvimento do projeto

### 3.1. Tecnologias utilizadas

Python 3.12, scikit-learn 1.7.2, pandas 2.2.3, NumPy 2.2.6, SciPy 1.15.3 e Matplotlib 3.10.3. Notebook via nbformat/nbclient. Testes com unittest. A demonstração local usa HTML, JavaScript e servidor Python da biblioteca padrão, vinculado apenas a 127.0.0.1.

### 3.2. Modelagem e algoritmos

O mapa de conhecimento contém nove linhas, com duas expressões, hipótese, fonte e observação em cada linha. A busca ignora caixa e acentos e respeita limites de palavra. Uma heurística reconhece negações em até seis palavras anteriores dentro da mesma cláusula. As hipóteses são retornadas com evidências; sintomas ausentes do mapa não recebem diagnóstico forçado.

O classificador é uma Pipeline de TF-IDF de unigramas/bigramas e regressão logística com C=1, máximo de 1.000 iterações e semente 42. O vocabulário e IDF são ajustados somente no treino. Não removemos stopwords para preservar palavras de negação. Isso não garante compreensão: o modelo ainda pode ignorar seu efeito.

### 3.3. Treinamento e teste

A base tem 80 registros sem duplicatas exatas, 40 por rótulo. A divisão estratificada 75/25 separa 60 exemplos de treino e 20 de teste, dez por classe no teste. Frases parecidas em vocabulário podem aparecer nas duas partições, de modo que o resultado é otimista para generalização.

Os 12 desafios linguísticos são adicionais e não entram no ajuste. Quatro bases geram 16 frases contrafactuais que variam gênero/idade. As partições e predições são salvas para auditoria. Os rótulos são didáticos, sem validação profissional; sua regra e proveniência constam em `dados_e_limites.md`.

## 4. Resultados e avaliações

### 4.1. Análise dos resultados

| Avaliação | Resultado observado |
|---|---|
| Acurácia no teste | 19/20 = 95% |
| Baseline | 10/20 = 50% |
| Matriz: linhas reais, colunas previstas; baixo/alto | [[9, 1], [0, 10]] |
| Precisão de alto risco | 10/11 = 90,9% |
| Recall de alto risco | 10/10 = 100% |
| F1 macro | 0,9499 |
| Desafios linguísticos | 8/12 = 66,7% |
| Negação | 1/4 |
| Negação mista / temporalidade | 2/2 em cada categoria |
| Linguagem coloquial | 3/4 |
| Mudanças de rótulo nos pares contrafactuais | 0/4; amplitude máxima de score = 0 |

O único erro no teste envolve “sem dificuldade para respirar”, previsto como alto risco apesar do rótulo baixo. Três de quatro negações no conjunto adicional também falharam. Isso é coerente com o uso superficial de expressões frequentes, sem compreensão semântica. Um caso coloquial de coceira também foi classificado incorretamente.

O extrator e o classificador são componentes independentes. No exemplo “Nego dor no peito e nego falta de ar; apenas coceira leve na pele”, as regras registram as negações e não sugerem hipóteses; a regressão prevê alto risco. A demonstração preserva essa contradição para análise, sem ocultar o erro.

Não houve mudanças nos pares demográficos, mas os atributos são quase ausentes do treino: o resultado não demonstra justiça. A base artificial incorpora as escolhas de redação e rotulagem de seus criadores. Sintomas atípicos, diferentes registros linguísticos e grupos populacionais não estão adequadamente representados. Scores não são probabilidades clínicas calibradas.

![Matriz de confusão](../results/matriz_confusao.png)

### 4.2. Feedback dos usuários

Não houve avaliação com usuários finais nem especialistas clínicos. Foram executados seis testes de extração, o classificador completo e o notebook em kernel limpo. A interface local foi exercitada com uma frase de alerta, uma frase leve e uma frase negada. Isso verifica funcionamento técnico, não utilidade clínica.

## 5. Conclusões e trabalhos futuros

A solução atende às duas partes técnicas obrigatórias: arquivos estruturados, extração, TF-IDF, classificador e avaliação reproduzível. A queda de desempenho nos desafios revela a limitação central do experimento: correlações lexicais em uma base artificial não constituem raciocínio diagnóstico.

Antes de qualquer aplicação real seriam necessários dados autorizados e desidentificados, revisão dos rótulos por profissionais, divisão por paciente/instituição, validação externa, testes de calibração e desempenho por grupos, avaliação prospectiva e supervisão humana. Nenhuma dessas etapas clínicas é alegada nesta entrega.

Publicação aprovada pelo integrante em 07/10/2026. Repositório: https://github.com/omninc/grupo-100-cardioia-fase2. Vídeo não listado: https://youtu.be/NkU1Qqp_IdA. Professora indicada para colaboração: [Sabrina Otoni](https://github.com/SabrinaOtoni).

## 6. Referências

- FIAP. [Template oficial indicado](https://github.com/agodoi/templateFiapVfinal). Estrutura e atribuição mantidas; seções preenchidas e adaptadas à Fase 2.
- scikit-learn. [Feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html).
- scikit-learn. [Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html).
- NHLBI. [Heart attack symptoms](https://www.nhlbi.nih.gov/health/heart-attack/symptoms).
- NHLBI. [Heart failure symptoms](https://www.nhlbi.nih.gov/health/heart-failure/symptoms).
- NHLBI. [Arrhythmias symptoms](https://www.nhlbi.nih.gov/health/arrhythmias/symptoms).
- NHLBI. [Coronary heart disease symptoms](https://www.nhlbi.nih.gov/health/coronary-heart-disease/symptoms).

Acesso em 07/10/2026. As fontes médicas sustentam associações gerais; os rótulos deste experimento não foram extraídos ou validados por elas.

## Anexos

Notebook executado em `notebooks/`, tabelas e JSON em `results/`, dados em `data/`, vídeo local separado para revisão e [checklist](checklist_entrega.md). O vídeo é uma montagem de capturas da execução local com explicações textuais, com duração de três minutos.
