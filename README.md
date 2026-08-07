# Sistema de gerenciamento de estacionamento

Este projeto implementa um sistema completo de estacionamento com uma estrutura organizada em três camadas principais:

- interface gráfica em Tkinter, responsável pela experiência do operador
- módulo de negócio em Python, com as regras de cadastro, entrada, saída e tarifas
- persistência em JSON ou MySQL, para armazenar clientes, movimentações e configurações

- interface gráfica em Tkinter
- login básico
- controle de entrada e saída de veículos
- versão web com Flask
- tarifas configuráveis por tipo de veículo
- painel de ocupação em tempo real
- persistência em JSON e integração com MySQL real

## Funcionalidades

- Cadastro de mensalistas, credenciados e avulsos
- Listagem de clientes em uma interface visual
- Busca por placa
- Remoção de cliente por placa
- Login com usuário e senha
- Registro de entrada e saída de veículos
- Versão web para cadastro de clientes
- Painel com ocupação e vagas livres
- Tarifas para carro, moto e caminhão
- Persistência em arquivo JSON ou MySQL

## Estrutura do projeto

- main.py: ponto de entrada da aplicação desktop
- interface.py: telas de login, cadastro e controle de entrada/saída
- estacionamento.py: regras de negócio e persistência
- app.py: versão web baseada em Flask
- tests/: testes automatizados para validar o funcionamento

## Como executar

### Interface gráfica

```bash
python main.py
```

Usuário padrão para login:
- usuário: `admin`
- senha: `admin123`

O fluxo típico é:
1. fazer login
2. cadastrar clientes ou mensalistas
3. registrar entradas e saídas de veículos
4. acompanhar o painel de ocupação

### Versão web

```bash
python app.py
```

Acesse no navegador:
- http://127.0.0.1:5000/

### Persistência em JSON

O sistema usa JSON por padrão. O arquivo salvo é `estacionamento.json`.

Essa opção é ideal para testes rápidos e execução local sem dependência externa.

### Persistência em MySQL

Para usar MySQL de forma real, instale o pacote:

```bash
pip install mysql-connector-python
```

E configure as variáveis de ambiente:

```bash
set ESTACIONAMENTO_DB_HOST=localhost
set ESTACIONAMENTO_DB_USER=root
set ESTACIONAMENTO_DB_PASSWORD=
set ESTACIONAMENTO_DB_NAME=estacionamento
set ESTACIONAMENTO_STORAGE_TYPE=mysql
```

Se o servidor MySQL estiver disponível, o sistema cria automaticamente o banco e as tabelas necessárias.

Essa opção é útil quando se deseja usar uma base de dados real para produção ou compartilhamento.

## Testes

Para rodar os testes:

```bash
python -m unittest discover -s tests -v
```
