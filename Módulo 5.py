import csv
from datetime import datetime

class LojaAcademia:
    def __init__(self):
        self.produtos = []
        self.clientes = {}
        self.entregas = {}
        self.pontos_fidelidade = {}

    def carregar_produtos(self):
        with open('produtos.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.produtos.append({
                    'nome': row['nome'],
                    'preco': float(row['preco']),
                    'tamanhos': row['tamanhos'].split(',')
                })

    def cadastrar_cliente(self, nome):
        if nome not in self.clientes:
            self.clientes[nome] = {'historico_compras': []}
            self.pontos_fidelidade[nome] = 0

    def cadastrar_produto(self, nome, preco, tamanhos):
        self.produtos.append({
            'nome': nome,
            'preco': float(preco),
            'tamanhos': tamanhos.split(',')
        })
        print(f"Produto {nome} cadastrado com sucesso.")

    def comprar_produto(self, cliente, produto_index, tamanho):
        produto = self.produtos[produto_index]
        if tamanho in produto['tamanhos']:
            valor = produto['preco']
            compra = {'produto': produto['nome'], 'preco': valor, 'tamanho': tamanho, 'data': datetime.now()}
            self.clientes[cliente]['historico_compras'].append(compra)
            self.pontos_fidelidade[cliente] += int(valor)

            print(f"Produto {produto['nome']} comprado com sucesso.")
        else:
            print(f"Tamanho {tamanho} indisponível para o produto {produto['nome']}.")

    def avaliar_produto(self, cliente, produto_index, avaliacao):
        produto = self.produtos[produto_index]
        print(f"Cliente {cliente} avaliou o produto {produto['nome']} com nota {avaliacao}.")

    def realizar_entrega(self, cliente, endereco):
        entrega = {'cliente': cliente, 'endereco': endereco, 'status': 'Em andamento'}
        self.entregas[cliente] = entrega
        print(f"Entrega para {cliente} em andamento para o endereço {endereco}.")

    def exibir_historico_compras(self, cliente):
        historico = self.clientes[cliente]['historico_compras']
        print(f"Histórico de compras para {cliente}:")
        for compra in historico:
            print(f"{compra['data']}: {compra['produto']} - R${compra['preco']} - Tamanho: {compra['tamanho']}")

    def exibir_pontos_fidelidade(self, cliente):
        pontos = self.pontos_fidelidade[cliente]
        print(f"Cliente {cliente} possui {pontos} pontos de fidelidade.")

    def exibir_menu(self):
        print("1. Cadastrar Produto")
        print("2. Comprar Produto")
        print("3. Avaliar Produto")
        print("4. Realizar Entrega")
        print("5. Exibir Histórico de Compras")
        print("6. Exibir Pontos de Fidelidade")
        print("0. Sair")

    def executar_menu(self):
        while True:
            self.exibir_menu()
            escolha = input("Escolha uma opção (0-6): ")

            if escolha == "0":
                print("Saindo do programa. Até mais!")
                break
            elif escolha == "1":
                nome_produto = input("Digite o nome do produto: ")
                preco_produto = input("Digite o preço do produto: ")
                tamanhos_produto = input("Digite os tamanhos disponíveis, separados por vírgula: ")
                self.cadastrar_produto(nome_produto, preco_produto, tamanhos_produto)
            elif escolha == "2":
                nome_cliente = input("Digite o nome do cliente: ")
                produto_index = int(input("Digite o índice do produto a ser comprado: "))
                tamanho_compra = input("Digite o tamanho do produto: ")
                self.comprar_produto(nome_cliente, produto_index, tamanho_compra)
            elif escolha == "3":
                nome_cliente = input("Digite o nome do cliente: ")
                produto_index = int(input("Digite o índice do produto a ser avaliado: "))
                avaliacao = int(input("Digite a avaliação do produto (de 1 a 5): "))
                self.avaliar_produto(nome_cliente, produto_index, avaliacao)
            elif escolha == "4":
                nome_cliente = input("Digite o nome do cliente: ")
                endereco_entrega = input("Digite o endereço de entrega: ")
                self.realizar_entrega(nome_cliente, endereco_entrega)
            elif escolha == "5":
                nome_cliente = input("Digite o nome do cliente: ")
                self.exibir_historico_compras(nome_cliente)
            elif escolha == "6":
                nome_cliente = input("Digite o nome do cliente: ")
                self.exibir_pontos_fidelidade(nome_cliente)
            else:
                print("Opção inválida. Tente novamente.")

loja = LojaAcademia()
loja.carregar_produtos()
loja.executar_menu()
