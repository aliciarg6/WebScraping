import requests
from bs4 import BeautifulSoup
import csv


class Traspaso(object):
    jugador = ""
    fecha = ""
    equipo = ""
    tipo = ""

    def __init__(self, jugador, fecha, equipo, tipo):
        self.jugador = jugador
        self.fecha = fecha
        self.equipo = equipo
        self.tipo = tipo

def scraping(url):
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    page = requests.get(url, headers=agent)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="competition-select")

    job_elements = soup.find_all("div", class_="transfers-container")
    list_players = []

    club = ''
    tipo_transferencia = ''
    fecha_transferencia = ''
    nombre_jugador = ''
    equipo = ''
    subtipo_transferencia = ''
    for job_element in job_elements:
        a = job_element.find_all("tr")
        for aux in a:
            class_type = aux.get('class')[0]
            if class_type == 'group-head':
                club = aux.find('a').text.encode('utf-8')
            elif class_type == 'subgroup-head':
                tipo_transferencia = aux.find('th').text.encode('utf-8')
            elif class_type == 'odd' or class_type == 'even':
                lp = []
                nombre_jugador = aux.find("td", class_="player").text.encode('utf-8')
                fecha_transferencia = aux.find("td", class_="date").text.encode('utf-8')
                equipo = aux.find("td", class_="team").text.encode('utf-8')
                subtipo_transferencia = aux.find("td", class_="type").text.encode('utf-8')

                lp.append(club)
                lp.append(tipo_transferencia)
                lp.append(nombre_jugador)
                lp.append(fecha_transferencia)
                lp.append(equipo)
                lp.append(subtipo_transferencia)
                list_players.append(lp)

    return list_players

def writeListToCSV(listaTraspasos):

    fields = ['Club','Tipo Transferencia','Nombre Jugador', 'Fecha Traspaso', 'Equipo', 'Subtipo Traspaso']

    with open('output.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(listaTraspasos)



if __name__ == "__main__":
    url = 'https://es.soccerway.com/players/'

    list = scraping(url)
    writeListToCSV(list)

