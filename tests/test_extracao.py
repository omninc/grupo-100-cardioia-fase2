import unittest
from src.extracao import extrair, carregar_mapa, executar


class ExtracaoTest(unittest.TestCase):
    def setUp(self):
        self.mapa = carregar_mapa()

    def test_dez_relatos(self):
        self.assertEqual(len(executar()), 10)

    def test_negacao_e_adversativa(self):
        r = extrair('NÃO sinto dor no peito, mas tenho falta de ar.', self.mapa)
        self.assertNotIn('dor no peito', r['sintomas_presentes'])
        self.assertIn('dor no peito', r['sintomas_negados'])
        self.assertIn('falta de ar', r['sintomas_presentes'])

    def test_negacao_coordenada(self):
        r = extrair('Sem dor no peito nem falta de ar.', self.mapa)
        self.assertEqual(r['sintomas_presentes'], [])

    def test_limite_de_palavra(self):
        self.assertEqual(extrair('Sinto fadigado.', self.mapa)['sintomas_presentes'], [])

    def test_sem_correspondencia(self):
        self.assertEqual(extrair('Coceira leve na pele.', self.mapa)['hipoteses_educacionais'], [])

    def test_sobreposicao_explicita(self):
        self.assertEqual(len(extrair('Dor no peito.', self.mapa)['hipoteses_educacionais']), 2)


if __name__ == '__main__':
    unittest.main()
