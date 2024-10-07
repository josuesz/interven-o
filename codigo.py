import sqlite3
import tkinter as tk
from tkinter import messagebox


# Função para conectar ao banco de dados e criar a tabela, se necessário
def conectar():
    conexao = sqlite3.connect('clientes.db')  # Cria/abre o arquivo clientes.db
    cursor = conexao.cursor()

    # Cria a tabela de clientes, se não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        telefone TEXT NOT NULL
    )
    ''')

    return conexao, cursor


# Função para incluir um cliente
def incluir_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()

    if nome and email and telefone:
        conexao, cursor = conectar()
        cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", (nome, email, telefone))
        conexao.commit()
        conexao.close()
        messagebox.showinfo("Sucesso", f'Cliente "{nome}" adicionado com sucesso!')
        listar_clientes()
    else:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")


# Função para listar os clientes na interface
def listar_clientes():
    conexao, cursor = conectar()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conexao.close()

    # Limpa a lista antes de mostrar novos resultados
    listbox_clientes.delete(0, tk.END)

    for cliente in clientes:
        listbox_clientes.insert(tk.END,
                                f'ID: {cliente[0]}, Nome: {cliente[1]}, E-mail: {cliente[2]}, Telefone: {cliente[3]}')


# Função para excluir um cliente
def excluir_cliente():
    try:
        selecionado = listbox_clientes.get(listbox_clientes.curselection())
        id_cliente = int(selecionado.split(",")[0].split(":")[1].strip())

        conexao, cursor = conectar()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", f'Cliente com ID {id_cliente} excluído com sucesso!')
        listar_clientes()
    except:
        messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")


# Função para atualizar um cliente
def atualizar_cliente():
    try:
        selecionado = listbox_clientes.get(listbox_clientes.curselection())
        id_cliente = int(selecionado.split(",")[0].split(":")[1].strip())

        novo_nome = entry_nome.get()
        novo_email = entry_email.get()
        novo_telefone = entry_telefone.get()

        if novo_nome and novo_email and novo_telefone:
            conexao, cursor = conectar()
            cursor.execute("UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
                           (novo_nome, novo_email, novo_telefone, id_cliente))
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", f'Cliente de ID {id_cliente} atualizado com sucesso!')
            listar_clientes()
        else:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")
    except:
        messagebox.showwarning("Atenção", "Selecione um cliente para atualizar.")


# Interface gráfica com Tkinter
root = tk.Tk()
root.title("CRUD Clientes")

# Configurar para tela cheia
root.attributes("-fullscreen", True)


# Função para sair do modo tela cheia com a tecla "Esc"
def sair_tela_cheia(event):
    root.attributes("-fullscreen", False)


# Vincular a tecla "Esc" para sair da tela cheia
root.bind("<Escape>", sair_tela_cheia)

# Labels e campos de entrada
tk.Label(root, text="Nome:").grid(row=0, column=1, padx=10, pady=10)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="E-mail:").grid(row=1, column=1, padx=10, pady=10)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Telefone:").grid(row=2, column=1, padx=10, pady=10)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=2, column=2, padx=10, pady=10)

# Botões para as operações CRUD
tk.Button(root, text="Incluir Cliente", command=incluir_cliente).grid(row=3, column=1, columnspan=2, padx=10, pady=10)
tk.Button(root, text="Atualizar Cliente", command=atualizar_cliente).grid(row=4, column=1, columnspan=2, padx=10,
                                                                          pady=10)
tk.Button(root, text="Excluir Cliente", command=excluir_cliente).grid(row=5, column=1, columnspan=2, padx=10, pady=10)

# Centralizar e ajustar tamanho da Listbox
frame_listbox = tk.Frame(root)
frame_listbox.grid(row=6, column=0, columnspan=3, padx=50, pady=20)

# Listbox para exibir os clientes
listbox_clientes = tk.Listbox(frame_listbox, width=100, height=20)
listbox_clientes.pack(side=tk.LEFT, padx=20)

# Barra de rolagem para a Listbox
scrollbar = tk.Scrollbar(frame_listbox)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Conectar a barra de rolagem à Listbox
listbox_clientes.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_clientes.yview)

# Chamar a função para listar clientes na inicialização
listar_clientes()

# Rodar a interface gráfica
root.mainloop()
