# 📄 arXiv Paper Summarizer com Gemini AI

Este projeto é uma ferramenta de automação em Python que realiza o *scraping* de artigos científicos do **arXiv** (versão HTML) e utiliza a inteligência artificial do **Google Gemini (modelo 2.5 Flash)** para gerar resumos técnicos, didáticos e estruturados.

O projeto foi construído utilizando o **[uv](https://github.com/astral-sh/uv)** para um gerenciamento de dependências e ambiente virtual moderno e ultra-rápido.

## 🚀 Funcionalidades

* **Web Scraping Automático:** Coleta o conteúdo HTML de artigos do arXiv a partir do ID do artigo.
* **Limpeza de Conteúdo:** Processa o HTML bruto (BeautifulSoup) para extrair apenas o texto relevante do corpo do artigo, removendo cabeçalhos e rodapés.
* **Resumo com IA Generativa:** Utiliza o modelo `gemini-2.5-flash` via SDK do Google GenAI para analisar e sintetizar o conteúdo.
* **Logs e Monitoramento:** Utiliza `loguru` para rastreamento detalhado de erros e fluxo de execução.
* **Resiliência:** Implementa decoradores (`@catch_erros_in_requests`) para tratar falhas em requisições HTTP de forma elegante.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Gerenciador de Pacotes:** [uv](https://docs.astral.sh/uv/)
* **IA / LLM:** Google GenAI SDK (`google-genai`)
* **Web Scraping:** BeautifulSoup4 (`bs4`) & Requests
* **Utilitários:** Loguru (Logs) & Python-dotenv (Variáveis de ambiente)

## ⚙️ Pré-requisitos

Antes de começar, você precisa ter o **uv** instalado. Ele substitui o `pip` e o `venv` tradicional com muito mais velocidade.

### Instalando o uv

**Linux e macOS:**
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```
### Chave de API
Você precisará de uma API Key do Google Gemini. Obtenha gratuitamente no Google AI Studio.

## Instalação e Configuração

Siga os passos abaixo para configurar o ambiente de desenvolvimento:

1. **Clone o Repositório:**
```bash
git clone https://github.com/luizfernandoOliveiraa/Paper-Assist.git
cd Paper-Assist
  ```
2. **Inicialize o projeto com uv**: Isso criará a estrutura necessária e o ambiente virtual.
```bash
uv init
```
3. **Instale as dependências**:
```bash
uv add requests beautifulsoup4 loguru google-genai python-dotenv
```
4. **Configure as Variáveis de Ambiente**: Crie um arquivo .env na raiz do projeto e adicione sua chave:
```env
GEMINI_KEY="sua_chave_aqui"
```
git ## Como Executar

Com o uv, você não precisa ativar o ambiente virtual manualmente. Basta usar o comando uv run.
```bash
uv run main.py
```
### Analisando Outros Artigos
Para analisar um artigo diferente, edite a linha final do arquivo main.py:
```python
if __name__ == "__main__":
    # Substitua pelo ID do artigo desejado (ex: 2401.00001)
    main("ID do artigo aqui!")
```
## Estrutura do Projeto
O projeto está organizado em um único arquivo main.py para simplicidade, contendo as seguintes funções principais:

- @catch_erros_in_requests: Decorator para capturar e logar erros de conexão HTTP.
- get_content_of_desc_paper(url): Realiza o GET na URL do arXiv.
- filter_content(soup): Extrai o texto limpo da div ltx_page_content.
- build_prompt(title, content): Monta o prompt de sistema e usuário para a IA.
- generate_response(prompt): Envia os dados para o Gemini e recebe o resumo.

## Contribuições
Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests. Ideias para melhorias:

Adicionar suporte a leitura de PDFs (OCR ou PyPDF).

Implementar CLI com argparse ou typer para passar o ID do artigo como argumento.

Salvar o resumo gerado em um arquivo Markdown local.