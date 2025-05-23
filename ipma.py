import requests
from datetime import datetime

URL_CIDADES = "https://api.ipma.pt/open-data/distrits-islands.json"
URL_PREV = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{gid}.json"
URL_TYPES = "https://api.ipma.pt/open-data/weather-type-classe.json"

def _mapa_cidades():
    return """Mapeia as cidades para os seus IDS globais.
              Retorna um dicionario onde as chaves são os nomes das cidades e os valores são os ids globais"""
    try:
        dados= requests.get(URL_CIDADES, timeout=10).json()["data"]
        return {d ["local"]: d ["glocalIdlocal"] for d in dados}
    except Exception as e:
        print (f"Erro ao obter dados das cidades: {e}")
        return {}
    
def _mapa_icones():
    """
    Mapeia os tipos de tempo para descrição e nomes dos ficheiros dos ícones.
    Retorna um dicionário onde as chaves são os Ids dos tipos de tempo e os valores são tuplos com a descrição e o nome dos ficheiros do icone
    """
 
    try:
        dados = requests.get(URL_TYPES, timeout=10).json()["data"]
        return {
             int(d["idweatherType"]):
             (d["descweatherType"],
             f"w_ic_d_{str(d['idweatherType']).zfill(2)}.svg")
            for d in dados
        }
    except Exception as e:
        print(f"Erro ao obter os tipos de tempo: {e}")
        return []
    
# Dicionarios globais para cidades e icones
CIDADES = _mapa_cidades()
ICONES = _mapa_icones()

def previsao_por_cidade(nome_cidade):
    """
    Obter a precisão do tempo para uma cidade especifica.
    
    Args:
         nome_cidade (str): o nome da cidade para qual queremos obter a previsão do tempo
    Retorna: 
         lista: uma lista de dicionarios com a previsão diária, incluindo a descrição e o ícone
   Lança:
    ValueError se a cidade não for encontrada
    Exception se ocorrer um erro na chamada da API"""
    gid = CIDADES.get(nome_cidade.title())
    if gid is None:
        raise ValueError("Cidade não encontrada") 
    
    try: 
        # Obter os dados da previsao do tempo
        dados= requests.get (URL_PREV.format(gid=gid),timeout=10).json()["data"]
    except Exception as e:
        print (f"Erro ao obter a previsão: {e}")
        raise
    
    for d in dados: 
        try:
            # Obter o tipo de tempo e mapear para a descrição e icone
            weather_type = int(d.get("idweatherType", 0))
            desc, icon_file = ICONES.get(weather_type, ("", "icon-fallback.svg"))
        except (ValueError, TypeError):
            desc, icon_file = "-", "icon-fallback.svg"
            # Adicionar a descrição e o ficheiro do icone ao dicionário do dia
            d["descrição"] = desc
            d["icon_file"] = icon_file
    return dados  # retorna a lista de previsões processadas
    
