import streamlit as st
import json
from web3 import Web3

user_data_file = "data/user_data.json"
try:
    with open(user_data_file, "r") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}

def save_user_data(name, account_address, private_key):
    user_data[name] = {"account_address": account_address, "private_key": private_key}
    with open(user_data_file, "w") as file:
        json.dump(user_data, file)

def user_exists(name):
    return name in user_data


def create_contact(name, account_address):
    user_data[st.session_state.user]["contacts"][name] = account_address
    with open(user_data_file, "w") as file:
        json.dump(user_data, file)

def perform_transaction(sender, sender_private_key, recipient, amount):
    # Conectar-se à rede Ethereum
    ganache_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    if web3.is_connected():
        st.success("Conectado à rede Ethereum")
    else:
        st.error("Não foi possível conectar à rede Ethereum")
        return

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

if "user" not in st.session_state:
    st.session_state.user = None

st.subheader("Cadastro ou Login")
name = st.text_input("Nome do usuário")
if user_exists(name):
    private_key = st.text_input("Número da chave", type="password")
else:
    account_address = st.text_input("Número da conta")
    private_key = st.text_input("Número da chave", type="password")

if st.button("Entrar"):
    if user_exists(name):
        if private_key == user_data[name]["private_key"]:
            st.session_state.user = name
            st.success(f"Bem-vindo, {name}!")
        else:
            st.error("Chave privada incorreta. Verifique a chave e tente novamente.")
    else:
        if not account_address:
            st.error("Número da conta é obrigatório para o cadastro.")
        else:
            save_user_data(name, account_address, private_key)
            st.session_state.user = name
            st.success(f"Usuário cadastrado com sucesso!")

if st.session_state.user is not None:
    st.subheader("Gerenciamento de Contatos")
    if "contacts" not in user_data[st.session_state.user]:
        user_data[st.session_state.user]["contacts"] = {}
    
    contact_name = st.text_input("Nome do contato")
    contact_account_address = st.text_input("Número da conta do contato")
    if st.button("Adicionar Contato"):
        create_contact(contact_name, contact_account_address)
        st.success(f"Contato {contact_name} adicionado com sucesso!")
    
    st.subheader("Transações")
    recipient = st.selectbox("Selecione um contato", list(user_data[st.session_state.user]["contacts"].keys()))
    amount = st.number_input("Quantidade a ser transferida (ETH)")
    if st.button("Enviar"):
        perform_transaction(st.session_state.user, private_key, user_data[st.session_state.user]["contacts"][recipient], amount)