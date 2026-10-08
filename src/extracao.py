"""Extração lexical explicável; não realiza diagnóstico clínico."""
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalizar(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto.lower())
                   if unicodedata.category(c) != 'Mn')


def extrair(frase, mapa):
    texto = normalizar(frase)
    presentes, negados, hipoteses = set(), set(), {}
    # Reinicia o escopo na pontuação e em adversativas. Não é análise sintática.
    clausulas = re.split(r'[.;,!?]|\b(?:mas|porem|entretanto)\b', texto)
    for linha in mapa:
        encontrados = []
        for coluna in ('sintoma_1', 'sintoma_2'):
            termo = normalizar(linha[coluna])
            for clausula in clausulas:
                for match in re.finditer(r'(?<!\w)' + re.escape(termo) + r'(?!\w)', clausula):
                    antes = clausula[:match.start()]
                    # Negação em até 6 palavras: cobre "não sinto X nem Y".
                    negacao = re.search(r'\b(?:nao|sem|nego|nega|negou|nem)\b(?:\s+\w+){0,6}\s*$', antes)
                    if negacao:
                        negados.add(linha[coluna])
                    else:
                        presentes.add(linha[coluna])
                        encontrados.append(linha[coluna])
        if encontrados:
            hipoteses.setdefault(linha['doenca_associada'], set()).update(encontrados)
    return {'frase': frase, 'sintomas_presentes': sorted(presentes),
            'sintomas_negados': sorted(negados),
            'hipoteses_educacionais': [{'hipotese': h, 'evidencias': sorted(v)}
                                      for h, v in sorted(hipoteses.items())],
            'aviso': 'Associações didáticas, inespecíficas e sem validade diagnóstica. '
                     'Ausência de correspondência não significa ausência de risco.'}


def carregar_mapa(caminho=ROOT / 'data/mapa_conhecimento.csv'):
    with Path(caminho).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def executar(entrada=ROOT / 'data/relatos.txt'):
    mapa = carregar_mapa()
    frases = Path(entrada).read_text(encoding='utf-8').splitlines()
    return [extrair(frase, mapa) for frase in frases if frase.strip()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada', type=Path, default=ROOT / 'data/relatos.txt')
    parser.add_argument('--saida', type=Path, default=ROOT / 'results/extracao.json')
    args = parser.parse_args()
    resultados = executar(args.entrada)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding='utf-8')
    for i, item in enumerate(resultados, 1):
        print(f"{i:02d}. {item['frase']}")
        print('    Sintomas:', ', '.join(item['sintomas_presentes']) or 'não reconhecidos')
        print('    Hipóteses:', '; '.join(h['hipotese'] for h in item['hipoteses_educacionais']) or 'sem correspondência')
