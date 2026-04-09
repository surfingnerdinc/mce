# ustawiamy losowe zmiany w spawnie na 0. Przy okazji to informacja czy kod się załadował
player.execute("/gamerule spawnRadius 0")
# zmienne pomocnicze dzięki nim dany etap będzie tworzony raz w ramach jednej rozgrywki
etap1=False
etap2=False
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

