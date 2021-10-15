from bs4 import BeautifulSoup
import requests

from online import getPlayers


class App():

    def __init__(self):
        self.url = "https://aurera-global.com/?view=jogadores_online"
        self.players = getPlayers()

    def contentPage(self):
        try:
            html = requests.get(self.url)
            bs = BeautifulSoup(html.content, "html.parser")
            content = bs.find("tbody")

            return content
        except requests.ConnectionError as e:
            return None

    def getPlayers(self):
        players = []
        content = self.contentPage()
        for tags in content:
            playerInfo = list(tags)
            if len(playerInfo) < 4:
                del(playerInfo)
            else:
                name = playerInfo[0].getText()
                guild = playerInfo[1].getText()
                level = playerInfo[2].getText()
                vocation = playerInfo[3].getText()
                players.append([name, guild, level, vocation])

        return players

    def getVocationOnline(self):

        vocations = []
        for player in self.players:
            vocation = player[3]
            vocations.append(vocation)

        knight = vocations.count("Knight") + vocations.count("Elite\xa0Knight")
        paladin = vocations.count("Paladin") + vocations.count("Royal\xa0Paladin")
        sorcerer = vocations.count("Sorcerer") + vocations.count("Master\xa0Sorcerer")
        druid = vocations.count("Druid") + vocations.count("Elder\xa0Druid")
        no_vocation = vocations.count("None")
        total_online = knight + paladin + sorcerer + druid + no_vocation

        status_vocation_online = {
            "knight": knight,
            "paladin": paladin,
            "sorcerer": sorcerer,
            "druid": druid,
            "no_vocation": no_vocation,
            "total": total_online,
        }

        return status_vocation_online

    def saveName(self):
        with open("character_online_now.txt", "w") as file:
            for player in self.players:
                file.write(player[0])
            
        return "Nomes salvos com sucesso!"



app = App()
print(app.saveName())