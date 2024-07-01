import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._locationScelta = None

    def handleCreaGrafo(self, e):
        distanza = self._view._txtInDistanza.value
        if distanza == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Distanza non inserita."))
            self._view.update_page()
            return

        try:
            x = float(distanza)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, soglia inserita non numerica."))
            self._view.update_page()
            return

        provider = self._view._ddProvider.value
        if provider is None:
            print("Seleziona un provider")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Seleziona un provider."))
            self._view.update_page()
            return

        self._model.buildGraph(x, provider)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo creato corretamente"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumNodes()} vertici."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumEdges()} archi."))
        self.fillDDTarget()
        self._view.update_page()



    def handleAnalizzaGrafo(self,e):
        if self._model.getNumNodes() == 0 and self._model.getNumEdges() == 0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, grafo vuoto."))
            self._view.update_page()
            return

        maggiori =self._model.AnalisiGrafo()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(ft.Text("Vertici con più vicini:"))
        for m in maggiori:
            self._view._txt_result.controls.append(ft.Text(f"{m[0]} -- {m[1]}"))
        self._view.update_page()

    def handleCalcolaPercorso(self,e):
        stringa = self._view._txtInString.value
        if stringa == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Stringa non inserita."))
            self._view.update_page()
            return

        destinazione = self._locationScelta

        percorso, sorgente = self._model.calcolaPercorso(stringa, destinazione)
        if percorso == []:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Non ho trovato un cammino da {sorgente} a {destinazione}."))
            self._view.update_page()
            return

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Ho trovato un cammino tra {sorgente} a {destinazione}."))
        for p in percorso:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()


    def fillDDProvider(self):
        provider = self._model.getAllProvider()
        for p in provider:
            self._view._ddProvider.options.append(ft.dropdown.Option(p))

    def fillDDTarget(self):
        localita = self._model.getNodes()
        for l in localita:
            self._view._ddTarget.options.append(ft.dropdown.Option(data = l, text = l.Location, on_click = self.readDDLocation))

    def readDDLocation(self, e):
        if e.control.data is None:
            self._locationScelta = None
        else:
            self._locationScelta = e.control.data