from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    import mysql.connector as mysql_connector  # type: ignore
except Exception:  # pragma: no cover - depende do ambiente
    mysql_connector = None  # type: ignore


class Estacionamento:
    """Classe central com a regra de negócio do estacionamento."""

    @staticmethod
    def normalizar_placa(placa: str) -> str:
        """Padroniza a placa para evitar duplicidades entre formatos antigos e Mercosul."""
        texto = placa.strip().upper().replace("-", "")
        texto = "".join(ch for ch in texto if ch.isalnum())
        if len(texto) == 7 and texto[:3].isalpha() and texto[3:7].isdigit():
            return f"{texto[:3]}-{texto[3:7]}"
        if len(texto) == 8 and texto[:4].isalpha() and texto[4:8].isdigit():
            return f"{texto[:4]}-{texto[4:8]}"
        if len(texto) == 7 and texto[:4].isdigit() and texto[4:7].isalpha():
            return f"{texto[:4]}-{texto[4:7]}"
        if len(texto) == 8 and texto[:4].isalpha() and texto[4:8].isalnum() and texto[4:5].isdigit() and texto[5:8].isalpha():
            return f"{texto[:4]}-{texto[4:8]}"
        return texto

    def __init__(
        self,
        storage_type: str = "json",
        storage_path: Optional[str] = None,
        mysql_config: Optional[Dict[str, str]] = None,
        users: Optional[Dict[str, str]] = None,
        capacidade: Optional[int] = None,
    ) -> None:
        # Lista de clientes cadastrados, como mensalistas, credenciados e avulsos.
        self.clientes: List[Dict[str, object]] = []
        # Registros ativos e finalizados de entradas e saídas de veículos.
        self.movimentacoes: List[Dict[str, object]] = []
        self.tarifas: Dict[str, float] = {}
        # Capacidade total do estacionamento para o painel de ocupação.
        self.capacidade: int = capacidade or int(os.getenv("ESTACIONAMENTO_CAPACIDADE", "50"))
        self.storage_type = storage_type.lower()
        # Configurações para persistência em JSON ou MySQL, conforme a escolha do ambiente.
        self.storage_path = storage_path or os.getenv("ESTACIONAMENTO_JSON_PATH", "estacionamento.json")
        self.mysql_config = mysql_config or {
            "host": os.getenv("ESTACIONAMENTO_DB_HOST", "localhost"),
            "user": os.getenv("ESTACIONAMENTO_DB_USER", "root"),
            "password": os.getenv("ESTACIONAMENTO_DB_PASSWORD", ""),
            "database": os.getenv("ESTACIONAMENTO_DB_NAME", "estacionamento"),
        }
        self.users = users or {
            "admin": {"senha": "admin123", "perfil": "administrador"},
            "operador": {"senha": "operador123", "perfil": "operador"},
        }

    def cadastrar_cliente(
        self,
        tipo: str,
        nome: str,
        placa: str,
        telefone: str,
        valor_mensal: Optional[float] = None,
        codigo_acesso: Optional[str] = None,
    ) -> Dict[str, object]:
        placa_normalizada = self.normalizar_placa(placa)
        if self.buscar_por_placa(placa_normalizada):
            raise ValueError("Já existe um cliente cadastrado com esta placa")

        cliente: Dict[str, object] = {
            "tipo": tipo,
            "nome": nome,
            "placa": placa_normalizada,
            "telefone": telefone,
        }

        if tipo == "mensalista":
            cliente["valor_mensal"] = valor_mensal if valor_mensal is not None else 0.0
        elif tipo == "credenciado":
            cliente["codigo_acesso"] = codigo_acesso or ""
        elif tipo == "avulso":
            cliente["valor_hora"] = 10.0
        else:
            raise ValueError("Tipo de cliente inválido")

        self.clientes.append(cliente)
        return cliente

    def listar_clientes(self, tipo: Optional[str] = None) -> List[Dict[str, object]]:
        """Retorna os clientes cadastrados, opcionalmente filtrados por tipo."""
        if tipo is None:
            return list(self.clientes)
        return [cliente for cliente in self.clientes if cliente.get("tipo") == tipo]

    def buscar_por_placa(self, placa: str) -> Optional[Dict[str, object]]:
        """Procura um cliente cadastrado pela placa normalizada."""
        placa_normalizada = self.normalizar_placa(placa)
        for cliente in self.clientes:
            if self.normalizar_placa(str(cliente.get("placa", ""))) == placa_normalizada:
                return cliente
        return None

    def remover_cliente(self, placa: str) -> bool:
        """Remove um cliente da lista usando a placa como referência."""
        placa_normalizada = self.normalizar_placa(placa)
        for indice, cliente in enumerate(self.clientes):
            if self.normalizar_placa(str(cliente.get("placa", ""))) == placa_normalizada:
                del self.clientes[indice]
                return True
        return False

    def autenticar_usuario(self, usuario: str, senha: str) -> bool:
        """Valida as credenciais de acesso do operador do sistema."""
        credencial = self.users.get(usuario)
        if isinstance(credencial, dict):
            return credencial.get("senha") == senha
        return credencial == senha

    def obter_perfil_usuario(self, usuario: str) -> Optional[str]:
        """Retorna o perfil do usuário autenticado, se existir."""
        credencial = self.users.get(usuario)
        if isinstance(credencial, dict):
            return credencial.get("perfil")
        return None

    def listar_usuarios(self) -> List[Dict[str, str]]:
        """Retorna a lista de usuários com perfil e nome de usuário."""
        usuarios = []
        for nome, dados in self.users.items():
            if isinstance(dados, dict):
                usuarios.append({"usuario": nome, "perfil": dados.get("perfil", "")})
            else:
                usuarios.append({"usuario": nome, "perfil": "desconhecido"})
        return usuarios

    def registrar_entrada(self, placa: str) -> Dict[str, object]:
        """Cria um novo movimento de entrada com a hora atual."""
        placa_normalizada = self.normalizar_placa(placa)
        movimento = {
            "placa": placa_normalizada,
            "entrada": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "ativo",
        }
        self.movimentacoes.append(movimento)
        return movimento

    def registrar_saida(self, placa: str, forma_pagamento: Optional[str] = None) -> Dict[str, object]:
        """Fecha um movimento ativo e calcula o valor, se necessário para avulsos."""
        placa_normalizada = self.normalizar_placa(placa)
        for movimento in self.movimentacoes:
            if self.normalizar_placa(str(movimento.get("placa", ""))) == placa_normalizada and movimento.get("status") == "ativo":
                cliente = self.buscar_por_placa(placa_normalizada)
                tipo_cliente = "cadastrado" if cliente is not None else "avulso"
                valor_total = 0.0

                if tipo_cliente == "avulso":
                    tarifa = self.obter_tarifa("carro")
                    valor_total = float(tarifa if tarifa else 0.0)

                movimento["saida"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                movimento["status"] = "finalizado"
                movimento["tipo_cliente"] = tipo_cliente
                movimento["valor_total"] = valor_total
                movimento["forma_pagamento"] = forma_pagamento or ""
                return movimento
        raise ValueError("Nenhuma entrada ativa encontrada para esta placa")

    def listar_movimentacoes_ativas(self) -> List[Dict[str, object]]:
        """Retorna apenas os veículos que ainda estão dentro do pátio."""
        return [mov for mov in self.movimentacoes if mov.get("status") == "ativo"]

    def definir_tarifa(self, tipo_veiculo: str, valor: float) -> None:
        """Define o valor cobrado para um tipo de veículo."""
        self.tarifas[tipo_veiculo.lower()] = float(valor)

    def obter_tarifa(self, tipo_veiculo: str) -> float:
        """Recupera a tarifa configurada para um tipo de veículo."""
        return self.tarifas.get(tipo_veiculo.lower(), 0.0)

    def obter_painel_ocupacao(self) -> Dict[str, float]:
        """Calcula a ocupação atual do estacionamento para exibição no painel."""
        ocupadas = len(self.listar_movimentacoes_ativas())
        livres = max(self.capacidade - ocupadas, 0)
        percentual = round((ocupadas / self.capacidade) * 100, 1) if self.capacidade else 0.0
        return {"ocupadas": ocupadas, "livres": livres, "percentual": percentual}

    def salvar(self) -> None:
        """Persiste os dados atuais em JSON ou MySQL, conforme a configuração."""
        if self.storage_type == "json":
            caminho = Path(self.storage_path)
            payload = {
                "clientes": self.clientes,
                "movimentacoes": self.movimentacoes,
                "tarifas": self.tarifas,
                "capacidade": self.capacidade,
            }
            caminho.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        elif self.storage_type == "mysql":
            self._salvar_mysql()
        else:
            raise ValueError("Tipo de armazenamento inválido")

    def carregar(self) -> None:
        """Carrega os dados salvos no armazenamento selecionado."""
        if self.storage_type == "json":
            caminho = Path(self.storage_path)
            if caminho.exists():
                dados = json.loads(caminho.read_text(encoding="utf-8"))
                if isinstance(dados, dict):
                    self.clientes = dados.get("clientes", [])
                    self.movimentacoes = dados.get("movimentacoes", [])
                    self.tarifas = dados.get("tarifas", {})
                    self.capacidade = int(dados.get("capacidade", self.capacidade))
                else:
                    self.clientes = dados
                    self.movimentacoes = []
                    self.tarifas = {}
                    self.capacidade = int(os.getenv("ESTACIONAMENTO_CAPACIDADE", "50"))
            else:
                self.clientes = []
                self.movimentacoes = []
                self.tarifas = {}
                self.capacidade = int(os.getenv("ESTACIONAMENTO_CAPACIDADE", "50"))
        elif self.storage_type == "mysql":
            self._carregar_mysql()
        else:
            raise ValueError("Tipo de armazenamento inválido")

    def _salvar_mysql(self) -> None:
        """Salva os dados em tabelas MySQL para uso com banco real."""
        if mysql_connector is None:
            raise RuntimeError("mysql-connector-python não está instalado")

        conexao = mysql_connector.connect(**self.mysql_config, autocommit=True)
        cursor = conexao.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % self.mysql_config["database"])
        cursor.execute("USE %s" % self.mysql_config["database"])
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS clientes ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "tipo VARCHAR(50), "
            "nome VARCHAR(255), "
            "placa VARCHAR(20), "
            "telefone VARCHAR(20), "
            "valor_mensal FLOAT, "
            "codigo_acesso VARCHAR(50), "
            "valor_hora FLOAT)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS movimentacoes ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "placa VARCHAR(20), "
            "entrada VARCHAR(50), "
            "saida VARCHAR(50), "
            "status VARCHAR(20))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS tarifas ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "tipo_veiculo VARCHAR(50), "
            "valor FLOAT)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS configuracoes ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "chave VARCHAR(50), "
            "valor VARCHAR(100))"
        )
        cursor.execute("DELETE FROM clientes")
        cursor.execute("DELETE FROM movimentacoes")
        cursor.execute("DELETE FROM tarifas")
        cursor.execute("DELETE FROM configuracoes")

        for cliente in self.clientes:
            cursor.execute(
                "INSERT INTO clientes (tipo, nome, placa, telefone, valor_mensal, codigo_acesso, valor_hora) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    cliente.get("tipo"),
                    cliente.get("nome"),
                    cliente.get("placa"),
                    cliente.get("telefone"),
                    cliente.get("valor_mensal"),
                    cliente.get("codigo_acesso"),
                    cliente.get("valor_hora"),
                ),
            )

        for movimento in self.movimentacoes:
            cursor.execute(
                "INSERT INTO movimentacoes (placa, entrada, saida, status) VALUES (%s, %s, %s, %s)",
                (
                    movimento.get("placa"),
                    movimento.get("entrada"),
                    movimento.get("saida"),
                    movimento.get("status"),
                ),
            )

        for tipo_veiculo, valor in self.tarifas.items():
            cursor.execute(
                "INSERT INTO tarifas (tipo_veiculo, valor) VALUES (%s, %s)",
                (tipo_veiculo, valor),
            )

        cursor.execute(
            "INSERT INTO configuracoes (chave, valor) VALUES (%s, %s)",
            ("capacidade", str(self.capacidade)),
        )

        cursor.close()
        conexao.close()

    def _carregar_mysql(self) -> None:
        """Carrega os dados a partir de tabelas MySQL."""
        if mysql_connector is None:
            raise RuntimeError("mysql-connector-python não está instalado")

        conexao = mysql_connector.connect(**self.mysql_config)
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("USE %s" % self.mysql_config["database"])
        cursor.execute("SELECT * FROM clientes")
        registros = cursor.fetchall()

        self.clientes = []
        for registro in registros:
            cliente: Dict[str, object] = {
                "tipo": registro.get("tipo"),
                "nome": registro.get("nome"),
                "placa": registro.get("placa"),
                "telefone": registro.get("telefone"),
            }
            if registro.get("valor_mensal") is not None:
                cliente["valor_mensal"] = float(registro["valor_mensal"])
            if registro.get("codigo_acesso") is not None:
                cliente["codigo_acesso"] = registro["codigo_acesso"]
            if registro.get("valor_hora") is not None:
                cliente["valor_hora"] = float(registro["valor_hora"])
            self.clientes.append(cliente)

        cursor.execute("SELECT * FROM movimentacoes")
        registros_movimentos = cursor.fetchall()
        self.movimentacoes = []
        for registro in registros_movimentos:
            movimento: Dict[str, object] = {
                "placa": registro.get("placa"),
                "entrada": registro.get("entrada"),
                "saida": registro.get("saida"),
                "status": registro.get("status"),
            }
            self.movimentacoes.append(movimento)

        cursor.execute("SELECT * FROM tarifas")
        registros_tarifas = cursor.fetchall()
        self.tarifas = {}
        for registro in registros_tarifas:
            self.tarifas[registro.get("tipo_veiculo")] = float(registro.get("valor", 0.0))

        cursor.execute("SELECT * FROM configuracoes")
        registros_configuracoes = cursor.fetchall()
        self.capacidade = int(os.getenv("ESTACIONAMENTO_CAPACIDADE", "50"))
        for registro in registros_configuracoes:
            if registro.get("chave") == "capacidade":
                self.capacidade = int(registro.get("valor", self.capacidade))

        cursor.close()
        conexao.close()
