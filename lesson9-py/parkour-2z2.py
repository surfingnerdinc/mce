# ustawiamy losowe zmiany w spawnie na 0. Przy okazji to informacja czy kod się załadował
player.execute("/gamerule spawnRadius 0")
# zmienne pomocnicze dzięki nim dany etap będzie tworzony raz w ramach jednej rozgrywki
etap1=False
etap2=False
etap3=False
etap4=False

# budujemy schody oraz pierwszą platformę ładującą etap 1
def parkour():
    # aktualne miejsce odrodzenia gracza, zmienne w zależności od checkpointu, który zaliczymy
    player.execute("/setworldspawn " + player.position())
    # teleportujemy konstruktor w okolice gracza
    builder.teleport_to(pos(5, 0, 0))
    # obracamy
    builder.face(EAST)
    # oznaczamy bieżącą pozycję konstruktora
    builder.mark()
    # konstruktor przemieszcza się w przód, górę i lewo
    builder.shift(70, 70, 0)
    #tworzymy linie z danego bloku od znaku (mark) do obecnej pozycji
    builder.line(PURPUR_STAIRS)
    builder.mark()
    builder.shift(2, 0, -4)
    # konstruktor wypełnia przestrzeń blokami od znaku(mark) do obecnej pozycji
    builder.fill(DIAMOND_BLOCK)
player.on_chat("start", parkour)

# pętla sterująca ładowaniem etapów oraz system checkpoint
while True:
    if blocks.test_for_block(DIAMOND_BLOCK, pos(0, -1, 0)) and not etap1:
        # generujemy nowy spawn
        player.execute("/setworldspawn " + player.position())
        etap1 = True
        etap_1_i_2(STONE,GOLD_BLOCK)
    elif blocks.test_for_block(GOLD_BLOCK, pos(0, -1, 0)) and not etap2:
        player.execute("/setworldspawn " + player.position())
        etap2 = True
        etap_1_i_2(GLOWSTONE,BEDROCK)
    elif blocks.test_for_block(BEDROCK, pos(0, -1, 0)) and not etap3:
        player.execute("/setworldspawn " + player.position())
        etap3 = True
        etap_3()
    elif blocks.test_for_block(MOSS_STONE, pos(0, -1, 0)) and not etap4:
        player.execute("/setworldspawn " + player.position())
        etap4 = True
        etap_4()
        # dodajemy break by pętla nie spowalniała działania reszty funkcji
        break

      
def etap_1_i_2(rodzaj_toru,rodzaj_checkpointu):
    # decydujemy jaka będzie długość toru (losujemy, by była różnica między poziomami)
    for i in range(randint(10, 15)):
        # ustawiamy zmienne służące do generowania przesunięć do kolejnego bloku.
        # jeśli poziom jest za łatwy wystarczy zwiększyć przod z 3 do 4 lub bok z -1,1 do -2,2 
        przod = randint(2, 3)
        bok = randint(-1, 1)
        wysokosc = randint(-1, 1)
        # losujemy długość platformy (0 to 1 blok)
        dlugosc = randint(0, 3)
        # przesuwamy się do kolejnej platformy
        builder.shift(przod, wysokosc, bok)
        # budujemy platformę
        builder.mark()
        builder.move(FORWARD, dlugosc)
        builder.line(rodzaj_toru)
    # budujemy checkpoint
    builder.mark()
    builder.shift(2, 0, -4)
    builder.fill(rodzaj_checkpointu)

def etap_3():
    # tworzymy zmienną, która mówi jak długi będzie tor z netherracku
    koniec = 66
    #tworzymy koło ze szlamu
    shapes.circle(SLIME_BLOCK, pos(4, -30, 0), 1, Axis.Y, ShapeOperation.REPLACE)
    builder.shift(4, -32, 0)
    builder.mark()
    #ustawiamy pozycję pierwotną później wrócimy w to miejsce konstruktorem i będziemy dodawać ogień
    builder.set_origin()
    builder.move(FORWARD, koniec)
    builder.line(NETHERRACK)
    #wracamy aby dodać ogień
    builder.teleport_to_origin()
    builder.move(UP, 1)
    builder.set_origin()
    # tworzymy zmienną, która będzie liczyć jak daleko ma pojawić się ogień
    ogien = 0
    while True:
        ogien += randint(3,6)
        if (ogien <= koniec):
            builder.move(FORWARD, ogien)
            builder.place(FIRE)
            builder.teleport_to_origin()
        else:
            builder.move(FORWARD, koniec+1)
            break
    #budowa platformy
    builder.mark()
    builder.shift(2, 0, -4)
    builder.fill(MOSS_STONE)


def etap_4():
    #projektujemy skok
    builder.shift(0, -30, -6)
    #budujemy studnię z wodą
    builder.mark()
    builder.shift(2, 2, 2)
    builder.fill(BRICKS)
    builder.shift(-1, 0, -1)
    builder.place(WATER)
    builder.move(FORWARD, 4)
    # budujemy platformę
    builder.set_origin()
    builder.shift(-2,40,0)
    builder.mark()
    builder.shift(2, 0, 4)
    builder.fill(SEA_LANTERN)
    platforma = builder.position()
    #pętla tworząca schody spiralne kończy swoje działanie kiedy gracz stanie na ostatniej platformie
    while not blocks.test_for_block(SEA_LANTERN, pos(0, -1, 0)):
        builder.teleport_to_origin()
        #budowanie schodów w każdej chwili może być przerwane kiedy gracz stanie na ostatniej platformie
        for i in range(40):
            if not blocks.test_for_block(SEA_LANTERN, pos(0, -1, 0)):
                builder.place(POLISHED_GRANITE)
                builder.shift(1,1,0)
                builder.turn(RIGHT_TURN)
            else:
                break
        builder.teleport_to_origin()
        loops.pause(5000)
        #podmieniamy schody na blok magmy
        for i in range(40):
            if not blocks.test_for_block(SEA_LANTERN, pos(0, -1, 0)):
                builder.place(MAGMA_BLOCK)
                builder.shift(1,1,0)
                builder.turn(RIGHT_TURN)
                loops.pause(500)
            else:
                break
    builder.teleport_to(platforma)
 #gracz otrzymuje wiaderko z wodą, wykonujemy water bucket challange spadamy w przepaść i klikamy PPM tak aby wylać wodę pod siebie i zamortyzować upadek
    while True:
        if blocks.test_for_block(SEA_LANTERN, pos(0, -1, 0)):
            player.execute("/clear")
            player.execute("/give @p water_bucket 1")
            loops.pause(5000)
