# 🧾 Form Validator System — Regex & Decorators (Python)

## 🚀 Sistema Modular de Validação de Formulários

Projeto em Python que implementa um sistema de validação de dados de formulários utilizando:

- 🔍 **Expressões Regulares (Regex)**
- ⚙️ **Decoradores (Decorators)**

---

## 🎯 Objetivo

Construir um sistema que:

- ✅ Valida dados de entrada automaticamente
- ♻️ Reutiliza código com decoradores
- 🧠 Separa lógica de validação da lógica de negócio
- 🚀 Facilita expansão e manutenção

---

## 🧠 Conceitos Utilizados

- Regex (`re`)
- Decoradores em Python
- Funções de ordem superior
- Validação de dados
- Modularidade

---

## ⚙️ Funcionalidades

✔ Validação de Email  
✔ Validação de Telefone (Angola 🇦🇴)  
✔ Validação de Data (DD-MM-AAAA)  
✔ Validação de NIF Angolano  
✔ Sistema de validação automático via decorador  
✔ Tratamento de erros estruturado  

---


---

## 🔍 Validações Implementadas

| Campo | Regra |
|------|------|
| Email | Formato padrão `usuario@dominio.com` |
| Telefone | 9 dígitos (Angola) |
| Data | DD-MM-AAAA |
| NIF | Alfanumérico estruturado |

---

## ⚡ Como Funciona o Decorador

O decorador:

1. Recebe um dicionário de validações  
2. Percorre os dados do formulário  
3. Aplica validação por campo  
4. Acumula erros  
5. Só executa a função se tudo estiver válido  

---

## 💡 Exemplo de Uso

```python
@validar_formulario({
    "email": validar_email,
    "telefone": validar_telefone,
    "data": validar_data,
    "nif": validar_nif
})
def processar_cadastro(**dados):
    print("Cadastro realizado com sucesso!")

🧪 Testes
✅ Caso válido
email: joao@gmail.com
telefone: 923213912
data: 15-08-1995
nif: 021007251UE053

✔ Cadastro realizado com sucesso

❌ Caso inválido
telefone: 923-213-912
data: 2024/12/31

❌ Erros:
- telefone inválido
- data inválida

🧠 Modularidade (Muito Importante)

Para adicionar nova validação:

def validar_codigo_postal(cp):
    ...

👉 Basta adicionar ao dicionário:

"codigo_postal": validar_codigo_postal

✔ Sem alterar o decorador
✔ Código limpo e escalável

🚨 Tratamento de Erros

Mensagens claras por campo
Suporte a múltiplos erros
Validação de campos obrigatórios
Uso de exceções (ValueError)

📊 Critérios de Avaliação (Atendidos)

| Critério            | Status |
| ------------------- | ------ |
| Regex               | ✅      |
| Decorador           | ✅      |
| Modularidade        | ✅      |
| Tratamento de erros | ✅      |
| Organização         | ✅      |

👥 Equipa
Alípio Joaquim Zambo
Domingas Ernesto Rocha
Dulce Rita Manuel Gonçalves
Mendes Eduardo Gouveia Manuel ⭐
Nsimba Alberto Ndosi
🎓 Instituição

Universidade Kimpa Vita
Engenharia Informática

📌 Conclusão

Este projeto demonstra como:

👉 Regex valida dados com precisão
👉 Decoradores tornam o código reutilizável
👉 Modularidade facilita manutenção

🚀 Possíveis Melhorias
🌐 Integração com Flask ou Django
🔐 Validação de senha forte
💳 Validação de IBAN
🗄️ Integração com base de dados
🧾 Licença

MIT

⭐ Apoia o Projeto

Se gostaste, deixa uma ⭐ no repositório!
