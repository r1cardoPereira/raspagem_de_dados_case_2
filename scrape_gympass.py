import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException, ElementClickInterceptedException
)
from bs4 import BeautifulSoup

def human_sleep(a=0.8, b=1.6):
    """Pequena espera randômica para parecer mais 'humano'."""
    time.sleep(random.uniform(a, b))

def expand_all_results(driver, timeout=30, sleep_min=0.3, sleep_max=0.8):
    """
    Expande todos os resultados de uma página, clicando em 'Ver mais' ou
    'Carregar mais' e rolando até o final, garantindo que todos os elementos
    estejam carregados antes de prosseguir.

    Args:
        driver: WebDriver ativo
        timeout: tempo máximo em segundos para tentar carregar todos os resultados
        sleep_min/sleep_max: intervalo aleatório entre ações para simular comportamento humano
    """
    start_time = time.time()
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while time.time() - start_time < timeout:
        # Tenta clicar no botão "Ver mais" se existir
        try:
            ver_mais_btn = driver.find_element(
                By.XPATH,
                "//button[contains(., 'Ver mais') or contains(., 'Ver todos') or contains(., 'Carregar mais')]"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ver_mais_btn)
            human_sleep(sleep_min, sleep_max)
            try:
                ver_mais_btn.click()
            except Exception:
                driver.execute_script("arguments[0].click();", ver_mais_btn)
            human_sleep(sleep_min, sleep_max)
            continue  # tenta novamente após clicar
        except NoSuchElementException:
            # Se não houver botão, faz scroll até o final da página
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            human_sleep(sleep_min, sleep_max)

        # Verifica se a altura da página mudou
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # Não houve mais carregamento, podemos parar
            break
        last_height = new_height


def parse_page_html(html, cep):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    container = soup.select_one("div.sc-98cb3247-9.sc-44ecda3e-1.gqOAaR.dcyPRw")
    if not container:
        print(f"[AVISO] Container principal não encontrado para o CEP {cep}")
        return results

    # Seleciona todos os cards de parceiros reais
    cards = [a for a in container.find_all("a", href=True) if "/partners/" in a['href']]

    for card in cards:
        try:
            # Nome da academia
            name_tag = card.find("h3")
            name = name_tag.get_text(strip=True) if name_tag else card.get_text(" ", strip=True).split("•")[0].strip()

            # Contêiner da info do card (pai ou próximo div)
            parent_div = card.find_parent("div", class_="sc-98cb3247-9")
            if not parent_div:
                parent_div = card

            # Distância e horário
            distance = "N/A"
            horario = "N/A"
            p_tags = parent_div.find_all("p")
            for p in p_tags:
                txt = p.get_text(" ", strip=True)
                if "m" in txt and "•" in txt:
                    parts = [s.strip() for s in txt.split("•")]
                    distance = parts[0]
                    horario = parts[1] if len(parts) > 1 else "N/A"
                    break

            # Atividades
            activities = "N/A"
            for p in p_tags:
                txt = p.get_text(" ", strip=True)
                if txt != distance + " • " + horario:
                    activities = txt
                    activities = activities.replace(" • ", ", ").strip()
                    break

            # Plano / Preço
            plan = "N/A"
            span = parent_div.find("span", string=lambda s: s and "A partir do plano" in s)
            if span:
                plan = span.get_text(" ", strip=True)
                plan = plan.replace("A partir do plano ", "").replace("•", "").strip()
            else:
                possible = parent_div.find(string=lambda s: s and ("plano" in s.lower() or "r$" in s.lower()))
                if possible:
                    plan = possible.strip()
                    plan = plan.replace("A partir do plano ", "").replace("•", "").strip()
                    

            results.append({
                "CEP": cep,
                "Nome Academia": name,
                "Distancia": distance,
                "Horario de Funcionamento": horario,
                "Atividades": activities,
                "Plano inicial": plan
            })

        except Exception as e:
            print(f"[AVISO] Erro ao processar card: {e}")
            continue

    return results


def scrape_gympass_data(ceps_file_path):
    # Carrega CEPs
    try:
        df_ceps = pd.read_csv(ceps_file_path)
        ceps = df_ceps['CEP'].astype(str).tolist()
    except FileNotFoundError:
        print(f"Erro: arquivo '{ceps_file_path}' não encontrado.")
        return

    # Inicia webdriver (ajuste se usar chromedriver em caminho custom)
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    
    except WebDriverException as e:
        print("Erro ao iniciar ChromeDriver:", e)
        return

    all_data = []

    for cep in ceps:
        print(f"\n=== Processando CEP: {cep} ===")
        try:
            driver.get("https://wellhub.com/pt-br/search/?gympass-variation-id=variation")
            human_sleep(1.0, 2.0)

            
            
            
            
            # Carregando elemento de input
            cep_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Cidade, endereço ou CEP']"))
            )
            
            # Garantindo que o input esteja vazio
            cep_input.send_keys(Keys.CONTROL + "a")
            cep_input.send_keys(Keys.DELETE)
            human_sleep(0.5, 1.0)
            
            # Inserindo CEP
            cep_input.send_keys(cep)
            human_sleep(0.6, 1.2)

            # tentar clicar no item de sugestão que contenha o CEP
            try:
                suggestion = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[.//p[contains(text(), '{cep}')]]"))
                )
                driver.execute_script("arguments[0].click();", suggestion)
                human_sleep(0.5, 1.2)
            except TimeoutException:
                # sugestão não encontrada — seguir mesmo assim
                pass

            # encontrar e clicar no botão Busca (ajuste caso o texto ou atributo seja diferente)
            try:
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Busca' and @aria-disabled='false']"))
                )
                driver.execute_script("arguments[0].click();", search_button)
            except TimeoutException:
                # tentar outro seletor só por segurança
                try:
                    search_button = driver.find_element(By.XPATH, "//button[contains(., 'Buscar') or contains(., 'Buscar resultados')]")
                    driver.execute_script("arguments[0].click();", search_button)
                except Exception:
                    pass

            # aguarda resultados iniciais
            human_sleep(2.0, 3.5)

            # Expande tudo (ver mais / scroll)
            expand_all_results(driver, timeout=30)
            human_sleep(1.0, 1.8)

            # captura o HTML completo da página (pode salvar num arquivo)
            page_html = driver.page_source
            # Opcional: salvar em arquivo para auditoria/debug
            with open(f"page_dump_{cep}.html", "w", encoding="utf-8") as f:
                f.write(page_html)

            # parse com BeautifulSoup (offline)
            results = parse_page_html(page_html, cep)
            print(f"  -> {len(results)} items extraídos para {cep}")
            all_data.extend(results)

        except Exception as e:
            print(f"Erro ao processar CEP {cep}: {e}")
            continue

    driver.quit()

    # salva CSV final
    if all_data:
        df = pd.DataFrame(all_data, columns=[
            "CEP", "Nome Academia", "Distancia", "Horario de Funcionamento", "Atividades", "Plano inicial"
        ])
        df.to_csv("academias_gympass.csv", index=False, encoding="utf-8-sig")
        print("\nCSV gerado: academias_gympass.csv")
    else:
        print("\nNenhum dado coletado. Verifique possibilidade de bloqueio ou mudanças no HTML.")

if __name__ == "__main__":
    ceps_file = "ceps_para_pesquisa.csv"
    scrape_gympass_data(ceps_file)
