import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._genreUtente = None
        self._artistaUtente = None

    def fillDDGenre(self):
        opzioni = self._model.getGenre()

        opzioniDD = list(map(lambda x: ft.dropdown.Option(
            key=x.GenreId,
            text=x.Name,
            data=x,
            on_click=self._readGenre
        ), opzioni))
        self._view._ddGenre.options = opzioniDD

    def _readGenre(self, e):
        scelta = e.control.data

        if scelta is None:
            self._genreUtente = None

        else:
            self._genreUtente = scelta
            print(self._genreUtente)

    def handleCreaGrafo(self, e):
        genere = self._genreUtente
        if genere is None:
            self._view.create_alert('Attenzione! Selezionare un genere')
            return

        self._view.txt_result.controls.clear()
        self._model.creaGrafo(genere.GenreId)
        self._view.txt_result.controls.append(ft.Text(f'Grafo correttamente creato:', color='green'))

        nodi, archi = self._model.getInfo()
        self._view.txt_result.controls.append(ft.Text(f'Numero di nodi: {nodi}'))
        self._view.txt_result.controls.append(ft.Text(f'Numero di archi: {archi}'))

        artista = self._model.getBestArtista()
        self._view.txt_result.controls.append(ft.Text(f'Artista più influente {artista[0]} con influenza: {artista[1]}'))

        best = self._model.getBestArchi()
        self._view.txt_result.controls.append(ft.Text(f'Top 5 archi:'))
        for b in best:
            self._view.txt_result.controls.append(ft.Text(f'{b[0]} -> {b[1]} : {b[2]['weight']}'))

        self._fillDDArtista()
        self._view.update_page()

    def _fillDDArtista(self):
        opzioni = self._model.getNodi()

        opzioniDD = list(map(lambda x: ft.dropdown.Option(
            key=x.ArtistId,
            text=x.Name,
            data=x,
            on_click=self._readArtist
        ), opzioni))
        self._view._ddArtist.options = opzioniDD

    def _readArtist(self, e):
        scelta = e.control.data

        if scelta is None:
            self._artistaUtente = None

        else:
            self._artistaUtente = scelta
            print(self._artistaUtente)

    def handleCammino(self,e):
        artista = self._artistaUtente
        if artista is None:
            self._view.create_alert('Attenzione! Selezionare un artista')
            return

        self._view.txt_result.controls.clear()

        cammino, lunghezza = self._model.getCamminoOttimo(artista)

        self._view.txt_result.controls.append(ft.Text(f'Ho trovato un cammino lungo {lunghezza}', color='green'))
        for b in cammino:
            self._view.txt_result.controls.append(ft.Text(f'{b}'))

        self._view.update_page()