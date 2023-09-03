# Sistema de Gerenciamento Ethereum

Este é um aplicativo Streamlit que permite que os usuários realizem transações Ethereum, gerenciem seus contatos e façam login ou cadastro usando seus nomes de usuário e chaves privadas.

## Pré-requisitos

Antes de executar este aplicativo, você precisará ter o Python e algumas bibliotecas instaladas. Certifique-se de ter os seguintes pré-requisitos:

- Python 3.x (recomendado)
- `streamlit` (instalável via `pip`)
- `json` (biblioteca Python padrão)
- `web3` (instalável via `pip`)

Você também precisará de uma rede Ethereum local (por exemplo, Ganache) em execução em `http://127.0.0.1:7545` para testar transações.

## Instalação

1. Clone este repositório ou baixe o código-fonte para sua máquina.

2. Navegue até a pasta onde você baixou/clonou o código-fonte.

3. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   conda create --name SGE
   conda activate SGE
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução

Depois de concluir a instalação, você pode executar o aplicativo Streamlit:

```bash
streamlit run main.py
```

Isso iniciará o aplicativo em seu navegador padrão. Você poderá usar o aplicativo para fazer login, criar transações Ethereum e gerenciar contatos.

Lembre-se de que este é um exemplo de aplicativo de demonstração e não deve ser usado com contas Ethereum reais em uma rede principal. Certifique-se de estar usando uma rede Ethereum local para fins de teste e desenvolvimento. Certifique-se de manter suas chaves privadas seguras e não compartilhá-las com terceiros.