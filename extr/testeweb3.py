'''
RODAR O GANACHE
cd squashfs-root
./AppRun
w

'''
from web3 import Web3

# Conectar-se a uma rede Ethereum local usando Ganache (mude para suas configurações)
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# verificar conexao da rede
if web3.is_connected():
    print("Conectado à rede Ethereum")
else:
    print("Não foi possível conectar à rede Ethereum")

# conta de quem deposita
account_address = "0xa8f7595Dea4ABC916e69f86Ce0760A3a3DA9550d"

# chave de quem deposita
private_key = "0x0db874ae678c60b088da789a57594b81aadfeab369a0d10aa36e72d4f23e9112"

# Obter o saldo da conta
balance_wei = web3.eth.get_balance(account_address)
balance_eth = web3.from_wei(balance_wei, "ether")
print(f"Saldo da conta: {balance_eth} ETH")

# transação (usado apenas para fins educacionais, NÃO COMPARTILHE)
transaction = {
    "to": "0xd4f934BB55b450f25f7cb2BD236d85C702549A7D",
    "value": web3.to_wei(0.3, "ether"),
    "gas": 2000000,
    "gasPrice": web3.to_wei("50", "gwei"),
    "nonce": web3.eth.get_transaction_count(account_address),
}

signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
print(f"Transação enviada. Hash: {web3.to_hex(tx_hash)}")

# Obter informações de um bloco
block_number = web3.eth.block_number
block = web3.eth.get_block(block_number)
print(f"Informações do bloco {block_number}:")
print(f"Hash: {block['hash'].hex()}")
print(f"Timestamp: {block['timestamp']}")
print(f"Transações: {block['transactions']}")
