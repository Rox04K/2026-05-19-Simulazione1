from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getGenre():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct *
                    from genre g """

        cursor.execute(query)

        for row in cursor:
            results.append(Genre(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from artist 
                    where ArtistId in (
                    select ArtistId
                    from album a, track t, genre g
                    where a.AlbumId = t.AlbumId and t.GenreId = g.GenreId
                    and g.GenreId = %s)"""

        cursor.execute(query, (genere,))

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(genere, mappa):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ with nodi as (
                    select distinct ArtistId
                    from album a, track t, genre g
                    where a.AlbumId = t.AlbumId and t.GenreId = g.GenreId
                    and g.GenreId = %s),
                    possibili as(
                    select a.ArtistId, i.CustomerId 
                    from invoice i, invoiceline i2, track t, album a 
                    where t.TrackId = i2.TrackId 
                    and i.InvoiceId = i2.InvoiceId 
                    and t.AlbumId = a.AlbumId 
                    and a.ArtistId in (select * from nodi)),
                    statistiche as(
                    select a.ArtistId , sum(Quantity) as popolarita 
                    from invoice i3, invoiceline i4, track t, album a 
                    where t.TrackId = i4.TrackId 
                    and i3.InvoiceId = i4.InvoiceId 
                    and t.AlbumId = a.AlbumId 
                    and a.ArtistId in (select * from nodi)
                    group by a.ArtistId )
                    select distinct p1.ArtistId as a1, p2.ArtistId as a2, (s1.popolarita + s2.popolarita) as peso
                    from possibili p1, possibili p2, statistiche s1, statistiche s2
                    where p1.CustomerId = p2.CustomerId
                    and s1.ArtistId = p1.ArtistId and s2.ArtistId = p2.ArtistId
                    and s1.popolarita >= s2.popolarita
                    and p1.ArtistId <> p2.ArtistId """

        cursor.execute(query, (genere,))

        for row in cursor:
            results.append((mappa[row['a1']], mappa[row['a2']], row['peso']))

        cursor.close()
        conn.close()
        return results