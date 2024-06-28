import sqlite3
from tkinter import *

root = Tk()
root.title("Tietokantasovellus")
# root.iconbitmap("C:/image.ico") (Tämä on sovelluskuvake)
root.geometry("360x400")

# Luodaan tietokanta(/-yhteys, jos tietokanta on jo olemassa)
conn = sqlite3.connect('osoite_kirja.db')
cur = conn.cursor()

''' Luodaan "osoitteet"-taulu tietokantaan. Alla oleva täytyy poistaa kommenteista, kun ohjelman ajaa ensimmäisen kerran. 
Sen jälkeen alla olevan voi asettaa uudestaan kommentteihin.
cur.execute("""CREATE TABLE osoitteet (
    etunimi text,
    sukunimi text,
    osoite text,
    postinumero integer,
    kaupunki text,
    maa text
)""")
'''


# Tämä funktio lisää uuden tietueen tietokantaan
def toimita():
    conn = sqlite3.connect('osoite_kirja.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO osoitteet VALUES (:enimi, :snimi, :osoite, :postinro, :kaupunki, :maa)",
                {
                    'enimi': enimi.get(),
                    'snimi': snimi.get(),
                    'osoite': osoite.get(),
                    'postinro': postinro.get(),
                    'kaupunki': kaupunki.get(),
                    'maa': maa.get()
                })

    conn.commit()
    conn.close()

    # Entryt tyhjennetään napin painamisen jälkeen
    enimi.delete(0, END)
    snimi.delete(0, END)
    osoite.delete(0, END)
    postinro.delete(0, END)
    kaupunki.delete(0, END)
    maa.delete(0, END)

# Tämä funktio tekee kyselyn tietokantaan ja hakee tietueen
def kysely():
    conn = sqlite3.connect('osoite_kirja.db')
    cur = conn.cursor()

    cur.execute("SELECT *, oid FROM osoitteet")
    tietueet = cur.fetchall()

    tulosta_tietueet = ''
    for tietue in tietueet:
        tulosta_tietueet += str(tietue[0]) + " " + str(tietue[1]) + " " + str(tietue[6]) + "\n"
        # Näytettävät tiedot tietueessta: voi muokata haluamallansa tavalla

    kysely_label = Label(root, text=tulosta_tietueet)
    kysely_label.grid(row=12, column=0, columnspan=2)

    conn.commit()
    conn.close()

# Tämä funktio päivittää tietueen (esim. tietuetta muokattaessa)
def paivita():
    conn = sqlite3.connect('osoite_kirja.db')
    cur = conn.cursor()

    tietue_id = poista_entry.get()
    cur.execute("""UPDATE osoitteet SET 
        etunimi = :enimi,
        sukunimi = :snimi,
        osoite = :osoite,
        postinumero = :postinro,
        kaupunki = :kaupunki,
        maa = :maa
        
        WHERE oid = :oid""",
                {
                    'enimi': editori_enimi.get(),
                    'snimi': editori_snimi.get(),
                    'osoite': editori_osoite.get(),
                    'postinro': editori_postinro.get(),
                    'kaupunki': editori_kaupunki.get(),
                    'maa': editori_maa.get(),
                    'oid': tietue_id
                })

    conn.commit()
    conn.close()

# Tämä funktio poistaa tietueen tietokannasta
def poista():
    conn = sqlite3.connect('osoite_kirja.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM osoitteet WHERE oid = " + poista_entry.get())

    conn.commit()
    conn.close()

# Tämä funtkio muokkaa tietueen tietoja
def muokkaa():
    editori = Tk()
    editori.title("Tietueen muokkaus")
    editori.iconbitmap("C:/image.ico")
    editori.geometry("360x400")

    conn = sqlite3.connect('osoite_kirja.db')
    cur = conn.cursor()

    tietue_id = poista_entry.get()
    cur.execute("SELECT * FROM osoitteet WHERE oid = " + tietue_id)
    tietueet = cur.fetchall()

    # Luodaan globaalit muuttujat entryille muokkausikkunaa varten
    global editori_enimi
    global editori_snimi
    global editori_osoite
    global editori_postinro
    global editori_kaupunki
    global editori_maa

    # Luodaan entryt ja labelit muokkausikkunaan
    editori_enimi = Entry(editori, width=30)
    editori_enimi.grid(row=0, column=1, padx=20, pady=(10, 0))
    editori_snimi = Entry(editori, width=30)
    editori_snimi.grid(row=1, column=1, padx=20)
    editori_osoite = Entry(editori, width=30)
    editori_osoite.grid(row=2, column=1, padx=20)
    editori_postinro = Entry(editori, width=30)
    editori_postinro.grid(row=3, column=1, padx=20)
    editori_kaupunki = Entry(editori, width=30)
    editori_kaupunki.grid(row=4, column=1, padx=20)
    editori_maa = Entry(editori, width=30)
    editori_maa.grid(row=5, column=1, padx=20)

    editori_enimi_label = Label(editori, text="Etunimi")
    editori_enimi_label.grid(row=0, column=0, pady=(10, 0))
    editori_snimi_label = Label(editori, text="Sukunimi")
    editori_snimi_label.grid(row=1, column=0)
    editori_osoite_label = Label(editori, text="Osoite")
    editori_osoite_label.grid(row=2, column=0)
    editori_postinro_label = Label(editori, text="Postinumero")
    editori_postinro_label.grid(row=3, column=0)
    editori_kaupunki_label = Label(editori, text="Kaupunki")
    editori_kaupunki_label.grid(row=4, column=0)
    editori_maa_label = Label(editori, text="Maa")
    editori_maa_label.grid(row=5, column=0)

    # Täytetään entryt annetuilla arvoilla
    for tietue in tietueet:
        editori_enimi.insert(0, tietue[0])
        editori_snimi.insert(0, tietue[1])
        editori_osoite.insert(0, tietue[2])
        editori_postinro.insert(0, tietue[3])
        editori_kaupunki.insert(0, tietue[4])
        editori_maa.insert(0, tietue[5])

    tallenna_nappi = Button(editori, text="Tallenna tietue", command=paivita)
    tallenna_nappi.grid(row=6, column=0, columnspan=2, padx=10, ipadx=100, pady=10)

# Luodaan pääikkunan entryt, labelit ja napit
enimi = Entry(root, width=30)
enimi.grid(row=0, column=1, padx=20, pady=(10, 0))
snimi = Entry(root, width=30)
snimi.grid(row=1, column=1, padx=20)
osoite = Entry(root, width=30)
osoite.grid(row=2, column=1, padx=20)
postinro = Entry(root, width=30)
postinro.grid(row=3, column=1, padx=20)
kaupunki = Entry(root, width=30)
kaupunki.grid(row=4, column=1, padx=20)
maa = Entry(root, width=30)
maa.grid(row=5, column=1, padx=20)
poista_entry = Entry(root, width=30)
poista_entry.grid(row=9, column=1)

enimi_label = Label(root, text="Etunimi")
enimi_label.grid(row=0, column=0, pady=(10, 0))
snimi_label = Label(root, text="Sukunimi")
snimi_label.grid(row=1, column=0)
osoite_label = Label(root, text="Osoite")
osoite_label.grid(row=2, column=0)
postinro_label = Label(root, text="Postinumero")
postinro_label.grid(row=3, column=0)
kaupunki_label = Label(root, text="Kaupunki")
kaupunki_label.grid(row=4, column=0)
maa_label = Label(root, text="Maa")
maa_label.grid(row=5, column=0)
poista_entry_label = Label(root, text="Valitse ID")
poista_entry_label.grid(row=9, column=0)

toimita_nappi = Button(root, text="Lisää tietue", command=toimita)
toimita_nappi.grid(row=6, column=0, columnspan=2, padx=10, ipadx=135, pady=10)
kysely_nappi = Button(root, text="Näytä tietueet", command=kysely)
kysely_nappi.grid(row=7, column=0, columnspan=2, padx=10, ipadx=127, pady=10)
poista_nappi = Button(root, text="Poista tietue", command=poista)
poista_nappi.grid(row=10, column=0, columnspan=2, padx=10, ipadx=131, pady=10)
muokkaa_nappi = Button(root, text="Päivitä tietue", command=muokkaa)
muokkaa_nappi.grid(row=11, column=0, columnspan=2, padx=10, ipadx=129, pady=10)

conn.commit()
conn.close()

mainloop()