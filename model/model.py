import copy
import random

import networkx as nx

from database.DAO import DAO

from geopy.distance import distance


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._soluzioneBest = []
        self._bestLen = 0


    def calcolaPercorso(self, stringa, destinazione):
        sorgenti = self.AnalisiGrafo()
        d1 = sorgenti[random.randint(0, len(sorgenti)-1)][0]
        if not nx.has_path(self._grafo, d1, destinazione):
            print(f"{d1} e {destinazione} non sono connessi.")
            return [], d1

        self._soluzioneBest = []
        self._bestLen = 0

        parziale = [d1]
        self.ricorsione(parziale, stringa, destinazione)

        return self._soluzioneBest, d1

    def ricorsione(self, parziale, stringa, destinazione):
        if parziale[-1] == destinazione:
            if len(parziale) > self._bestLen:
                self._bestLen = len(parziale)
                self._soluzioneBest = copy.deepcopy(parziale)
            return

        else:
            for n in self._grafo.neighbors(parziale[-1]):
                if stringa not in n.Location and n not in parziale:
                    parziale.append(n)
                    self.ricorsione(parziale, stringa, destinazione)
                    parziale.pop()

    def getAllProvider(self):
        return DAO.getProvider()

    def buildGraph(self, x, provider):
        self._grafo.clear()
        self._nodes = DAO.getCollegamenti(provider)
        self._grafo.add_nodes_from(self._nodes)

        distanza = 0
        for n1 in self._nodes:
            for n2 in self._nodes:
                if n1 != n2:
                    distanza = distance((n1.mLat, n1.mLon), (n2.mLat, n2.mLon)).km
                    if distanza <= x:
                        self._grafo.add_edge(n1, n2, weight=distanza)

    def AnalisiGrafo(self):
        tupla = []
        for node in self._grafo.nodes():
            numeroVicini = len(list(self._grafo.neighbors(node)))
            tupla.append((node, numeroVicini))
        tupla.sort(key=lambda x: x[1], reverse=True) #decrescente
        tuplaMax = tupla[0]
        maggiori = []
        for t in tupla:
            if t[1] == tuplaMax[1]:
                maggiori.append(t)
        return maggiori

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getNodes(self):
        return self._grafo.nodes