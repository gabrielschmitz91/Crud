from db import conectar
import datetime

# Criar escola
#def criar_escola(nome, codigo, cnpj, tipo_escola, status, vendedor_id):
#    conn = conectar()
#    if not conn: 
#       return None
#    cur = conn.cursor()
#    try:
#        cur.execute("""
#            INSERT INTO escolas 
#            (nome, codigo, cnpj, tipo_escola, status, vendedor_id, criado_em, atualizado_em, data_cadastro)
#            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
#        """, (
#            nome, codigo, cnpj, tipo_escola, status, vendedor_id,
#            datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()
#        ))
#        escola_id = cur.fetchone()[0]
#        conn.commit()
#        return escola_id
#    except Exception as e:
#        print(f"❌ Erro ao criar escola: {e}")
#        conn.rollback()
#    finally:
#        cur.close()
#        conn.close()


# Listar todas as escolas
#def listar_escolas():
#    conn = conectar()
#    if not conn: 
#        return []
#    cur = conn.cursor()
#    try:
#        cur.execute("SELECT id, nome, tipo_escola, status FROM escolas ORDER BY id;")
#        return cur.fetchall()
#    except Exception as e:
#        print(f"❌ Erro ao listar escolas: {e}")
#        return []
#    finally:
#        cur.close()
#        conn.close()


# Buscar escola por ID
#def buscar_escola_por_id(escola_id):
#    conn = conectar()
#    if not conn: 
#        return None
#    cur = conn.cursor()
#    try:
#        cur.execute("SELECT * FROM escolas WHERE id = %s;", (escola_id,))
#        return cur.fetchone()
#   except Exception as e:
#        print(f"❌ Erro ao buscar escola: {e}")
#        return None
#    finally:
#        cur.close()
#        conn.close()


# Atualizar escola
#def atualizar_escola(escola_id, nome=None, codigo=None, cnpj=None, tipo_escola=None, status=None, vendedor_id=None):
#    conn = conectar()
#    if not conn: 
#        return False
#    cur = conn.cursor()
#    try:
#        cur.execute("""
#            UPDATE escolas
#           SET nome = COALESCE(%s, nome),
#                codigo = COALESCE(%s, codigo),
#                cnpj = COALESCE(%s, cnpj),
#                tipo_escola = COALESCE(%s, tipo_escola),
#                status = COALESCE(%s, status),
#                vendedor_id = COALESCE(%s, vendedor_id),
#                atualizado_em = %s
#            WHERE id = %s;
#        """, (
#            nome, codigo, cnpj, tipo_escola, status, vendedor_id,
#            datetime.datetime.now(), escola_id
#        ))
#        conn.commit()
#        return cur.rowcount > 0
#    except Exception as e:
#        print(f"❌ Erro ao atualizar escola: {e}")
##        conn.rollback()
#       return False
#    finally:
#        cur.close()
#        conn.close()


# Deletar escola
#def deletar_escola(escola_id):
#    conn = conectar()
#    if not conn: 
#        return False
#    cur = conn.cursor()
#    try:
#        cur.execute("DELETE FROM escolas WHERE id = %s;", (escola_id,))
#        conn.commit()
#        return cur.rowcount > 0
#    except Exception as e:
#        print(f"❌ Erro ao deletar escola: {e}")
#        conn.rollback()
#        return False
#    finally:
#        cur.close()
#        conn.close()









import bcrypt
# Importa conectar e a nova função get_current_timestamp (que deve estar no db.py)
from db import conectar, get_current_timestamp

# --- Funções Genéricas (Reutilizáveis - DRY) ---

def obter_todos(tabela, select_cols, order_by):
    """Função genérica para listar todos os registros de uma tabela."""
    conn = conectar()
    if not conn: return []
    cur = conn.cursor()
    try:
        query = f"SELECT {select_cols} FROM {tabela} ORDER BY {order_by};"
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"❌ Erro ao obter dados de {tabela}: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def buscar_por_id(tabela, id_valor):
    """Função genérica para buscar um registro por ID e retornar seus detalhes e nomes das colunas."""
    conn = conectar()
    if not conn: return None, None
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM {tabela} WHERE id = %s;", (id_valor,))
        data = cur.fetchone()
        # Captura os nomes das colunas para a View
        col_names = [desc[0] for desc in cur.description] if data else None
        return data, col_names
    except Exception as e:
        print(f"❌ Erro ao buscar em {tabela}: {e}")
        return None, None
    finally:
        cur.close()
        conn.close()

def atualizar_generico(tabela, id_valor, updates_dict):
    """Função genérica para atualizar campos de um registro por ID."""
    conn = conectar()
    if not conn: return False
    cur = conn.cursor()
    
    updates = []
    params = []

    for key, value in updates_dict.items():
        if value is not None and value != '':
            updates.append(f"{key} = %s")
            params.append(value)

    if not updates:
        return "Nenhum campo fornecido"

    # Adiciona a atualização do timestamp
    updates.append("atualizado_em = %s")
    params.append(get_current_timestamp())
    params.append(id_valor)

    try:
        query = f"UPDATE {tabela} SET {', '.join(updates)} WHERE id = %s;"
        cur.execute(query, tuple(params))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"❌ Erro ao atualizar {tabela}: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def deletar_generico(tabela, id_valor):
    """Função genérica para deletar um registro por ID."""
    conn = conectar()
    if not conn: return False
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM {tabela} WHERE id = %s;", (id_valor,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"❌ Erro ao deletar em {tabela}: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


# --- Funções Específicas para Entidades (Usam as funções genéricas sempre que possível) ---

# ==================== ESCOLAS ====================

def criar_escola(nome, codigo, cnpj, tipo_escola, status, vendedor_id):
    conn = conectar()
    if not conn: return None
    cur = conn.cursor()
    try:
        # Usa get_current_timestamp para consistência
        now = get_current_timestamp()
        cur.execute("""
            INSERT INTO escolas 
            (nome, codigo, cnpj, tipo_escola, status, vendedor_id, criado_em, atualizado_em, data_cadastro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """, (nome, codigo, cnpj, tipo_escola, status, vendedor_id, now, now, now))
        escola_id = cur.fetchone()[0]
        conn.commit()
        return escola_id
    except Exception as e:
        print(f"❌ Erro ao criar escola: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

def obter_todas_escolas():
    # Chama a função genérica
    return obter_todos("escolas", "id, nome, cidade, status, tipo_escola", "id")

def buscar_escola_por_id(id_escola):
    # Chama a função genérica (agora retorna data e nomes das colunas)
    return buscar_por_id("escolas", id_escola)

def atualizar_escola(id_escola, nome, status):
    # Chama a função genérica, passando apenas os campos que o Controller (gerenciar_atualizar_escola) está enviando
    updates = {'nome': nome, 'status': status}
    return atualizar_generico("escolas", id_escola, updates)
    # OBS: O Controller só envia 'nome' e 'status' para manter a simplicidade, mas o genérico aceitaria mais.

def deletar_escola(id_escola):
    # Chama a função genérica
    return deletar_generico("escolas", id_escola)


# ==================== UNIDADES ESCOLARES ====================

def criar_unidade_escolar(nome, tipo_unidade, status, escola_id):
    conn = conectar()
    if not conn: return None
    cur = conn.cursor()
    try:
        now = get_current_timestamp()
        cur.execute("""
            INSERT INTO unidades_escolares
            (nome, tipo_unidade, status, escola_id, criado_em, atualizado_em)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """, (nome, tipo_unidade, status, escola_id, now, now))
        unidade_id = cur.fetchone()[0]
        conn.commit()
        return unidade_id
    except Exception as e:
        print(f"❌ Erro ao criar unidade: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

def obter_todas_unidades():
    return obter_todos("unidades_escolares", "id, nome, tipo_unidade, status, escola_id", "id")

def buscar_unidade_escolar_por_id(id_unidade):
    return buscar_por_id("unidades_escolares", id_unidade)

def atualizar_unidade_escolar(id_unidade, nome, tipo, status):
    updates = {'nome': nome, 'tipo_unidade': tipo, 'status': status}
    return atualizar_generico("unidades_escolares", id_unidade, updates)

def deletar_unidade_escolar(id_unidade):
    return deletar_generico("unidades_escolares", id_unidade)


# ==================== TURMAS ====================

def criar_turma(nome, ano, turno, id_unidade):
    conn = conectar()
    if not conn: return None
    cur = conn.cursor()
    try:
        now = get_current_timestamp()
        cur.execute("""
            INSERT INTO turmas
            (nome, ano, turno, id_unidade_escolar, criado_em, atualizado_em)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """, (nome, ano, turno, id_unidade, now, now))
        turma_id = cur.fetchone()[0]
        conn.commit()
        return turma_id
    except Exception as e:
        print(f"❌ Erro ao criar turma: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

def obter_todas_turmas():
    # Consulta mais complexa para mostrar o nome da Unidade
    conn = conectar()
    if not conn: return []
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT t.id, t.nome, t.ano, t.turno, u.nome AS nome_unidade, t.id_unidade_escolar 
            FROM turmas t
            JOIN unidades_escolares u ON t.id_unidade_escolar = u.id
            ORDER BY t.id;
        """)
        return cur.fetchall()
    except Exception as e:
        print(f"❌ Erro ao obter turmas: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def buscar_turma_por_id(id_turma):
    # Consulta mais complexa para mostrar o nome da Unidade
    conn = conectar()
    if not conn: return None, None
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT t.*, u.nome AS nome_unidade 
            FROM turmas t
            JOIN unidades_escolares u ON t.id_unidade_escolar = u.id
            WHERE t.id = %s;
        """, (id_turma,))
        turma = cur.fetchone()
        col_names = [desc[0] for desc in cur.description] if turma else None
        return turma, col_names
    except Exception as e:
        print(f"❌ Erro ao buscar turma: {e}")
        return None, None
    finally:
        cur.close()
        conn.close()

def atualizar_turma(id_turma, nome, ano, turno, id_unidade):
    updates = {'nome': nome, 'ano': ano, 'turno': turno, 'id_unidade_escolar': id_unidade}
    return atualizar_generico("turmas", id_turma, updates)

def deletar_turma(id_turma):
    return deletar_generico("turmas", id_turma)


# ==================== USUÁRIOS ====================

def criar_usuario(nome, username, email, senha, is_admin, roles):
    # Criptografa a senha antes de enviar
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    conn = conectar()
    if not conn: return None
    cur = conn.cursor()

    try:
        now = get_current_timestamp()
        cur.execute("""
            INSERT INTO usuarios
            (nome, username, email, senha_hash, is_admin, is_ativo, roles, criado_em, atualizado_em)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (nome, username, email, senha_hash, is_admin, True, roles, now, now))
        conn.commit()
        return cur.fetchone()[0]
    except Exception as e:
        print("❌ Erro ao criar usuário:", e)
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

def obter_todos_usuarios():
    return obter_todos("usuarios", "id, nome, email, is_admin, is_ativo, roles", "id")

def buscar_usuario_por_id(id_usuario):
    return buscar_por_id("usuarios", id_usuario)

def atualizar_usuario(id_usuario, novo_nome, novo_email, nova_senha):
    updates = {'nome': novo_nome, 'email': novo_email}
    
    # Se uma nova senha for fornecida, ela deve ser hasheada
    if nova_senha:
        senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()
        updates['senha_hash'] = senha_hash
        
    return atualizar_generico("usuarios", id_usuario, updates)

def deletar_usuario(id_usuario):
    return deletar_generico("usuarios", id_usuario)