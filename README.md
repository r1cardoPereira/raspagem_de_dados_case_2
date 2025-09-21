# Gympass Academy Scraper

Automação para consulta de academias cadastradas no Gympass por CEP, coletando informações de **nome, distância, horário de funcionamento, atividades e planos**.  

O script utiliza **Selenium** para navegação e interação com o site e **BeautifulSoup** para parsing do HTML.

---

## Pré-requisitos

- Python 3.10 ou superior
- Chrome ou Chromium instalado
- [ChromeDriver](https://chromedriver.chromium.org/downloads) compatível com sua versão do Chrome
- pip (gerenciador de pacotes Python)

---

## Instalação

1. Clone este repositório:

```bash
git clone https://github.com/r1cardoPereira/gympass-scraper.git
cd gympass-scraper
````

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

> **requirements.txt** deve conter:

```
selenium
beautifulsoup4
pandas
```

---

## Configuração

1. Certifique-se de que o **ChromeDriver** está no PATH ou no mesmo diretório do script.
2. Prepare um arquivo CSV chamado `ceps_para_pesquisa.csv` contendo os CEPs a serem consultados:

```csv
CEP
01311-000
04538-100
```

---

## Execução

Execute o script principal:

```bash
python scrape_gympass.py
```

* O script abrirá o navegador, realizará as buscas por CEP e extrairá os dados.
* Um arquivo CSV chamado `academias_gympass.csv` será gerado ao final com os resultados.

---

## Observações

* O site pode bloquear scraping excessivo; por isso o script inclui pequenas pausas (`human_sleep`) e interação simulando comportamento humano.
* Cada CEP gera um dump do HTML na pasta do script (`page_dump_<CEP>.html`) para auditoria/debug.
* Campos extraídos:

  * `CEP`
  * `Nome Academia`
  * `Distancia`
  * `Horario de Funcionamento`
  * `Atividades`
  * `Plano inicial`

---

## Estrutura do repositório

```
gympass-scraper/
│
├─ scrape_gympass.py          # Script principal
├─ ceps_para_pesquisa.csv     # Lista de CEPs
├─ requirements.txt           # Dependências
├─ README.md                  # Este arquivo
└─ page_dump_<CEP>.html       # Dumps do HTML (gerados após execução)
```

---

## Autor

**Ricardo Pereira** – Desenvolvedor Python / Cientista de Dados

```

