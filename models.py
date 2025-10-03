from db import conectar
import datetime

# Criar escola
def criar_escola(nome, codigo, cnpj, tipo_escola, status, vendedor_id):
    conn = conectar()
    if not conn: 
        return None
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO escolas 
            (nome, codigo, cnpj, tipo_escola, status, vendedor_id, criado_em, atualizado_em, data_cadastro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """, (
            nome, codigo, cnpj, tipo_escola, status, vendedor_id,
            datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()
        ))
        escola_id = cur.fetchone()[0]
        conn.commit()
        return escola_id
    except Exception as e:
        print(f"❌ Erro ao criar escola: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# Listar todas as escolas
def listar_escolas():
    conn = conectar()
    if not conn: 
        return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, nome, tipo_escola, status FROM escolas ORDER BY id;")
        return cur.fetchall()
    except Exception as e:
        print(f"❌ Erro ao listar escolas: {e}")
        return []
    finally:
        cur.close()
        conn.close()


# Buscar escola por ID
def buscar_escola_por_id(escola_id):
    conn = conectar()
    if not conn: 
        return None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM escolas WHERE id = %s;", (escola_id,))
        return cur.fetchone()
    except Exception as e:
        print(f"❌ Erro ao buscar escola: {e}")
        return None
    finally:
        cur.close()
        conn.close()


# Atualizar escola
def atualizar_escola(escola_id, nome=None, codigo=None, cnpj=None, tipo_escola=None, status=None, vendedor_id=None):
    conn = conectar()
    if not conn: 
        return False
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE escolas
            SET nome = COALESCE(%s, nome),
                codigo = COALESCE(%s, codigo),
                cnpj = COALESCE(%s, cnpj),
                tipo_escola = COALESCE(%s, tipo_escola),
                status = COALESCE(%s, status),
                vendedor_id = COALESCE(%s, vendedor_id),
                atualizado_em = %s
            WHERE id = %s;
        """, (
            nome, codigo, cnpj, tipo_escola, status, vendedor_id,
            datetime.datetime.now(), escola_id
        ))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"❌ Erro ao atualizar escola: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


# Deletar escola
def deletar_escola(escola_id):
    conn = conectar()
    if not conn: 
        return False
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM escolas WHERE id = %s;", (escola_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"❌ Erro ao deletar escola: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
