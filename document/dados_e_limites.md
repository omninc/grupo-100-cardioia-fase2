# Dados, rótulos e limites

## Proveniência

Todos os relatos são fictícios e foram preparados para esta atividade com assistência de IA. Não provêm de prontuários nem contêm dados de pacientes reais. A base textual foi criada especificamente para a Fase 2, conforme a orientação detalhada para uma base simulada; não se afirma reutilização de um dataset da Fase 1.

`relatos.txt`: 10 linhas, cada uma com sintoma, início e impacto na rotina. O décimo caso combina um sintoma presente e outro negado. Casos sem correspondência são verificados nos testes e na demonstração, sem forçar uma doença para todo relato.

`mapa_conhecimento.csv`: 9 associações, duas expressões por linha. Uma expressão pode levar a mais de uma hipótese, intencionalmente. As colunas de fonte e observação deixam explícitos o fundamento geral e a inespecificidade. As fontes não foram usadas para extrair registros ou copiar uma base.

`frases_rotuladas.csv`: 80 frases, 40 de cada classe, sem duplicatas exatas. Rótulos didáticos: combinações de sintomas descritas como intensas/persistentes ou limitantes são “alto risco”; incômodos leves/localizados, com melhora ou rotina preservada, são “baixo risco”. Esse critério simplifica excessivamente a realidade. Sintomas leves também podem ser importantes, portanto o rótulo não autoriza decisões clínicas.

`desafios_linguisticos.csv`: 12 casos reservados para análise de negação (4), negação mista (2), registro coloquial (4) e temporalidade (2). Não entram no treinamento ou na escolha de parâmetros. Os testes contrafactuais acrescentam 16 frases a partir de quatro bases e variam apenas gênero/idade.

## Protocolo

Divisão estratificada 75/25 com semente 42: 60 treino e 20 teste. Não há duplicatas textuais, mas existem padrões lexicais semelhantes entre partições. Não se trata de validação por paciente, instituição ou período. A Pipeline aprende vocabulário e IDF exclusivamente no treino. O CSV `results/particoes.csv` torna a divisão auditável. Hiperparâmetros fixos em `config/modelo.json`; não houve seleção por desempenho no teste.

## Limitações e governança

- O extrator usa expressões exatas após normalização: erros de grafia e sinônimos ausentes podem não ser reconhecidos.
- A negação é limitada a seis palavras anteriores dentro de uma cláusula. Não interpreta relações clínicas, hipótese, história familiar, sujeito ou temporalidade.
- A regressão logística usa padrões de palavras, sem compreender fisiologia. Palavras “forte”, “leve”, “melhora” podem virar atalhos artificiais.
- Dados pequenos, equilibrados e artificiais não reproduzem a prevalência nem a diversidade da população. Acurácia não é evidência de segurança.
- Ausência de mudança nos pares demográficos não comprova equidade: esses atributos são praticamente desconhecidos no treino.
- Não há revisão clínica dos rótulos, calibração, avaliação prospectiva, feedback de usuários ou validação externa.
- Não usar para atendimento, priorização de pacientes, diagnóstico, tratamento ou tranquilização de pessoas.

Para evoluir: consentimento/base legal e proteção de dados, anotação clínica independente, conjunto externo, divisão por paciente, avaliação por subgrupos, testes de linguagem e supervisão profissional.
