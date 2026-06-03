import sqlite3

conexao = sqlite3.connect("estoque.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    senha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    quantidade INTEGER,
    usuario_id INTEGER
)
""")

conexao.commit()

usuario_id = None

while usuario_id is None:

    print("\n1 - Cadastrar usuário")
    print("2 - Fazer login")
    print("3 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":

        nome = input("Nome de usuário: ")
        senha = input("Senha: ")

        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, senha) VALUES (?, ?)",
                (nome, senha)
            )
            conexao.commit()

            print("Usuário cadastrado com sucesso!")

        except sqlite3.IntegrityError:
            print("Esse usuário já existe.")

    elif opcao == "2":

        nome = input("Usuário: ")
        senha = input("Senha: ")

        cursor.execute(
            "SELECT id FROM usuarios WHERE nome = ? AND senha = ?",
            (nome, senha)
        )

        usuario = cursor.fetchone()

        if usuario:
            usuario_id = usuario[0]
            print("Login realizado com sucesso!")
        else:
            print("Usuário ou senha incorretos.")

    elif opcao == "3":
        conexao.close()
        exit()

    else:
        print("Opção inválida.")

while True:

    print("\n1 - Cadastrar item")
    print("2 - Ver itens")
    print("3 - Retirar quantidade")
    print("4 - Remover item")
    print("5 - Excluir conta")
    print("6 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":

        nome_item = input("Nome do item: ")
        quantidade = int(input("Quantidade: "))

        cursor.execute(
            "INSERT INTO itens (nome, quantidade, usuario_id) VALUES (?, ?, ?)",
            (nome_item, quantidade, usuario_id)
        )

        conexao.commit()
        print("Item cadastrado com sucesso!")

    elif opcao == "2":

        cursor.execute(
            "SELECT id, nome, quantidade FROM itens WHERE usuario_id = ?",
            (usuario_id,)
        )

        itens = cursor.fetchall()

        if len(itens) == 0:
            print("Nenhum item cadastrado.")
        else:
            print("\nItens cadastrados:")
            for item in itens:
                print(f"ID: {item[0]} - {item[1]} | Quantidade: {item[2]}")

    elif opcao == "3":

        id_item = int(input("ID do item: "))
        retirada = int(input("Quantidade a retirar: "))

        cursor.execute(
            "SELECT quantidade FROM itens WHERE id = ? AND usuario_id = ?",
            (id_item, usuario_id)
        )

        resultado = cursor.fetchone()

        if resultado:

            quantidade_atual = resultado[0]

            if retirada <= quantidade_atual:

                nova_quantidade = quantidade_atual - retirada

                cursor.execute(
                    "UPDATE itens SET quantidade = ? WHERE id = ?",
                    (nova_quantidade, id_item)
                )

                conexao.commit()

                print("Quantidade atualizada!")

                if nova_quantidade == 0:
                    print("Produto sem estoque.")

            else:
                print("Quantidade insuficiente.")

        else:
            print("Item não encontrado.")

    elif opcao == "4":

        id_item = int(input("ID do item que deseja remover: "))

        cursor.execute(
            "DELETE FROM itens WHERE id = ? AND usuario_id = ?",
            (id_item, usuario_id)
        )

        conexao.commit()

        if cursor.rowcount > 0:
            print("Item removido com sucesso!")
        else:
            print("Item não encontrado.")

    elif opcao == "5":

        senha = input("Digite sua senha: ")

        cursor.execute(
            "SELECT senha FROM usuarios WHERE id = ?",
            (usuario_id,)
        )

        resultado = cursor.fetchone()

        if resultado and senha == resultado[0]:

            confirmacao = input(
                'ATENÇÃO! Todos os seus itens serão apagados.\n'
                'Digite "EXCLUIR" para confirmar: '
            )

            if confirmacao == "EXCLUIR":

                cursor.execute(
                    "DELETE FROM itens WHERE usuario_id = ?",
                    (usuario_id,)
                )

                cursor.execute(
                    "DELETE FROM usuarios WHERE id = ?",
                    (usuario_id,)
                )

                conexao.commit()

                print("Conta excluída com sucesso.")
                break

            else:
                print("Exclusão cancelada.")

        else:
            print("Senha incorreta.")

    elif opcao == "6":
        break

    else:
        print("Opção inválida.")

conexao.close()