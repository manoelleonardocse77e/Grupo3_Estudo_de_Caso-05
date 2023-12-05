import csv
import requests
from email.mime.text import MIMEText
from datetime import datetime

app_id = 'SUA_APP_ID'
app_key = 'SUA_CHAVE_DE_API'
perfis_nutricionais = {}


def modulo_1():
class SistemaTreino:
    def __init__(self):
        self.alunos = []
        self.avaliacoes = []
        self.mensagens = []
        self.carregar_dados_iniciais()

    def carregar_dados_csv(self):
        try:
            with open('alunos.csv', mode='r') as file:
                reader = csv.DictReader(file)
                self.alunos = list(reader)

            with open('avaliacoes.csv', mode='r') as file:
                reader = csv.DictReader(file)
                self.avaliacoes = list(reader)

            with open('mensagens.csv', mode='r') as file:
                reader = csv.DictReader(file)
                self.mensagens = list(reader)

        except FileNotFoundError:
            print("Arquivos de dados não encontrados. Iniciando com listas vazias.")

    def salvar_dados_csv(self):
        with open('alunos.csv', mode='w', newline='') as file:
            fieldnames = ['nome', 'idade', 'peso', 'altura', 'condicao_medica']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Remover o campo 'mensagens' antes de salvar os dados
            for aluno in self.alunos:
                aluno_data = {key: aluno[key] for key in fieldnames if key in aluno}
                writer.writerow(aluno_data)

        with open('avaliacoes.csv', mode='w', newline='') as file:
            fieldnames = ['aluno', 'tipo_avaliacao', 'data', 'resultado', 'avaliador']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.avaliacoes)

        with open('mensagens.csv', mode='w', newline='') as file:
            fieldnames = ['remetente', 'destinatario', 'mensagem', 'data_envio']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.mensagens)

    def carregar_dados_iniciais(self):
        self.carregar_dados_csv()

    def cadastrar_aluno(self, nome, idade, peso, altura, condicao_medica, meta):
        if len(self.alunos) < 200:
            aluno = {
                'nome': nome,
                'idade': idade,
                'peso': peso,
                'altura': altura,
                'condicao_medica': condicao_medica,
                'metas': {meta: None},
                'historico_avaliacoes': [],
                'mensagens': []
            }
            self.alunos.append(aluno)
            return aluno
        else:
            print("Limite máximo de alunos atingido.")
            return None

    def marcar_avaliacao(self, aluno):
        if 'historico_avaliacoes' not in aluno:
            aluno['historico_avaliacoes'] = []

        print("==== Marcar Avaliação ====")
        avaliador = input("Nome do Avaliador: ")
        tipo_avaliacao = input("Tipo de Avaliação: ")
        data_avaliacao = input("Data da Avaliação (formato AAAA-MM-DD): ")

        avaliacao = {
            'tipo_avaliacao': tipo_avaliacao,
            'data': data_avaliacao,
            'resultado': None
        }

        aluno['historico_avaliacoes'].append(avaliacao)
        print(f"Avaliação marcada com sucesso por {avaliador} em {data_avaliacao}")

    def realizar_avaliacao(self, aluno, tipo_avaliacao, data, resultado, avaliador):
        if 'metas' not in aluno:
            aluno['metas'] = {}
        if 'historico_avaliacoes' not in aluno:
            aluno['historico_avaliacoes'] = []

        aluno['metas'][tipo_avaliacao] = resultado

        avaliacao = {
            'tipo_avaliacao': tipo_avaliacao,
            'data': data,
            'resultado': resultado,
            'avaliador': avaliador
        }

        aluno['historico_avaliacoes'].append(avaliacao)
        self.avaliacoes.append({'aluno': aluno['nome'], **avaliacao})

    def alerta_avaliacao_pendente(self, aluno):
        historico_avaliacoes = aluno.get('historico_avaliacoes', [])
        avaliacoes_pendentes = [avaliacao for avaliacao in historico_avaliacoes if avaliacao['resultado'] is None]

        if avaliacoes_pendentes:
            proxima_avaliacao = avaliacoes_pendentes[0]
            data_proxima_avaliacao = proxima_avaliacao['data']
            print(f"ALERTA: Próxima avaliação em {data_proxima_avaliacao}")
        else:
            print("Sem avaliações pendentes.")

    def enviar_mensagem(self, remetente, destinatario, mensagem):
        if 'mensagens' not in destinatario:
            destinatario['mensagens'] = []

        mensagem = {
            'remetente': remetente,
            'destinatario': destinatario,
            'mensagem': mensagem,
            'data_envio': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        destinatario['mensagens'].append(mensagem)
        self.mensagens.append(mensagem)

    def visualizar_mensagens(self, aluno):
        if 'mensagens' in aluno:
            print(f"=== Mensagens para {aluno['nome']} ===")
            for mensagem in aluno['mensagens']:
                print(f"{mensagem['remetente']} ({mensagem['data_envio']}): {mensagem['mensagem']}")
                print("=-=" * 10)
        else:
            print(f"Não há mensagens para {aluno['nome']}.")

    def gerar_relatorio(self, aluno):
        metas = aluno.get('metas', {})
        relatorio = f"Relatório de Progresso para {aluno['nome']}:\n"
        for tipo_avaliacao, resultado in metas.items():
            relatorio += f"- {tipo_avaliacao}: {resultado}\n"
        return relatorio

    def imprimir_relatorio(self, aluno):
        relatorio_aluno = self.gerar_relatorio(aluno)
        print("=-=" * 10)
        print(relatorio_aluno)
        print("=-=" * 10)

    def imprimir_mensagens_enviadas(self, aluno):
        self.visualizar_mensagens(aluno)

    def imprimir_metas(self, aluno):
        metas = aluno.get('metas', {})
        print(f"Metas para {aluno['nome']}:")
        for tipo_avaliacao, resultado in metas.items():
            print(f"- {tipo_avaliacao}: {resultado}")


  sistema = SistemaTreino()
  sistema.carregar_dados_csv()

  while True:
      print('''==== Menu ====
  [ 1 ] Cadastrar Aluno
  [ 2 ] Aluno Já Cadastrado
  [ 3 ] Sair''')
      escolha = int(input("-> "))

    if escolha == 1:
        print("==== Cadastro de Aluno ====")
        nome = input("Nome: ")

        aluno_existente = next((aluno for aluno in sistema.alunos if aluno['nome'] == nome), None)
        if aluno_existente:
            print(f"Aluno com o nome '{nome}' já cadastrado.")
            continue

        idade = int(input("Idade: "))
        peso = int(input("Peso: "))
        altura = float(input("Altura: "))
        condicao_medica = input("Condição Médica: ")
        meta = input("Meta: ")
        aluno = sistema.cadastrar_aluno(nome, idade, peso, altura, condicao_medica, meta)

        if aluno:
            print(f"Aluno cadastrado com sucesso! Nome: {aluno['nome']}")
        else:
            print("Limite máximo de alunos atingido.")

    elif escolha == 2:
        print("=-=" * 13)
        nome_aluno = input("Nome do Aluno: ")
        aluno_encontrado = None
        for aluno in sistema.alunos:
            if aluno['nome'] == nome_aluno:
                aluno_encontrado = aluno
                break
        else:
            print("Aluno não encontrado")
            continue
        while True:
            sistema.alerta_avaliacao_pendente(aluno_encontrado)
            print(f'''
[ 1 ] Relatório de {nome_aluno}
[ 2 ] Marcar Avaliação para {nome_aluno}
[ 3 ] Avaliar {nome_aluno}
[ 4 ] Enviar Mensagem para {nome_aluno}
[ 5 ] Visualizar Mensagens de {nome_aluno}
[ 6 ] Sair''')
            escolha1 = int(input("-> "))

            if escolha1 == 1:
                sistema.imprimir_relatorio(aluno_encontrado)

            elif escolha1 == 2:
                sistema.marcar_avaliacao(aluno_encontrado)

            elif escolha1 == 3:
                data_avaliacao = datetime.now().strftime("%Y-%m-%d")
                print(f"==== Avaliação Aluno {nome_aluno} ====")
                avaliador = input("Nome do Avaliador: ")
                tipo_avaliacao = input("Tipo de Avaliação: ")
                resultado_avaliacao = input(f"Resultado {tipo_avaliacao}: ")
                sistema.realizar_avaliacao(aluno_encontrado, tipo_avaliacao, data_avaliacao, resultado_avaliacao, avaliador)

            elif escolha1 == 4:
                remetente = input("Nome de Remetente: ")
                mensagem = input("Mensagem: ")
                sistema.enviar_mensagem(remetente, aluno_encontrado, mensagem)
                print("Mensagem enviada com sucesso!")

            elif escolha1 == 5:
                sistema.visualizar_mensagens(aluno_encontrado)

            elif escolha1 == 6:
                print("Saindo...")
                break

            else:
                print("Escolha invalida!")

    elif escolha == 3:
        sistema.salvar_dados_csv()
        print("Saindo do programa. Dados salvos.")
        break

    else:
        print("Escolha invalida!")

def Modulo_4():
  def criar_perfil_aluno():
      nome = input("Digite o nome do aluno: ")
      idade = int(input("Digite a idade do aluno: "))
      rest_alimentar = input("Digite as restrições alimentares (separadas por vírgula): ").split(',')
      objetivo_peso = input("Digite o objetivo de peso do aluno: ")
      preferencias_alimentares = input("Digite as preferências alimentares (separadas por vírgula): ").split(',')

      perfil = {
          'Nome': nome,
          'Idade': idade,
          'Restricoes Alimentares': rest_alimentar,
          'Objetivo de Peso': objetivo_peso,
          'Preferencias Alimentares': preferencias_alimentares,
          'Registro Alimentar': []
      }
      perfis_nutricionais[nome] = perfil
      print(f"Perfil para {nome} criado com sucesso!")

      salvar_perfil()

  def atualizar_perfil_aluno():
      nome = input("Digite o nome do aluno para atualizar o perfil: ")
      if nome in perfis_nutricionais:
          print(f"Perfil encontrado para {nome}. O que você deseja atualizar?")
          chave = input("Digite a chave (Nome, Idade, Restricoes Alimentares, Objetivo de Peso, Preferencias Alimentares): ")
          valor = input(f"Digite o novo valor para {chave}: ")

          perfis_nutricionais[nome][chave] = valor
          print(f"Informação atualizada para {nome}: {chave} = {valor}")

          salvar_perfil()
      else:
          print(f"Aluno {nome} não encontrado!")

  def registrar_ingestao_alimentar():
      nome = input("Digite o nome do aluno para registrar a ingestão alimentar: ")
      if nome in perfis_nutricionais:
          print(f"Perfil encontrado para {nome}.")
          refeicao = input("Digite a refeição ou lanche consumido: ")
          quantidade = float(input("Digite a quantidade consumida (em gramas): "))

          ingestao = {'Refeicao': refeicao, 'Quantidade': quantidade}
          perfis_nutricionais[nome]['Registro Alimentar'].append(ingestao)
          print(f"Ingestão registrada para {nome}: {refeicao} - {quantidade}g")

          salvar_perfil()
      else:
          print(f"Aluno {nome} não encontrado!")

  def salvar_perfil():
      with open('perfis_nutricionais.csv', 'w', newline='') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=['Nome', 'Idade', 'Restricoes Alimentares', 'Objetivo de Peso', 'Preferencias Alimentares', 'Registro Alimentar'])
          writer.writeheader()
          for aluno in perfis_nutricionais.values():
              writer.writerow(aluno)

  def obter_informacoes_nutricionais(api_key, alimento):
    # URL da API Edamam
    url = "https://api.edamam.com/api/nutrition-details"

    # Parâmetros da solicitação
    params = {
        "app_id": 'a68eca48',  # Substitua pelo seu app ID
        "app_key": '15945e901639b2e8ed72f06cb3a05a5a'	,  # Substitua pela sua chave de API
    }

    # Dados do corpo da solicitação
    data = {
        "title": alimento,
        "ingr": [alimento],
    }

    # Faz a solicitação POST para obter informações nutricionais
    response = requests.post(url, params=params, json=data)

    # Verifica se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Converte a resposta para JSON
        resultado = response.json()

        # Exibe as informações nutricionais
        print("Informações Nutricionais para", alimento)
        for nutrient in resultado['totalNutrients']:
            print(f"{nutrient['label']}: {nutrient['quantity']} {nutrient['unit']}")

    else:
        # Exibe uma mensagem de erro se a solicitação falhou
        print(f"Erro ao obter informações nutricionais. Código de status: {response.status_code}")

  def analisar_registro(nome, perfis_nutricionais):
    if nome in perfis_nutricionais:
        total_calorias = 0
        total_proteinas = 0
        total_carboidratos = 0
        total_gorduras = 0

        for item in perfis_nutricionais[nome]['Registro Alimentar']:
            refeicao = item['Refeicao']
            quantidade = item['Quantidade']

            dados_nutricionais = obter_informacoes_nutricionais(api_key, refeicao)

            if dados_nutricionais:
                for nutrient in dados_nutricionais:
                    if nutrient['label'] == 'Energy':
                        total_calorias += nutrient['quantity'] * quantidade / 100
                    elif nutrient['label'] == 'Protein':
                        total_proteinas += nutrient['quantity'] * quantidade / 100
                    elif nutrient['label'] == 'Carbohydrate':
                        total_carboidratos += nutrient['quantity'] * quantidade / 100
                    elif nutrient['label'] == 'Fat':
                        total_gorduras += nutrient['quantity'] * quantidade / 100

        print(f'Total de calorias: {total_calorias} kcal')
        print(f'Total de proteínas: {total_proteinas} g')
        print(f'Total de carboidratos: {total_carboidratos} g')
        print(f'Total de gorduras: {total_gorduras} g')

    else:
        print('Nome não registrado')

  def verificar_hidratacao(nome):
    consumo_agua_diario = perfis_nutricionais[nome]['Consumo de Água Diário (ml)']
    if consumo_agua_diario < 2000:
        print(f"Lembrete: {nome}, lembre-se de beber mais água para manter-se hidratado!")

  import requests

  def obter_valores_nutricionais(alimento, app_id, app_key):
      url = "https://api.edamam.com/api/nutrition-details"

      params = {
          "app_id": "a68eca48" ,
          "app_key": "15945e901639b2e8ed72f06cb3a05a5a"	
      }

      data = {
          "title": alimento,
          "ingr": [alimento]
      }

      response = requests.post(url, params=params, json=data)

      if response.status_code == 200:
          dados = response.json()
          return dados
      else:
          print(f"Erro ao obter os valores nutricionais. Código de status: {response.status_code}")
          return None

  def enviar_mensagem(assunto, mensagem, destinatario):
    # Substituir com config do servidor do email, se existir
    servidor_smtp = "smtp.example.com"
    porta_smtp = 587
    usuario_smtp = "seu_usuario"
    senha_smtp = "sua_senha"

    # mensagem MIME
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = usuario_smtp
    msg['To'] = destinatario
  def registrar_consumo_agua():
    nome = input("Digite o nome do aluno para registrar o consumo de água diário (em ml): ")
    if nome in perfis_nutricionais:
        consumo_agua = float(input("Digite a quantidade de água consumida (em ml): "))
        perfis_nutricionais[nome]['Consumo de Água Diário (ml)'] += consumo_agua
        print(f"Consumo de água registrado para {nome}: {consumo_agua}ml")

        # Verificar hidratação após registrar o consumo de água
        verificar_hidratacao(nome)

        salvar_perfil()
    else:
        print(f"Aluno {nome} não encontrado!")

  def registrar_suplemento():
    nome = input("Digite o nome do aluno para registrar o uso de suplemento alimentar: ")
    if nome in perfis_nutricionais:
        suplemento = input("Digite o suplemento utilizado: ")
        perfis_nutricionais[nome]['Suplementos Alimentares'].append(suplemento)
        print(f"Suplemento alimentar registrado para {nome}: {suplemento}")

        salvar_perfil()
    else:
        print(f"Aluno {nome} não encontrado!")

  while True:
      print('O que deseja:\n 1 - Criar perfil\n 2 - Atualizar perfil\n 3 - Registrar ingestão alimentar\n 4 - Registrar consumo de água\n 5 - Registrar consumo de suplementos\n 6 - Analisar registro\n 7 - Mensagem\n 8 - Valores Nutricionais\n 9 - Sair')

      escolha = input('Digite a opção desejada: ')

      if escolha == '1':
          criar_perfil_aluno()
      elif escolha == '2':
          atualizar_perfil_aluno()
      elif escolha == '3':
          registrar_ingestao_alimentar()
      elif escolha == '4':
          registrar_consumo_agua()
      elif escolha == '5':
          registrar_suplemento()
      elif escolha == '6':
          nome_aluno = input("Digite o nome do aluno para análise nutricional: ")
          analisar_registro(nome_aluno)
      elif escolha == '7':
        assunto = input('insira o assunto da mensagem: ')
        conteudo = input('conteudo da mensagem: ')
        destinatario = input('insira o destinatario: ')
        enviar_mensagem(assunto, conteudo, destinatario)
      elif escolha == '8':
        alimento = input("Digite o nome do alimento para obter os valores nutricionais: ")
        resultado = obter_valores_nutricionais(alimento, app_id, app_key)
        if resultado:
          print("Valores nutricionais para", alimento)
          for nutrient in resultado.get('totalNutrients', {}).values():
              print(f"{nutrient['label']}: {nutrient['quantity']} {nutrient['unit']}")
      elif escolha == '0':
        exit()
      else:
          print('Opção inválida')



def main():
    while True:
        print("=-" * 50)
        print("1 - Nutrição")
        print("2 - Acompanhamento de Treino")
        print("0 - Encerrar")

        escolha = input("Escolha o módulo desejado: ")

        if escolha == "1":
            Modulo_4()
        elif escolha == "2":
            Modulo_1()
        elif escolha == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")
