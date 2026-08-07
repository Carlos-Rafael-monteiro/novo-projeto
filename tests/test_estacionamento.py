import unittest

from estacionamento import Estacionamento


class EstacionamentoTests(unittest.TestCase):
    def setUp(self):
        self.estacionamento = Estacionamento()

    def test_cadastrar_mensalista(self):
        cliente = self.estacionamento.cadastrar_cliente(
            tipo="mensalista",
            nome="Ana Souza",
            placa="ABC1D23",
            telefone="11999990000",
            valor_mensal=250.0,
        )

        self.assertEqual(cliente["tipo"], "mensalista")
        self.assertEqual(cliente["nome"], "Ana Souza")
        self.assertEqual(cliente["placa"], "ABC1D23")
        self.assertEqual(cliente["valor_mensal"], 250.0)

    def test_listar_por_tipo(self):
        self.estacionamento.cadastrar_cliente(
            tipo="credenciado",
            nome="Bruno Lima",
            placa="XYZ4E56",
            telefone="11888887777",
            codigo_acesso="C-100",
        )
        self.estacionamento.cadastrar_cliente(
            tipo="avulso",
            nome="Carla Dias",
            placa="QWE7R89",
            telefone="11777776666",
        )

        credenciados = self.estacionamento.listar_clientes("credenciado")
        avulsos = self.estacionamento.listar_clientes("avulso")

        self.assertEqual(len(credenciados), 1)
        self.assertEqual(len(avulsos), 1)
        self.assertEqual(credenciados[0]["codigo_acesso"], "C-100")

    def test_buscar_por_placa(self):
        self.estacionamento.cadastrar_cliente(
            tipo="avulso",
            nome="Davi Rocha",
            placa="LMN2P34",
            telefone="11666665555",
        )

        encontrado = self.estacionamento.buscar_por_placa("LMN2P34")

        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado["nome"], "Davi Rocha")


if __name__ == "__main__":
    unittest.main()
