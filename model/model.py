import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()  
        self._IDMap = {}  

        self._bestCammino = []
        self._bestLunghezza = 0
    
    def getGenre(self):
        return DAO.getGenre()

    def creaGrafo(self, genere):
        self._grafo.clear()
        self._IDMap = {}

        nodi = DAO.getNodi(genere)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            self._IDMap[n.ArtistId] = n

        archi = DAO.getArchi(genere, self._IDMap)
        for a in archi:
            self._grafo.add_edge(a[0], a[1], weight=a[2])

    def getInfo(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getBestArtista(self):
        nodi = []
        for n in list(self._grafo.nodes()):
            archiEntranti = list(self._grafo.in_edges(n, data=True))
            archiUscenti = list(self._grafo.out_edges(n, data=True))

            sommaE = sum([d['weight'] for u, v, d in archiEntranti])
            sommaU = sum([d['weight'] for u, v, d in archiUscenti])

            punteggio = sommaU - sommaE
            nodi.append((n, punteggio))

        nodi.sort(key=lambda x: x[1], reverse=True)
        return nodi[0]

    def getBestArchi(self):
        archi_ordinati = sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        return archi_ordinati[:5]

    def getNodi(self):
        return list(self._grafo.nodes())

    def getCamminoOttimo(self, nodo):
        self._bestCammino = []
        self._bestLunghezza = 0

        parziale = [nodo]
        self._ricorsione(parziale)

        return self._bestCammino, (self._bestLunghezza - 1)

    def _ricorsione(self, parziale):

        validi = self._getSuccessors(parziale)
        if validi == []:
            if len(parziale) > self._bestLunghezza:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestLunghezza = len(parziale)

        for n in validi:  # continuo la mia ricorsione
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()

    def _getSuccessors(self, parziale):
        succ = self._grafo.successors(parziale[-1])
        validi = []

        for n in succ:
            if n not in parziale:
                if len(parziale) >= 2:
                    if self._grafo[parziale[-1]][n]['weight'] > self._grafo[parziale[-2]][parziale[-1]]['weight']:
                        validi.append(n)
                else:
                    validi.append(n)

        return validi