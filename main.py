import streamlit as st
import json
from web3 import Web3

# Criar ou carregar o arquivo JSON para armazenar informações de usuário
user_data_file = "user_data.json"
try:
    with open(user_data_file, "r") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}

# Função para salvar os dados do usuário no JSON
def save_user_data(name, account_address, private_key):
    user_data[name] = {"account_address": account_address, "private_key": private_key}
    with open(user_data_file, "w") as file:
        json.dump(user_data, file)

# Função para verificar se o usuário existe no JSON
def user_exists(name):
    return name in user_data


def create_contact(name, account_address):
    user_data[st.session_state.user]["contacts"][name] = account_address
    with open(user_data_file, "w") as file:
        json.dump(user_data, file)

# Função para realizar uma transação
def perform_transaction(sender, sender_private_key, recipient, amount):
    # Conectar-se à rede Ethereum
    ganache_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    # Verificar conexão da rede
    if web3.is_connected():
        st.success("Conectado à rede Ethereum")
    else:
        st.error("Não foi possível conectar à rede Ethereum")
        return

    # Obter o saldo da conta do remetente
    balance_wei = web3.eth.get_balance(user_data[sender]["account_address"])
    balance_eth = web3.from_wei(balance_wei, "ether")
    st.write(f"Saldo da conta: {balance_eth} ETH")

    # Criar uma transação
    transaction = {
        "to": recipient,
        "value": web3.to_wei(amount, "ether"),
        "gas": 2000000,
        "gasPrice": web3.to_wei("50", "gwei"),
        "nonce": web3.eth.get_transaction_count(user_data[sender]["account_address"]),
    }

    signed_transaction = web3.eth.account.sign_transaction(transaction, user_data[sender]["private_key"])
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    st.success(f"Transação enviada. Hash: {web3.to_hex(tx_hash)}")



#inicial
st.title("Sistema de Gerenciamento Ethereum")

# Inicializar o estado de sessão
if "user" not in st.session_state:
    st.session_state.user = None

# Página de cadastro ou login
st.subheader("Cadastro ou Login")
name = st.text_input("Nome do usuário")
if user_exists(name):
    # Se o usuário já existe, solicitar apenas a chave privada
    private_key = st.text_input("Número da chave", type="password")
else:
    # Se o usuário não existir, solicitar o número da conta e a chave privada
    account_address = st.text_input("Número da conta")
    private_key = st.text_input("Número da chave", type="password")

if st.button("Entrar"):
    if user_exists(name):
        # Usuário já existe, verificar o número da chave
        if private_key == user_data[name]["private_key"]:
            st.session_state.user = name
            st.success(f"Bem-vindo, {name}!")
        else:
            st.error("Chave privada incorreta. Verifique a chave e tente novamente.")
    else:
        # Criar um novo usuário
        if not account_address:
            st.error("Número da conta é obrigatório para o cadastro.")
        else:
            save_user_data(name, account_address, private_key)
            st.session_state.user = name
            st.success(f"Usuário cadastrado com sucesso!")

# Se o usuário estiver logado, mostrar as páginas de gerenciamento de contatos e transações
if st.session_state.user is not None:
    # Página de gerenciamento de contatos
    st.subheader("Gerenciamento de Contatos")
    if "contacts" not in user_data[st.session_state.user]:
        user_data[st.session_state.user]["contacts"] = {}
    
    contact_name = st.text_input("Nome do contato")
    contact_account_address = st.text_input("Número da conta do contato")
    if st.button("Adicionar Contato"):
        create_contact(contact_name, contact_account_address)
        st.success(f"Contato {contact_name} adicionado com sucesso!")
    
    # Página de transações
    st.subheader("Transações")
    recipient = st.selectbox("Selecione um contato", list(user_data[st.session_state.user]["contacts"].keys()))
    amount = st.number_input("Quantidade a ser transferida (ETH)")
    if st.button("Enviar"):
        perform_transaction(st.session_state.user, private_key, user_data[st.session_state.user]["contacts"][recipient], amount)
