from models_escola import criar_escola
from views import mostrar_escolas

#def adicionar_escola():
#    nome = input("Nome da escola: ")
#    codigo = input("Código (opcional): ") or None
#    cnpj = input("CNPJ (opcional): ") or None
#    tipo = input("Tipo (publica/privada) [default=publica]: ") or "publica"
#    status = input("Status (ativo/inativo) [default=ativo]: ") or "ativo"
#    vendedor_id = input("ID vendedor (opcional): ") or None
#    
#    escola_id = criar_escola(nome, codigo, cnpj, tipo, status, vendedor_id)
#    if escola_id:
#        print(f"✅ Escola criada com sucesso! ID = {escola_id}")



from db import input_or_none
import models as m
import views as v

# --- CONTROLADORES DE AÇÃO ---

# Gerenciamento de Escolas
def gerenciar_criar_escola():
    print("\n--- Criar Nova Escola ---")
    nome = input("Nome da escola: ")
    codigo = input_or_none("Código da escola (opcional): ")
    cnpj = input_or_none("CNPJ (opcional): ")
    tipo_escola = input("Tipo (publica, privada, etc.) [default=publica]: ") or 'publica'
    status = input("Status (ativo, inativo, suspenso) [default=ativo]: ") or 'ativo'
    vendedor_id = input_or_none("ID do Vendedor (opcional): ")

    escola_id = m.criar_escola(nome, codigo, cnpj, tipo_escola, status, vendedor_id)
    if escola_id:
        print(f"✅ Escola '{nome}' criada com sucesso com o ID {escola_id}.")

def gerenciar_listar_escolas():
    escolas = m.obter_todas_escolas()
    v.listar_escolas_view(escolas)

def gerenciar_buscar_escola():
    id_escola = input("ID da escola para buscar: ")
    escola, col_names = m.buscar_escola_por_id(id_escola)
    v.buscar_detalhes_view(escola, col_names, "Escola")

def gerenciar_atualizar_escola():
    id_escola = input("ID da escola para atualizar: ")
    if not m.buscar_escola_por_id(id_escola)[0]:
        print(f"⚠ Escola com ID {id_escola} não encontrada.")
        return

    print("Deixe o campo em branco para não alterar.")
    nome = input_or_none("Novo nome: ")
    status = input_or_none("Novo status (ativo, inativo, suspenso): ")

    resultado = m.atualizar_escola(id_escola, nome, status)
    
    if resultado is True:
        print("✅ Escola atualizada com sucesso.")
    elif resultado == "Nenhum campo fornecido":
        print("Nenhum campo para atualizar foi fornecido.")

def gerenciar_deletar_escola():
    id_escola = input("ID da escola a ser deletada: ")
    confirmacao = input(f"Tem certeza que deseja deletar a escola com ID {id_escola}? (s/n): ").lower()
    
    if confirmacao != 's':
        print("Operação cancelada.")
        return

    if m.deletar_escola(id_escola):
        print("✅ Escola deletada com sucesso.")
    else:
        print("⚠ Escola não encontrada ou erro ao deletar.")


# Gerenciamento de Unidades Escolares
def gerenciar_criar_unidade():
    v.listar_escolas_view(m.obter_todas_escolas())
    escola_id = input("Digite o ID da escola à qual esta unidade pertence: ")
    if not escola_id.isdigit():
        print("❌ ID da escola inválido.")
        return

    nome = input("Nome da unidade: ")
    tipo_unidade = input("Tipo (sede, filial, etc.) [default=sede]: ") or 'sede'
    status = input("Status (ativo, inativo, etc.) [default=ativo]: ") or 'ativo'

    unidade_id = m.criar_unidade_escolar(nome, tipo_unidade, status, escola_id)
    if unidade_id:
        print(f"✅ Unidade Escolar '{nome}' criada com sucesso com o ID {unidade_id}.")

def gerenciar_listar_unidades():
    unidades = m.obter_todas_unidades()
    v.listar_unidades_view(unidades)

def gerenciar_buscar_unidade():
    id_unidade = input("ID da unidade para buscar: ")
    unidade, col_names = m.buscar_unidade_escolar_por_id(id_unidade)
    v.buscar_detalhes_view(unidade, col_names, "Unidade Escolar")

def gerenciar_atualizar_unidade():
    id_unidade = input("ID da unidade para atualizar: ")
    if not m.buscar_unidade_escolar_por_id(id_unidade)[0]:
        print(f"⚠ Unidade com ID {id_unidade} não encontrada.")
        return
        
    print("Deixe o campo em branco para não alterar.")
    nome = input_or_none("Novo nome: ")
    tipo = input_or_none("Novo tipo (sede, filial, campus, etc.): ")
    status = input_or_none("Novo status (ativo, inativo, etc.): ")
    
    resultado = m.atualizar_unidade_escolar(id_unidade, nome, tipo, status)

    if resultado is True:
        print("✅ Unidade Escolar atualizada com sucesso.")
    elif resultado == "Nenhum campo fornecido":
        print("Nenhum campo para atualizar foi fornecido.")

def gerenciar_deletar_unidade():
    id_unidade = input("ID da unidade a ser deletada: ")
    if m.deletar_unidade_escolar(id_unidade):
        print("✅ Unidade Escolar deletada com sucesso.")
    else:
        print("⚠ Unidade Escolar não encontrada ou erro ao deletar.")


# Gerenciamento de Turmas
def gerenciar_criar_turma():
    v.listar_unidades_view(m.obter_todas_unidades())
    id_unidade = input("Digite o ID da unidade escolar à qual esta turma pertence: ")
    if not id_unidade.isdigit():
        print("❌ ID da unidade inválido.")
        return

    nome = input("Nome da turma (ex: 3º Ano A): ")
    ano = input_or_none("Ano letivo (ex: 2024): ")
    turno = input_or_none("Turno (matutino, vespertino, noturno): ")

    turma_id = m.criar_turma(nome, ano, turno, id_unidade)
    if turma_id:
        print(f"✅ Turma '{nome}' criada com sucesso com o ID {turma_id}.")

def gerenciar_listar_turmas():
    turmas = m.obter_todas_turmas()
    v.listar_turmas_view(turmas)

def gerenciar_buscar_turma():
    id_turma = input("ID da turma para buscar: ")
    turma, col_names = m.buscar_turma_por_id(id_turma)
    v.buscar_detalhes_view(turma, col_names, "Turma")

def gerenciar_atualizar_turma():
    id_turma = input("ID da turma para atualizar: ")
    if not m.buscar_turma_por_id(id_turma)[0]:
        print(f"⚠ Turma com ID {id_turma} não encontrada.")
        return

    print("Deixe o campo em branco para não alterar.")
    nome = input_or_none("Novo nome da turma (ex: 3º Ano B): ")
    ano = input_or_none("Novo ano letivo (ex: 2025): ")
    turno = input_or_none("Novo turno (matutino, vespertino, noturno): ")
    id_unidade = input_or_none("Novo ID da Unidade Escolar (opcional): ")
    
    resultado = m.atualizar_turma(id_turma, nome, ano, turno, id_unidade)

    if resultado is True:
        print("✅ Turma atualizada com sucesso.")
    elif resultado == "Nenhum campo fornecido":
        print("Nenhum campo para atualizar foi fornecido.")
    
def gerenciar_deletar_turma():
    id_turma = input("ID da turma a ser deletada: ")
    if m.deletar_turma(id_turma):
        print("✅ Turma deletada com sucesso.")
    else:
        print("⚠ Turma não encontrada ou erro ao deletar.")


# Gerenciamento de Usuários
def gerenciar_criar_usuario():
    nome = input("Nome: ")
    username = input("Username (opcional): ") or None
    email = input("Email: ")
    senha = input("Senha: ")
    is_admin = input("É admin? (s/n): ").lower() == "s"
    roles = input("Roles (separado por vírgula) [default=usuario]: ") or "usuario"

    usuario_id = m.criar_usuario(nome, username, email, senha, is_admin, roles)
    if usuario_id:
        print(f"✅ Usuário criado com ID {usuario_id}")

def gerenciar_listar_usuarios():
    usuarios = m.obter_todos_usuarios()
    v.listar_usuarios_view(usuarios)

def gerenciar_buscar_usuario():
    id_usuario = input("ID do usuário: ")
    usuario = m.buscar_usuario_por_id(id_usuario)
    v.buscar_usuario_view(usuario)

def gerenciar_atualizar_usuario():
    id_usuario = input("ID do usuário a atualizar: ")
    
    if not m.buscar_usuario_por_id(id_usuario):
        print(f"⚠ Usuário com ID {id_usuario} não encontrado.")
        return

    novo_nome = input("Novo nome (deixe vazio para não alterar): ")
    novo_email = input("Novo email (deixe vazio para não alterar): ")
    nova_senha = input("Nova senha (deixe vazio para não alterar): ")

    resultado = m.atualizar_usuario(id_usuario, novo_nome, novo_email, nova_senha)
    
    if resultado is True:
        print("✅ Usuário atualizado com sucesso.")
    elif resultado == "Nenhum campo fornecido":
        print("Nenhum campo para atualizar foi fornecido.")

def gerenciar_deletar_usuario():
    id_usuario = input("ID do usuário a excluir: ")
    if m.deletar_usuario(id_usuario):
        print("✅ Usuário excluído com sucesso.")
    else:
        print("⚠ Usuário não encontrado ou erro ao deletar.")


# --- MENUS DE NAVEGAÇÃO (CONTROLE DE FLUXO) ---

def menu_escola():
    while True:
        print("\n--- Gerenciar Escolas ---")
        print("1 - Criar Escola")
        print("2 - Listar Escolas")
        print("3 - Buscar Escola por ID")
        print("4 - Atualizar Escola")
        print("5 - Deletar Escola")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1": gerenciar_criar_escola()
        elif opcao == "2": gerenciar_listar_escolas()
        elif opcao == "3": gerenciar_buscar_escola()
        elif opcao == "4": gerenciar_atualizar_escola()
        elif opcao == "5": gerenciar_deletar_escola()
        elif opcao == "0": break
        else: print("⚠ Opção inválida.")

def menu_unidade():
    while True:
        print("\n--- Gerenciar Unidades Escolares ---")
        print("1 - Criar Unidade")
        print("2 - Listar Unidades")
        print("3 - Buscar Unidade por ID")
        print("4 - Atualizar Unidade")
        print("5 - Deletar Unidade")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1": gerenciar_criar_unidade()
        elif opcao == "2": gerenciar_listar_unidades()
        elif opcao == "3": gerenciar_buscar_unidade()
        elif opcao == "4": gerenciar_atualizar_unidade()
        elif opcao == "5": gerenciar_deletar_unidade()
        elif opcao == "0": break
        else: print("⚠ Opção inválida.")

def menu_turma():
    while True:
        print("\n--- Gerenciar Turmas ---")
        print("1 - Criar Turma")
        print("2 - Listar Turmas")
        print("3 - Buscar Turma por ID")
        print("4 - Atualizar Turma")
        print("5 - Deletar Turma")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1": gerenciar_criar_turma()
        elif opcao == "2": gerenciar_listar_turmas()
        elif opcao == "3": gerenciar_buscar_turma()
        elif opcao == "4": gerenciar_atualizar_turma()
        elif opcao == "5": gerenciar_deletar_turma()
        elif opcao == "0": break
        else: print("⚠ Opção inválida.")

def menu_usuario():
    while True:
        print("\n--- Gerenciar Usuários ---")
        print("1 - Criar usuário")
        print("2 - Listar usuários")
        print("3 - Buscar usuário por ID")
        print("4 - Atualizar usuário")
        print("5 - Deletar usuário")
        print("0 - Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")
        if opcao == "1": gerenciar_criar_usuario()
        elif opcao == "2": gerenciar_listar_usuarios()
        elif opcao == "3": gerenciar_buscar_usuario()
        elif opcao == "4": gerenciar_atualizar_usuario()
        elif opcao == "5": gerenciar_deletar_usuario()
        elif opcao == "0": break
        else: print("⚠ Opção inválida.")

def main_menu():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Gerenciar Escolas")
        print("2 - Gerenciar Unidades Escolares")
        print("3 - Gerenciar Turmas")
        print("4 - Gerenciar Usuários")
        print("0 - Sair do Programa")
        
        opcao = input("Escolha uma área para gerenciar: ")
        
        if opcao == "1": menu_escola()
        elif opcao == "2": menu_unidade()
        elif opcao == "3": menu_turma()
        elif opcao == "4": menu_usuario()
        elif opcao == "0":
            print("👋 Encerrando o programa.")
            break
        else:
            print("⚠ Opção inválida. Tente novamente.")
