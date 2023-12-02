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

        # Salvando arquivo JSON
        with open('perfil_treino.json', 'w') as file:
            json.dump(perfil_treino, file)

        return perfil_treino

    def inicializar_biblioteca_videos(self):
        return {
            "Aeróbico": ["Vídeo 1", "Vídeo 2", "Vídeo 3"],
            "Musculação": ["Vídeo 4", "Vídeo 5", "Vídeo 6"],
            "Ioga": ["Vídeo 7", "Vídeo 8", "Vídeo 9"]
            # Dá pra adicionar mais
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
        # Substituir as config pelo servidor certo, se existir
        servidor_smtp = "smtp.example.com"
        porta_smtp = 587
        usuario_smtp = "seu_usuario"
        senha_smtp = "sua_senha"

        # Usando MIME, mensagem
        msg = MIMEText(mensagem)
        msg['Subject'] = assunto
        msg['From'] = usuario_smtp
        msg['To'] = destinatario

        # Usar SMTP para enviar o email
        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()
            server.login(usuario_smtp, senha_smtp)
            server.sendmail(usuario_smtp, destinatario, msg.as_string())
