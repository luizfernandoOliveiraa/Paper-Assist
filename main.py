import requests
import functools
from typing import List
from loguru import logger
from bs4 import BeautifulSoup as bs
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_KEY"))


def catch_erros_in_requests(func):
    """"
    Decorator para capturar erros em requisições HTTP.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Erro na {func.__name__}: {e}")
            return None
    return wrapper

# Scraper de artigos científicos no arXiv
@catch_erros_in_requests
@logger.catch
def get_content_of_desc_paper(url: str) -> bs:
    """
    Obtém o conteúdo HTML do artigo científico a partir da URL fornecida.

    :param url: URL do artigo científico no arXiv para realizar o scrapping.

    :return: Objeto BeautifulSoup contendo o conteúdo HTML do artigo.
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return bs(response.text, "html.parser")

@logger.catch
def filter_content(soup: bs) -> str:
    """
    Extrai apenas o conteúdo principal do HTML do artigo.
    """
    if soup is None:
        return ""

    content_section = soup.find("div", class_="ltx_page_content")
    if not content_section:
        return ""

    # Removendo espaços desnecessários e obtendo o texto limpo
    text = content_section.get_text(separator="\n", strip=True)
    return text

sys_prompt = """
You are an expert in technology research analysis and technical article summarization.
You excel at breaking down complex technology papers into digestible content for your audience.
Your audience includes students, early-career researchers, engineers, and technology leaders.

Summarize the key findings in the following article [ARTICLE].

Focus on:
- Main objectives
- Key findings or contributions
- Methodologies or architectures used
- Implications or applications
- Limitations or future directions

Format:
- Bullet points with key ideas
- A short concluding paragraph
"""
@logger.catch
def build_prompt(article_title: str, content: str) -> str:
    """
    Constrói o prompt para o modelo Gemini com base no título do artigo e seu conteúdo.

    :param article_title: String com o título do artigo para identificação do artigo no sistema da arxiv.
    :param content: Conteúdo extraído do artigo científico.
    :return: Retorna o prompt completo para o modelo Gemini.
    """

    user_prompt = f"""
Article title: {article_title}

Here is the extracted article content:

{content}

Please summarize this article following the system instructions.
"""
    return sys_prompt + "\n\n" + user_prompt

@logger.catch
def generate_response(prompt: str) -> str:
    """
    Gera a resposta do modelo Gemini com base no prompt fornecido.
    :param prompt: Entrada do prompt criado para o modelo Gemini.
    :return: Retorna o resumo do artigo gerado pelo modelo Gemini.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

@logger.catch
def main(article_number: str):
    """
    Função principal para executar o fluxo de extração e resumo do artigo científico.
    :param article_number: Identificador do artigo no arXiv (ex: "2511.21080").
    :return: Não retorna nada.
    """
    url = f"https://arxiv.org/html/{article_number}v1"

    soup = get_content_of_desc_paper(url)
    content = filter_content(soup)

    if not content:
        print("Não foi possível extrair conteúdo do artigo.")
        return

    prompt = build_prompt(article_number, content)
    summary = generate_response(prompt)

    print("\n===================== SUMMARY =====================\n")
    print(summary)
    print("\n===================================================\n")


if __name__ == "__main__":
    main("2511.19654")
