from models_escola import criar_escola
from views import mostrar_escolas

def adicionar_escola():
    nome = input("Nome da escola: ")
    codigo = input("Código (opcional): ") or None
    cnpj = input("CNPJ (opcional): ") or None
    tipo = input("Tipo (publica/privada) [default=publica]: ") or "publica"
    status = input("Status (ativo/inativo) [default=ativo]: ") or "ativo"
    vendedor_id = input("ID vendedor (opcional): ") or None
    
    escola_id = criar_escola(nome, codigo, cnpj, tipo, status, vendedor_id)
    if escola_id:
        print(f"✅ Escola criada com sucesso! ID = {escola_id}")
