# %%
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

url = "https://www.residentevildatabase.com/personagens/alex-wesker/"

def get_content(url):
    resp = requests.get(url)
    return resp


# %%
def get_basic_infos(soup):
    div_page = soup.find("div", class_ = "td-page-content")
    paragrafo = div_page.find_all("p")[1] 
    ems = paragrafo.find_all("em")
    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")
    return data
# %%
def get_aparicoes(soup):

    lis = (soup.find("div", class_ = "td-page-content")
                .find("h4")
                .find_next()
                .find_all("li"))
    aparicoes = [i.text for i in lis]
    return aparicoes
#print(soup)
# %%
def get_personagem_infos(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("error")
        return {}
    else:
        soup = BeautifulSoup(resp.content)
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        return data
# %%
def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find("div", class_ = "td-page-content")
            .find_all("a"))
    links = [i["href"] for i in ancoras]
    return links
# %%

links = get_links()
data = []
for i in tqdm(links):
    d = get_personagem_infos(i)
    d["link"] = i
    data.append(d)



# %%
data
import pandas as pd
df = pd.DataFrame(data)
# %%
