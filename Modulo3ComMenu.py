import smtplib
from email.mime.text import MIMEText
import json
import matplotlib.pyplot as plt

class CentralTreinamentoIndividual:
    def __init__(self, nome, idade, historico, metas, restricoes, preferencias):
        self.perfil_treino = self.criar_perfil_treino(nome, idade, historico, metas, restricoes, preferencias)
        self.biblioteca_videos = self.inicializar_biblioteca_videos()
        self.rotina_treino = None
        self.desempenho = {
            "cargas": {},
            "frequencia_cardiaca": {},
            # Pode-se adicionar mais
        }
        self.feedback = []
        self.comunicados_professor = []
        self.distintivos = []

    def criar_perfil_treino(self, nome, idade, historico, metas, restricoes, preferencias):
        perfil_treino = {
            "nome": nome,
            "idade": idade,
            "historico": historico,
            "metas": metas,
            "restricoes": restricoes,
            "preferencias": preferencias
        }

        # Salvando JSON
        with open('perfil_treino.json', 'w') as file:
            json.dump(perfil_treino, file)

        return perfil_treino

    def inicializar_biblioteca_videos(self):
        return {
            "Aeróbico": ["Vídeo 1", "Vídeo 2", "Vídeo 3"],
            "Musculação": ["Vídeo 4", "Vídeo 5", "Vídeo 6"],
            "Ioga": ["Vídeo 7", "Vídeo 8", "Vídeo 9"]
            # Dá pra adicionar mais categorias se necessário
        }

    def gerar_rotina_treino(self):
        tipo_treino = "Aeróbico" if "aerobico" in self.perfil_treino["preferencias"].lower() else "Musculação"
        duracao_treino = 30 if tipo_treino == "Aeróbico" else 45
        intensidade = "Moderada" if self.perfil_treino["historico"] == "Iniciante" else "Intensa"

        self.rotina_treino = {
            "tipo_treino": tipo_treino,
            "duracao": duracao_treino,
            "intensidade": intensidade,
            "exercicios": self.selecionar_exercicios(tipo_treino)
        }

        # Salvando arquivo JSON
        with open('rotina_treino.json', 'w') as file:
            json.dump(self.rotina_treino, file)

    def selecionar_exercicios(self, tipo_treino):
        if tipo_treino == "Aeróbico":
            return ["Corrida", "Pular corda", "Ciclismo"]
        elif tipo_treino == "Musculação":
            return ["Agachamento", "Supino", "Rosca direta"]
        else:
            return []

    def fornecer_feedback(self, mensagem):
        self.feedback.append({"aluno": self.perfil_treino["nome"], "mensagem": mensagem})

    def comunicar_professor(self, mensagem):
        self.comunicados_professor.append({"aluno": self.perfil_treino["nome"], "mensagem": mensagem})

    def ganhar_distintivo(self, nome_distintivo):
        if nome_distintivo not in self.distintivos:
            self.distintivos.append(nome_distintivo)

    def ver_distintivos(self):
        return self.distintivos

    def registrar_desempenho_exercicio(self, nome_exercicio, carga, frequencia_cardiaca):
        if nome_exercicio not in self.desempenho["cargas"]:
            self.desempenho["cargas"][nome_exercicio] = []
            self.desempenho["frequencia_cardiaca"][nome_exercicio] = []

        self.desempenho["cargas"][nome_exercicio].append(carga)
        self.desempenho["frequencia_cardiaca"][nome_exercicio].append(frequencia_cardiaca)

    def gerar_relatorio_desempenho(self):
        for nome_exercicio in self.desempenho["cargas"]:
            plt.plot(self.desempenho["cargas"][nome_exercicio], label=f'{nome_exercicio} - Carga')
            plt.plot(self.desempenho["frequencia_cardiaca"][nome_exercicio], label=f'{nome_exercicio} - FC')

        plt.xlabel('Sessões de Treino')
        plt.ylabel('Desempenho')
        plt.title('Desempenho do Aluno ao Longo do Tempo')
        plt.legend()
        plt.savefig('relatorio_desempenho.png')

    def enviar_alerta_treino(self):
        if self.rotina_treino is not None:
            assunto = f"Alerta de Treino - {self.rotina_treino['tipo_treino']}"
            mensagem = f"Olá {self.perfil_treino['nome']},\n\n"
            mensagem += f"Lembre-se de realizar o treino de hoje: {self.rotina_treino['tipo_treino']}.\n"
            mensagem += "Bons treinos!"

            destinatario = "email_do_aluno@example.com"  # Substitua pelo e-mail real do aluno

            self.enviar_email(assunto, mensagem, destinatario)

    def enviar_email(self, assunto, mensagem, destinatario):
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

        # Conectar-se ao servidor SMTP e enviar o e-mail
        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()
            server.login(usuario_smtp, senha_smtp)
            server.sendmail(usuario_smtp, destinatario, msg.as_string())

def exibir_menu():
    print("\nMENU:")
    print("1. Gerar Rotina de Treino")
    print("2. Registrar Desempenho em Exercício")
    print("3. Gerar Relatório de Desempenho")
    print("4. Enviar Alerta de Treino")
    print("5. Fornecer Feedback")
    print("6. Comunicar com Professor")
    print("7. Ganhar Distintivo")
    print("8. Ver Distintivos")
    print("9. Sair")

if __name__ == "__main__":
    central_treinamento = CentralTreinamentoIndividual(
        nome="João", idade=25, historico="Iniciante", metas="Perda de peso", restricoes="Nenhuma", preferencias="Treino aeróbico"
    )

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (1-9): ")

        if opcao == "1":
            central_treinamento.gerar_rotina_treino()
            print("Rotina de treino gerada e salva.")
        elif opcao == "2":
            nome_exercicio = input("Nome do exercício: ")
            carga = float(input("Carga: "))
            frequencia_cardiaca = int(input("Frequência Cardíaca: "))
            central_treinamento.registrar_desempenho_exercicio(nome_exercicio, carga, frequencia_cardiaca)
            print("Desempenho registrado.")
        elif opcao == "3":
            central_treinamento.gerar_relatorio_desempenho()
            print("Relatório de desempenho gerado e salvo.")
        elif opcao == "4":
            central_treinamento.enviar_alerta_treino()
            print("Alerta de treino enviado.")
        elif opcao == "5":
            feedback = input("Fornecer Feedback: ")
            central_treinamento.fornecer_feedback(feedback)
            print("Feedback fornecido.")
        elif opcao == "6":
            comunicado = input("Enviar Comunicado ao Professor: ")
            central_treinamento.comunicar_professor(comunicado)
            print("Comunicado enviado.")
        elif opcao == "7":
            distintivo = input("Nome do Distintivo: ")
            central_treinamento.ganhar_distintivo(distintivo)
            print("Distintivo ganho.")
        elif opcao == "8":
            distintivos = central_treinamento.ver_distintivos()
            print("Distintivos ganhos:", distintivos)
        elif opcao == "9":
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
