import unittest

from estacionamento import Estacionamento


class NovasFuncionalidadesTests(unittest.TestCase):
    def test_login_com_credenciais_validas(self):
        estacionamento = Estacionamento(users={"admin": "admin123"})
        self.assertTrue(estacionamento.autenticar_usuario("admin", "admin123"))
        self.assertFalse(estacionamento.autenticar_usuario("admin", "senhaerrada"))

    def test_registrar_entrada_e_saida(self):
        estacionamento = Estacionamento()
        entrada = estacionamento.registrar_entrada("ABC9Z99")
        self.assertEqual(entrada["status"], "ativo")
        self.assertEqual(len(estacionamento.listar_movimentacoes_ativas()), 1)

        saida = estacionamento.registrar_saida("ABC9Z99")
        self.assertEqual(saida["status"], "finalizado")
        self.assertEqual(len(estacionamento.listar_movimentacoes_ativas()), 0)

    def test_tarifas_por_tipo_de_veiculo(self):
        estacionamento = Estacionamento()
        estacionamento.definir_tarifa("carro", 15.0)
        estacionamento.definir_tarifa("moto", 8.0)

        self.assertEqual(estacionamento.obter_tarifa("carro"), 15.0)
        self.assertEqual(estacionamento.obter_tarifa("moto"), 8.0)

    def test_painel_de_ocupacao(self):
        estacionamento = Estacionamento(capacidade=3)
        estacionamento.registrar_entrada("AAA1")
        estacionamento.registrar_entrada("BBB2")

        painel = estacionamento.obter_painel_ocupacao()
        self.assertEqual(painel["ocupadas"], 2)
        self.assertEqual(painel["livres"], 1)
        self.assertEqual(painel["percentual"], 66.7)

    def test_registrar_saida_avulso_calcula_cobranca(self):
        estacionamento = Estacionamento()
        estacionamento.definir_tarifa("carro", 15.0)
        estacionamento.registrar_entrada("XYZ9999")

        saida = estacionamento.registrar_saida("XYZ9999", forma_pagamento="pix")

        self.assertEqual(saida["status"], "finalizado")
        self.assertEqual(saida["tipo_cliente"], "avulso")
        self.assertEqual(saida["valor_total"], 15.0)
        self.assertEqual(saida["forma_pagamento"], "pix")

    def test_registrar_saida_cadastrado_nao_cobra(self):
        estacionamento = Estacionamento()
        estacionamento.cadastrar_cliente("mensalista", "Ana", "ABC1234", "99999")
        estacionamento.registrar_entrada("ABC1234")

        saida = estacionamento.registrar_saida("ABC1234")

        self.assertEqual(saida["tipo_cliente"], "cadastrado")
        self.assertEqual(saida["valor_total"], 0.0)


if __name__ == "__main__":
    unittest.main()
