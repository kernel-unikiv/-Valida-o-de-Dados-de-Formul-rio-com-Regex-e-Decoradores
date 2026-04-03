import re
from functools import wraps


# ──────────────────────────────────────────────
# 1. FUNÇÕES DE VALIDAÇÃO COM REGEX  (30%)
# ──────────────────────────────────────────────

def validar_email(email: str) -> bool:
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(padrao, email))


def validar_telefone(telefone: str) -> bool:
    padrao = r'^\d{9}$'
    return bool(re.match(padrao, telefone))


def validar_data(data: str) -> bool:
    padrao = r'^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-\d{4}$'
    return bool(re.match(padrao, data))


def validar_nif(nif: str) -> bool:
    # Padrão: começa com dígitos, contém pelo menos uma letra maiúscula, termina com dígitos ou letras
    padrao = r'^\d+[A-Z]{1,3}\d+$'
    return bool(re.match(padrao, nif))


# ──────────────────────────────────────────────
# 2. DECORADOR DE VALIDAÇÃO  (35%)
# ──────────────────────────────────────────────

def validar_formulario(validacoes: dict):
    def decorador(func):
        @wraps(func)                          # preserva nome e docstring da função original
        def wrapper(**kwargs):
            erros = {}                        # dicionário para acumular erros

            for campo, funcao_validar in validacoes.items():
                valor = kwargs.get(campo)     # obtém o valor do campo

                # Campo obrigatório ausente
                if valor is None:
                    erros[campo] = f"Campo '{campo}' é obrigatório e não foi informado."
                    continue

                # Aplica a função de validação; captura falhas inesperadas
                try:
                    if not funcao_validar(str(valor)):
                        erros[campo] = _mensagem_erro(campo)
                except Exception as e:
                    erros[campo] = f"Erro ao validar '{campo}': {e}"

            # Se existirem erros, lança exceção com relatório completo
            if erros:
                mensagem = "\n".join(
                    f"  ✗ {campo}: {msg}" for campo, msg in erros.items()
                )
                raise ValueError(f"\nErros de validação encontrados:\n{mensagem}")

            # Nenhum erro → executa a função decorada
            return func(**kwargs)

        return wrapper
    return decorador


def _mensagem_erro(campo: str) -> str:
    mensagens = {
        "email"    : "Formato inválido. Use o padrão: usuario@dominio.com",
        "telefone" : "Formato inválido. Use exactamente 9 dígitos, ex: 923213912",
        "data"     : "Formato inválido. Use o padrão: DD-MM-AAAA",
        "nif"      : "Formato inválido. O NIF deve ser alfanumérico, ex: 021007251UE053",
    }
    return mensagens.get(campo, f"Valor inválido para o campo '{campo}'.")


# ──────────────────────────────────────────────
# 3. FUNÇÃO DE PROCESSAMENTO  +  DECORADOR  (Modularidade 15%)
# ──────────────────────────────────────────────

# Dicionário de validações → fácil de ampliar sem tocar no decorador
VALIDACOES_CADASTRO = {
    "email"    : validar_email,
    "telefone" : validar_telefone,
    "data"     : validar_data,
    "nif"      : validar_nif,
}

@validar_formulario(VALIDACOES_CADASTRO)
def processar_cadastro(**dados_formulario):
    print("\n Todos os dados são válidos!")
    print("  Processando cadastro...\n")
    for campo, valor in dados_formulario.items():
        print(f"     {campo:<12}: {valor}")
    print("\n Cadastro realizado com sucesso!\n")
    return {"status": "sucesso", "dados": dados_formulario}


# ──────────────────────────────────────────────
# 4. TESTES  (Tratamento de Erros 10%)
# ──────────────────────────────────────────────

def separador(titulo: str):
    print("\n" + "═" * 55)
    print(f"  {titulo}")
    print("═" * 55)


def executar_teste(descricao: str, dados: dict):
    print(f"\n {descricao}")
    print("  " + "-" * 45)
    for campo, valor in dados.items():
        print(f"     {campo:<12}: {valor}")
    print()
    try:
        processar_cadastro(**dados)
    except ValueError as e:
        print(e)


if __name__ == "__main__":

    # ── Teste 1: Dados completamente válidos ──────────────
    separador("TESTE 1 — Dados Válidos")
    executar_teste(
        "Formulário preenchido correctamente",
        {
            "email"    : "joao.silva@gmail.com",
            "telefone" : "923213912",
            "data"     : "15-08-1995",
            "nif"      : "021007251UE053",
        }
    )

    # ── Teste 2: E-mail inválido ───────────────────────────
    separador("TESTE 2 — E-mail Inválido")
    executar_teste(
        "E-mail sem '@' e sem domínio",
        {
            "email"    : "joao.silva.gmail",
            "telefone" : "923213912",
            "data"     : "15-08-1995",
            "nif"      : "021007251UE053",
        }
    )

    # ── Teste 3: Múltiplos campos inválidos ───────────────
    separador("TESTE 3 — Múltiplos Erros")
    executar_teste(
        "Telefone com traços, data errada e NIF só números",
        {
            "email"    : "maria@empresa.co.ao",
            "telefone" : "923-213-912",        # traços não permitidos
            "data"     : "2024/12/31",          # formato errado
            "nif"      : "123456789",           # falta parte alfanumérica
        }
    )

    # ── Teste 4: Campo obrigatório ausente ────────────────
    separador("TESTE 4 — Campo Ausente")
    executar_teste(
        "NIF não foi enviado no formulário",
        {
            "email"    : "ana@outlook.com",
            "telefone" : "912345678",
            "data"     : "01-01-2000",
            # "nif" propositalmente omitido
        }
    )

    # ── Teste 5: Todos os campos inválidos ────────────────
    separador("TESTE 5 — Todos Inválidos")
    executar_teste(
        "Nenhum campo no formato correcto",
        {
            "email"    : "nao-e-um-email",
            "telefone" : "9232139120",          # 10 dígitos (excede o máximo)
            "data"     : "31/12/99",
            "nif"      : "00000",               # só dígitos, sem letras
        }
    )

    # ── Teste 6: Segundo NIF válido ────────────────────────
    separador("TESTE 6 — Segundo Formato de NIF")
    executar_teste(
        "NIF com estrutura alternativa",
        {
            "email"    : "pedro@angola.ao",
            "telefone" : "912000333",
            "data"     : "20-03-1990",
            "nif"      : "5000187643UE001",
        }
    )

    # ── Demonstração de Modularidade ──────────────────────
    separador("EXTRA — Modularidade: Nova Validação")

    def validar_codigo_postal(cp: str) -> bool:
        return bool(re.match(r'^\d{4}-\d{3}$', cp))

    @validar_formulario({
        "email"         : validar_email,
        "codigo_postal" : validar_codigo_postal,   # campo novo!
    })
    def processar_envio(**dados):
        print("\n Envio processado com sucesso!")
        return {"status": "sucesso"}

    print("\n Adicionando 'codigo_postal' sem tocar no decorador...\n")
    try:
        processar_envio(email="test@mail.com", codigo_postal="1234-567")
    except ValueError as e:
        print(e)

    try:
        processar_envio(email="test@mail.com", codigo_postal="99999")
    except ValueError as e:
        print(e)
