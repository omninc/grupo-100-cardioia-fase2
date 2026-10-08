"""Experimento reproduzível de classificação de texto sintético."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

ROOT = Path(__file__).resolve().parents[1]
LABELS = ['baixo risco', 'alto risco']


def executar():
    cfg = json.loads((ROOT / 'config/modelo.json').read_text())
    df = pd.read_csv(ROOT / 'data/frases_rotuladas.csv')
    assert list(df.columns) == ['frase', 'situacao']
    assert not df.isna().any().any() and df.frase.is_unique
    assert set(df.situacao) == set(LABELS)
    treino, teste = train_test_split(df.index, test_size=cfg['test_size'],
                                   stratify=df.situacao, random_state=cfg['random_state'])
    # O vocabulário e o IDF são aprendidos APENAS no treino.
    modelo = Pipeline([
        ('tfidf', TfidfVectorizer(strip_accents='unicode', lowercase=True,
                                 ngram_range=tuple(cfg['ngram_range']), sublinear_tf=True)),
        ('classificador', LogisticRegression(C=cfg['C'], max_iter=cfg['max_iter'],
                                            random_state=cfg['random_state']))])
    modelo.fit(df.loc[treino, 'frase'], df.loc[treino, 'situacao'])
    pred = modelo.predict(df.loc[teste, 'frase'])
    baseline = DummyClassifier(strategy='most_frequent').fit(df.loc[treino, 'frase'], df.loc[treino, 'situacao'])
    metrics = {'n_total': len(df), 'n_treino': len(treino), 'n_teste': len(teste),
               'acuracia': accuracy_score(df.loc[teste, 'situacao'], pred),
               'acuracia_baseline': accuracy_score(df.loc[teste, 'situacao'], baseline.predict(df.loc[teste, 'frase'])),
               'relatorio': classification_report(df.loc[teste, 'situacao'], pred, labels=LABELS, output_dict=True, zero_division=0),
               'matriz_confusao': confusion_matrix(df.loc[teste, 'situacao'], pred, labels=LABELS).tolist(),
               'ordem_classes_matriz': LABELS, 'config': cfg}
    out = ROOT / 'results'
    out.mkdir(exist_ok=True)
    aval = df.loc[teste].copy()
    aval.insert(0, 'linha_csv', teste + 2)
    aval['predicao'] = pred
    aval['acerto'] = aval.situacao == aval.predicao
    aval.to_csv(out / 'predicoes_teste.csv', index=False)
    split = df.copy()
    split['particao'] = ['treino' if i in treino else 'teste' for i in df.index]
    split.to_csv(out / 'particoes.csv', index=False)
    desafios = pd.read_csv(ROOT / 'data/desafios_linguisticos.csv')
    desafios['predicao'] = modelo.predict(desafios.frase)
    desafios['acerto'] = desafios.situacao == desafios.predicao
    desafios.to_csv(out / 'desafios_linguisticos.csv', index=False)
    metrics['desafios_acuracia'] = float(desafios.acerto.mean())
    metrics['desafios_por_categoria'] = desafios.groupby('categoria').acerto.agg(['mean', 'count']).to_dict('index')
    # Pares contrafactuais: muda só a apresentação demográfica, não o sintoma.
    bases = ['Sinto pressão forte no peito e suor frio.', 'Tenho leve coceira no braço após usar roupa nova.',
             'Meu coração dispara e quase desmaiei.', 'Sinto dor discreta nas costas após treino e já melhorei.']
    pares = []
    for n, base in enumerate(bases, 1):
        for atributo in ['Sou mulher de 30 anos.', 'Sou homem de 30 anos.', 'Sou mulher de 70 anos.', 'Sou homem de 70 anos.']:
            frase = atributo + ' ' + base
            prob = modelo.predict_proba([frase])[0]
            i = list(modelo.classes_).index('alto risco')
            pares.append({'par': n, 'frase': frase, 'predicao': modelo.predict([frase])[0], 'score_alto_risco': float(prob[i])})
    contrafactual = pd.DataFrame(pares)
    contrafactual.to_csv(out / 'contrafactuais.csv', index=False)
    metrics['pares_com_mudanca_rotulo'] = int((contrafactual.groupby('par').predicao.nunique() > 1).sum())
    metrics['maior_variacao_score_pares'] = float(contrafactual.groupby('par').score_alto_risco.agg(lambda x: x.max() - x.min()).max())
    vocab = modelo['tfidf'].get_feature_names_out()
    coef = modelo['classificador'].coef_[0]
    # coef positivo favorece classes_[1] (ordem alfabética: baixo risco).
    termos = pd.DataFrame({'termo': vocab, 'coeficiente': coef}).sort_values('coeficiente')
    pd.concat([termos.head(12), termos.tail(12)]).to_csv(out / 'termos_influentes.csv', index=False)
    metrics['classe_coeficiente_positivo'] = modelo.classes_[1]
    (out / 'metricas.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
    fig, ax = plt.subplots(figsize=(7, 5))
    ConfusionMatrixDisplay.from_predictions(df.loc[teste, 'situacao'], pred, labels=LABELS, cmap='Blues', colorbar=False, ax=ax)
    ax.set(title='CardioIA — teste sintético (n=20)', xlabel='Classe prevista', ylabel='Rótulo didático')
    fig.tight_layout()
    fig.savefig(out / 'matriz_confusao.png', dpi=160)
    plt.close(fig)
    return modelo, df, aval, desafios, metrics


if __name__ == '__main__':
    _, _, aval, desafios, metrics = executar()
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print('\nErros no conjunto de desafio (não usado no treinamento):')
    print(desafios.loc[~desafios.acerto].to_string(index=False))
