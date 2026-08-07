import json
import tempfile
import unittest
from pathlib import Path

from estacionamento import Estacionamento


class PersistenciaTests(unittest.TestCase):
    def test_json_persiste_e_recupera_clientes(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            caminho = Path(tmp_dir) / "estacionamento.json"
            estacionamento = Estacionamento(storage_type="json", storage_path=str(caminho))
            estacionamento.cadastrar_cliente(
                tipo="mensalista",
                nome="Maria Silva",
                placa="MSS9A99",
                telefone="11912345678",
                valor_mensal=300.0,
            )
            estacionamento.salvar()

            novo_estacionamento = Estacionamento(storage_type="json", storage_path=str(caminho))
            novo_estacionamento.carregar()

            self.assertEqual(len(novo_estacionamento.clientes), 1)
            self.assertEqual(novo_estacionamento.clientes[0]["nome"], "Maria Silva")
            self.assertEqual(novo_estacionamento.clientes[0]["placa"], "MSS9A99")

            with caminho.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.assertEqual(dados["clientes"][0]["nome"], "Maria Silva")


if __name__ == "__main__":
    unittest.main()
