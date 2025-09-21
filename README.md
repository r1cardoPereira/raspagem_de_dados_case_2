# Gympass Academy Scraper

Automação para consulta de academias cadastradas no Gympass por CEP, coletando informações de **nome, distância, horário de funcionamento, atividades e planos**.  

O script utiliza **Selenium** para navegação e interação com o site e **BeautifulSoup** para parsing do HTML.

---

## Pré-requisitos

- Python 3.10 ou superior
- Navegador Chrome ou Chromium instalado
- pip (gerenciador de pacotes Python)

---

## Instalação

1. Clone este repositório:

```bash
git clone https://github.com/r1cardoPereira/raspagem_de_dados_case_2.git
cd raspagem_de_dados_case_2
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
attrs==25.3.0
beautifulsoup4==4.13.5
certifi==2025.8.3
cffi==2.0.0
charset-normalizer==3.4.3
driver-manager==0.1.1
h11==0.16.0
idna==3.10
numpy==2.3.3
outcome==1.3.0.post0
packaging==25.0
pandas==2.3.2
pycparser==2.23
PySocks==1.7.1
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.5
selenium==4.35.0
six==1.17.0
sniffio==1.3.1
sortedcontainers==2.4.0
soupsieve==2.8
trio==0.30.0
trio-websocket==0.12.2
typing_extensions==4.14.1
tzdata==2025.2
urllib3==2.5.0
webdriver-manager==4.0.2
websocket-client==1.8.0
wsproto==1.2.0
```

---

## Configuração

1. Prepare um arquivo CSV chamado `ceps_para_pesquisa.csv` contendo os CEPs a serem consultados:

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

**Ricardo Pereira** – Desenvolvedor Python / Automação de Processos

```

