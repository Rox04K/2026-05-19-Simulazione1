from model.model import Model

model = Model()

model.creaGrafo(1)
print('Grafo correttamente creato')

nodi, archi = model.getInfo() #Questa formattazione può variare in base all'esempio
print(f'Numero di nodi: {nodi}')
print(f'Numero di archi: {archi}')

print()
artista = model.getBestArtista()
print(f'Artista più influente {artista[0]} con influenza: {artista[1]}')

best = model.getBestArchi()
print(f'Top 5 archi:')
for b in best:
    print(f'{b[0]} -> {b[1]} : {b[2]['weight']}')

artisti = model.getNodi()

print()
cammino, lunghezza = model.getCamminoOttimo(artisti[0])
print(f'Ho trovato un cammino lungo {lunghezza}')
for s in cammino:
    print(f'{s}')








