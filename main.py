import customtkinter as ctk
from tkinter import messagebox, Text
from tkinter import StringVar
import fdb
from tkinter import ttk


class ClientControlApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("ClientControl")
        self.geometry("600x400")

        self.db_conn = self.connect_db()

        self.create_widgets()

    def connect_db(self):
        try:
            conn = fdb.connect(
                # preencha com os dados do seu banco de dados
                dsn='localhost:C:\ClientsControl\ClientControl.fdb',
                user='SYSDBA',
                password='masterkey'
            )
            return conn
        except fdb.Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
            return None

    def create_widgets(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both")

        # Tela Inicial / consulta
        self.tab_startmenu = self.tabs.add("Tela Inicial")
        self.tela_inicial_widgets()

        # Tab Cadastro de Clientes
        self.tab_cadastro = self.tabs.add("Cadastro de Clientes")
        self.create_cadastro_widgets()

        # Tab Serviços
        self.tab_servicos = self.tabs.add("Serviços")
        self.create_servicos_widgets()

    def create_cadastro_widgets(self):
        self.nome_label = ctk.CTkLabel(self.tab_cadastro, text="Nome:")
        self.nome_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="e")
        self.nome_entry = ctk.CTkEntry(self.tab_cadastro, width=250)
        self.nome_entry.grid(row=0, column=1, padx=(0, 10), pady=10, columnspan=2)

        self.telefone_label = ctk.CTkLabel(self.tab_cadastro, text="Telefone:")
        self.telefone_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.telefone_entry = ctk.CTkEntry(self.tab_cadastro)
        self.telefone_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="w")

        self.email_label = ctk.CTkLabel(self.tab_cadastro, text="Email:")
        self.email_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = ctk.CTkEntry(self.tab_cadastro)
        self.email_entry.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="w")

        self.servico_label = ctk.CTkLabel(self.tab_cadastro, text="Serviço:")
        self.servico_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.servico_entry = ctk.CTkEntry(self.tab_cadastro)
        self.servico_entry.grid(row=3, column=1, padx=0, pady=10, sticky="w")

        self.select_servico = ctk.CTkButton(self.tab_cadastro, text="🔍", width=10, command=self.select_produto)
        self.select_servico.grid(row=3, column=2, padx=0, pady=10, sticky="w")

        self.cadastrar_button = ctk.CTkButton(self.tab_cadastro, text="Cadastrar", command=self.cadastrar_cliente)
        self.cadastrar_button.grid(row=4, columnspan=2, pady=20)

    def cadastrar_cliente(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        servico = self.servico_entry.get()

        if nome and telefone and email and servico:
            cursor = self.db_conn.cursor()
            try:
                cursor.execute("INSERT INTO clientes (nome, telefone, email, servico_id) VALUES (?, ?, ?, ?)",
                               (nome, telefone, email, servico))
                self.db_conn.commit()
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            except fdb.Error as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {e}")
            finally:
                cursor.close()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def create_servicos_widgets(self):
        self.descricao_label = ctk.CTkLabel(self.tab_servicos, text="Descrição:")
        self.descricao_label.grid(row=0, column=0, padx=10, pady=10)
        self.descricao_textbox = Text(self.tab_servicos, height=4, width=30)
        self.descricao_textbox.grid(row=0, column=1, padx=10, pady=10)

        self.urgencia_label = ctk.CTkLabel(self.tab_servicos, text="Urgência:")
        self.urgencia_label.grid(row=1, column=0, padx=10, pady=10)
        self.urgencia_var = StringVar()
        self.urgencia_combobox = ctk.CTkComboBox(self.tab_servicos, variable=self.urgencia_var, values=["Baixa", "Média", "Alta"])
        self.urgencia_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.etapa_label = ctk.CTkLabel(self.tab_servicos, text="Etapa:")
        self.etapa_label.grid(row=2, column=0, padx=10, pady=10)
        self.etapa_entry = ctk.CTkEntry(self.tab_servicos)
        self.etapa_entry.grid(row=2, column=1, padx=10, pady=10)

        self.anotacao_label = ctk.CTkLabel(self.tab_servicos, text="Anotação:")
        self.anotacao_label.grid(row=3, column=0, padx=10, pady=10)
        self.anotacao_textbox = Text(self.tab_servicos, height=4, width=30)
        self.anotacao_textbox.grid(row=3, column=1, padx=10, pady=10)

        self.salvar_button = ctk.CTkButton(self.tab_servicos, text="Salvar", command=self.salvar_servico)
        self.salvar_button.grid(row=4, columnspan=2, pady=20)

        self.valor_label = ctk.CTkLabel(self.tab_servicos, text="Valor: ")
        self.valor_label.grid(row=0, column=2, padx=10, pady=10)
        self.valor_entry = ctk.CTkEntry(self.tab_servicos)
        self.valor_entry.grid(row=0, column=3, padx=10, pady=10)

    def salvar_servico(self):
        descricao = self.descricao_textbox.get("1.0", "end-1c")
        urgencia = self.urgencia_var.get()
        etapa = self.etapa_entry.get()
        anotacao = self.anotacao_textbox.get("1.0", "end-1c")
        valor = self.valor_entry.get()

        if descricao and urgencia and etapa and anotacao:
            cursor = self.db_conn.cursor()
            try:
                cursor.execute("INSERT INTO servicos (descricao, urgencia, etapa, anotacao, valor) VALUES (?, ?, ?, ?, ?)",
                               (descricao, urgencia, etapa, anotacao, valor))
                self.db_conn.commit()
                messagebox.showinfo("Sucesso", "Serviço salvo com sucesso!")
            except fdb.Error as e:
                messagebox.showerror("Erro", f"Erro ao salvar serviço: {e}")
            finally:
                cursor.close()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def tela_inicial_widgets(self):
        self.pesquisa_label = ctk.CTkLabel(self.tab_startmenu, text="Buscar:")
        self.pesquisa_label.pack(padx=10, pady=10)
        self.pesquisa_entry = ctk.CTkEntry(self.tab_startmenu, width=300)
        self.pesquisa_entry.pack(padx=10, pady=10)

        self.pesquisar_button = ctk.CTkButton(self.tab_startmenu, text="Pesquisar", command=self.realizar_consulta)
        self.pesquisar_button.pack(padx=10, pady=10)

        self.resultados_tree = ttk.Treeview(self.tab_startmenu, columns=("ID", "Tipo", "Nome/Descrição", "Detalhes"),
                                            show="headings")
        self.resultados_tree.column('#0', width=1, anchor='center')
        self.resultados_tree.column('#1', width=1, anchor='center')
        self.resultados_tree.column('#2', width=30, anchor='center')
        self.resultados_tree.column('#3', width=250, anchor='center')
        self.resultados_tree.heading("ID", text="ID")
        self.resultados_tree.heading("Tipo", text="Tipo")
        self.resultados_tree.heading("Nome/Descrição", text="Nome/Descrição")
        self.resultados_tree.heading("Detalhes", text="Detalhes")
        self.resultados_tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.resultados_tree.bind("<Double-1>", self.service_client)

    def realizar_consulta(self):
        termo = self.pesquisa_entry.get()
        if not termo:
            messagebox.showerror("Erro", "Por favor, preencha o campo de busca.")
            return

        cursor = self.db_conn.cursor()
        try:
            query_cliente = "SELECT id, 'Cliente' AS tipo, nome, telefone || ', ' || email || ', ' || servico_id AS detalhes FROM clientes WHERE nome LIKE ? OR telefone LIKE ? OR email LIKE ? OR servico_id LIKE ?"
            query_servico = "SELECT id, 'Serviço' AS tipo, descricao, 'Urgência: ' || urgencia || ', Etapa: ' || etapa || ', Anotação: ' || anotacao AS detalhes FROM servicos WHERE descricao LIKE ? OR urgencia LIKE ? OR etapa LIKE ? OR anotacao LIKE ?"
            termo_like = f"%{termo}%"
            cursor.execute(query_cliente, (termo_like, termo_like, termo_like, termo_like))
            resultados_cliente = cursor.fetchall()
            cursor.execute(query_servico, (termo_like, termo_like, termo_like, termo_like))
            resultados_servico = cursor.fetchall()

            self.resultados_tree.delete(*self.resultados_tree.get_children())
            for row in resultados_cliente + resultados_servico:
                self.resultados_tree.insert("", "end", values=row)
        except fdb.Error as e:
            messagebox.showerror("Erro", f"Erro ao realizar a consulta: {e}")
        finally:
            cursor.close()

    def select_produto(self):
        self.new_tela = ctk.CTk()
        self.new_tela.geometry('400x400')
        self.servicos = ttk.Treeview(self.new_tela, columns=("ID", "DESCRICAO", "URGENCIA", "ETAPA"), show="headings")
        self.servicos.column('#0', width=1, anchor='center')
        self.servicos.column('#1', width=1, anchor='center')
        self.servicos.column('#2', width=150, anchor='center')
        self.servicos.column('#3', width=30, anchor='center')
        self.servicos.column('#4',width=40, anchor='center')
        self.servicos.heading("ID", text="ID")
        self.servicos.heading("DESCRICAO", text="DESCRICAO")
        self.servicos.heading("URGENCIA", text="URGENCIA")
        self.servicos.heading("ETAPA", text="ETAPA")
        self.servicos.pack(expand=True, fill="both", padx=10, pady=10)
        self.servicos.bind("<Double-1>", self.set_servico_cliente)
        self.servico_consulta()
        self.new_tela.mainloop()

    def servico_consulta(self):
        cursor = self.db_conn.cursor()

        try:
            query_servico = "SELECT id, descricao, urgencia, etapa FROM servicos"
            cursor.execute(query_servico)  # Executa a consulta SQL

            resultados_servico = cursor.fetchall()  # Busca os resultados

            self.servicos.delete(*self.servicos.get_children())  # Limpa a tabela
            for row in resultados_servico:
                self.servicos.insert("", "end", values=row)  # Insere os resultados na tabela
        except fdb.Error as e:
            messagebox.showerror("Erro", f"Erro ao realizar a consulta: {e}")
        finally:
            cursor.close()

    def set_servico_cliente(self, event):
        # Obtém o item selecionado
        selected_item = self.servicos.selection()[0]

        # Obtém o valor da primeira coluna do item selecionado
        id_servico = self.servicos.item(selected_item, 'values')[0]

        # Insere o valor no Entry
        self.servico_entry.delete(0, ctk.END)  # Limpa o Entry antes de inserir o novo valor
        self.servico_entry.insert(0, id_servico)

        # Fecha a janela
        self.new_tela.destroy()

    def on_click_cliente(self, id):
        cursor = self.db_conn.cursor()
        try:
            query_cliente = "SELECT id, nome, telefone, email, servico_id FROM clientes WHERE id = ?"
            cursor.execute(query_cliente, (id,))  # Executa a consulta SQL com o parâmetro correto

            resultados_clientes = cursor.fetchone()  # Busca o resultado único

            if resultados_clientes:
                # Insere o nome do cliente no entry (ajustando o índice conforme necessário)
                self.nome_entry.delete(0, ctk.END)  # Limpa o Entry antes de inserir o novo valor
                self.nome_entry.insert(0, resultados_clientes[1])  # Assume que 'nome' é o segundo campo na consulta

                self.telefone_entry.delete(0, ctk.END)
                self.telefone_entry.insert(0, resultados_clientes[2])

                self.email_entry.delete(0, ctk.END)
                self.email_entry.insert(0, resultados_clientes[3])

            self.tabs._segmented_button_callback('Cadastro de Clientes')
        except fdb.Error as e:
            messagebox.showerror("Erro", f"Erro ao realizar a consulta: {e}")
        finally:
            cursor.close()

    def on_click_service(self, id):

        cursor = self.db_conn.cursor()
        try:
            query_service = "SELECT id, descricao, urgencia, etapa, anotacao, valor FROM servicos WHERE id = ?"
            cursor.execute(query_service, (id,))  # Executa a consulta SQL com o parâmetro correto

            resultados_services = cursor.fetchone()  # Busca o resultado único

            if resultados_services:
                # Insere o nome do cliente no entry (ajustando o índice conforme necessário)
                #self.descricao_textbox.delete(0, ctk.END)  # Limpa o Entry antes de inserir o novo valor
                self.descricao_textbox.insert(0, resultados_services[1])  # Assume que 'nome' é o segundo campo na consulta

                self.urgencia_combobox.set(resultados_services[2])

                self.etapa_entry.delete(0, ctk.END)
                self.etapa_entry.insert(0, resultados_services[3])

                self.anotacao_textbox.delete(0, ctk.END)
                self.anotacao_textbox.insert(0, resultados_services[4])

                self.valor_entry.delete(0, ctk.END)
                self.valor_entry.insert(0, resultados_services[5])

            self.tabs._segmented_button_callback('Serviços')
        except fdb.Error as e:
            messagebox.showerror("Erro", f"Erro ao realizar a consulta: {e}")
        finally:
            cursor.close()

    def service_client(self, event):
        line = self.resultados_tree.selection()[0]
        type = self.resultados_tree.item(line, 'values')[1]
        id = self.resultados_tree.item(line, 'values')[0]
        print(id)

        if type == "Serviço":
            self.on_click_service(id)
        else:
            self.on_click_cliente(id)

    def chage_command_button_client(self):
        self.cadastrar_button.configure(command=self.update_cadastro_client)

    def update_cadastro_client(self):

        if descricao and urgencia and etapa and anotacao:
            cursor = self.db_conn.cursor() 
            try:
                cursor.execute("UPDATE servicos SET descricao, urgencia, etapa, anotacao, valor VALUES (?, ?, ?, ?, ?)",
                               (descricao, urgencia, etapa, anotacao, valor))
                self.db_conn.commit()
                messagebox.showinfo("Sucesso", "Serviço salvo com sucesso!")
            except fdb.Error as e:
                messagebox.showerror("Erro", f"Erro ao salvar serviço: {e}")
            finally:
                cursor.close()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def new_cadastro_client(self):
        ...

    def new_cadastro_serviço(self):
        ...

    def client_options(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both")

        # Tela Inicial / consulta
        self.tab_startmenu = self.tabs.add("Novo")
        # função que irá limpar os dados (caso preenchido) e irá alterar a função do botão para cadastrar

        # Tab Cadastro de Clientes
        self.tab_cadastro = self.tabs.add("Editar")
        self.update_cadastro_client()

        # Tab Serviços
        self.tab_servicos = self.tabs.add("Excluir")
        # Função que irá excluir o cadastro se necessário
    
    def service_options(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both")

        # Tela Inicial / consulta
        self.tab_startmenu = self.tabs.add("Tela Inicial")
        # função que irá limpar os dados (caso preenchido) e irá alterar a função do botão para cadastrar

        # Tab Cadastro de Clientes
        self.tab_cadastro = self.tabs.add("Cadastro de Clientes")
        # função que irá atualizar o cadastro do produto

        # Tab Serviços
        self.tab_servicos = self.tabs.add("Serviços")
        # Função que irá excluir o cadastro se necessário


if __name__ == "__main__":
    app = ClientControlApp()
    app.mainloop()
