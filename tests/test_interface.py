import unittest
import tkinter as tk
from unittest import mock

from interface import ControleWindow, InterfaceEstacionamento, TelaLogin


class InterfaceTests(unittest.TestCase):
    def test_tela_login_ativa_com_parent_oculto(self) -> None:
        root = tk.Tk()
        root.withdraw()
        try:
            login = TelaLogin(root, lambda *_args: True)
            self.assertTrue(login.root.winfo_exists())
            self.assertTrue(login.root.winfo_viewable())
        finally:
            if root.winfo_exists():
                root.destroy()

    def test_interface_possui_botoes_para_cadastro_e_controle(self) -> None:
        root = tk.Tk()
        root.withdraw()
        try:
            interface = InterfaceEstacionamento(root)
            botoes = []
            pilha = list(interface.root.winfo_children())
            while pilha:
                widget = pilha.pop()
                if isinstance(widget, tk.Button):
                    botoes.append(widget.cget("text"))
                pilha.extend(widget.winfo_children())
            self.assertIn("Cadastro de clientes", botoes)
            self.assertIn("Registro de entrada/saída", botoes)
        finally:
            if root.winfo_exists():
                root.destroy()

    def test_confirmar_movimento_registra_entrada_quando_placa_nao_esta_no_patio(self) -> None:
        root = tk.Tk()
        root.withdraw()
        try:
            interface = InterfaceEstacionamento(root)
            controle = ControleWindow(root, interface)
            controle.placa_mov_var.set("ABC1234")
            controle.estacionamento.movimentacoes = []
            controle.registrar_entrada = mock.Mock()
            controle.registrar_saida = mock.Mock()

            controle.confirmar_movimento()

            controle.registrar_entrada.assert_called_once()
            controle.registrar_saida.assert_not_called()
        finally:
            if root.winfo_exists():
                root.destroy()

    def test_confirmar_movimento_registra_saida_quando_placa_esta_no_patio(self) -> None:
        root = tk.Tk()
        root.withdraw()
        try:
            interface = InterfaceEstacionamento(root)
            controle = ControleWindow(root, interface)
            controle.placa_mov_var.set("ABC1234")
            controle.estacionamento.movimentacoes = [{"placa": "ABC1234", "status": "ativo"}]
            controle.registrar_entrada = mock.Mock()
            controle.registrar_saida = mock.Mock()

            controle.confirmar_movimento()

            controle.registrar_saida.assert_called_once()
            controle.registrar_entrada.assert_not_called()
        finally:
            if root.winfo_exists():
                root.destroy()

    def test_registrar_entrada_reprograma_foco_no_campo_de_placa(self) -> None:
        root = tk.Tk()
        root.withdraw()
        try:
            interface = InterfaceEstacionamento(root)
            controle = ControleWindow(root, interface)
            controle.placa_mov_var.set("ABC1234")

            with mock.patch.object(controle, "after") as after_mock, mock.patch("interface.messagebox.showinfo"):
                controle.registrar_entrada()

            after_mock.assert_called_once()
        finally:
            if root.winfo_exists():
                root.destroy()


if __name__ == "__main__":
    unittest.main()
