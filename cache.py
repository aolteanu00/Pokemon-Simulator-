from flask import request
import urllib, json, sqlite3

def runsqlcommand(command):
    DB_FILE = "data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(command)
    if "select" in command.lower():
        return c.fetchall()
    db.commit()
    db.close()

def cacheMoves():
    # c = "DROP TABLE moves"
    # runsqlcommand(c)
    # c = "CREATE TABLE moves (name TEXT, effect TEXT, category TEXT, type TEXT, pp INTEGER, dmg INTEGER, accuracy INTEGER)"
    # runsqlcommand(c)
    i = 1
    while i <= 165 :
        link = "https://pokeapi.co/api/v2/move/{}".format(i)
        request = urllib.request.Request(link)
        request.add_header('User-Agent', 'yes')
        u = urllib.request.urlopen(request)
        response = u.read()
        id = (json.loads(response)["id"])
        name = (json.loads(response)["name"]).replace("-", " ")
        eff = (json.loads(response)["effect_entries"][0]["short_effect"])
        eff = ((eff.replace("é", "e")).replace("\'", "\'\'")).replace("$effect_chance%", "{}")
        eff = eff.format(json.loads(response)["effect_chance"])
        dcl = (json.loads(response)["damage_class"]["name"])
        type = (json.loads(response)["type"]["name"])
        pp = (json.loads(response)["pp"])
        dmg = (json.loads(response)["power"])
        acc = (json.loads(response)["accuracy"])
        if dmg is None:
            dmg = -1
        if acc is None:
            acc = -1
        cmd = "SELECT * FROM moves"
        r = runsqlcommand(cmd)
        if len(r) > 0:
            cmd = "SELECT * FROM moves WHERE name = '{}'".format(name)
        q = runsqlcommand(cmd)
        if len(q) == 0:
            ins = "INSERT INTO moves VALUES({}, '{}', '{}', '{}', '{}', {}, {}, {})".format(id, name, eff, dcl, type, pp, dmg, acc)
            runsqlcommand(ins)
        i+=1

def cachePokemon():
    i = 1
    allPokemon = {}
    while i <= 151:
        thisPokemon = {}
        link = "https://pokeapi.co/api/v2/pokemon/{}".format(i)
        request = urllib.request.Request(link)
        request.add_header('User-Agent', 'yes')
        u = urllib.request.urlopen(request)
        response = u.read()
        pokemonInfo = json.loads(response)
        poke = json.loads(response)['name']
        thisPokemon['name'] = poke
        thisPokemon['pic'] =  pokemonInfo['sprites']['front_default']

        moves = {}
        #e = "DROP TABLE \"{}\"".format(n)
        #runsqlcommand(e)
        #d = "CREATE TABLE \"{}\" (move TEXT)".format(poke)
        # print(n)
        # print(d)
        # runsqlcommand(d)
        c = json.loads(response)["moves"]
        z = 0
        # a = "SELECT name FROM MOVES"
        # b = runsqlcommand(a)
        #print(b)
        while z < len(c):
            moves[z] = c[z]['move']['name'].replace("-", " ")
            # name = (c[z]['move']['name']).replace("-", " ")
            # num = int(((c[z]['move']['url']).replace("https://pokeapi.co/api/v2/move/", "")).replace("/", ""))
            # #url = c[z]['move']['url']
            # if num <= 165:
            #     cmd = "SELECT * FROM \"{}\"".format(n)
            #     r = runsqlcommand(cmd)
            #     if len(r) > 0:
            #         cmd = "SELECT * FROM \"{}\" WHERE move = '{}'".format(poke, name)
            #     q = runsqlcommand(cmd)
            #     if len(q) == 0:
            #         ins = "INSERT INTO \"{}\" VALUES('{}')".format(poke, name)
            #         #print(ins)
            #         runsqlcommand(ins)
            z += 1
        thisPokemon['moves'] = moves
        allPokemon[i] = thisPokemon
        i += 1
    return allPokemon

def getMoves(name):
    c = "SELECT * FROM {}".format(name)
    r = runsqlcommand(c)
    arr = []
    for i in r:
        arr.append(i[0])
    return(arr)
