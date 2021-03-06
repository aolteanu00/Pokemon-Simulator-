from flask import Flask, render_template, session, request, jsonify, redirect, url_for, flash
import ast
import urllib
import json
import os
import math
import sqlite3
from cache import runsqlcommand, cacheMoves, cachePokemon
import databaseUtils as help

allPokemon = cachePokemon()
allTeams = {}
app = Flask(__name__) #create instance of class Flask
app.secret_key = os.urandom(32)


@app.route("/battle") #assign following fxn to run when root route requested
def battle():

    print(__name__) #where will this go?

    # team1 = {}
    # team2 = {}
    # teams = {}
    # teams['team1'] = team1
    # teams['team2'] = team2
    #
    # teams = {}
    #
    # x = 1
    # while (x < 7):
    #     team1[x - 1] = getPokemonByID(x, "back", [0, 1, 2, 3])
    #     team2[x - 1] = getPokemonByID(7 * x, "front", [0, 1, 2, 3])
    #     x = x + 1
    # teams['team1'] = team1
    # teams['team2'] = team2
    # teamsJson = json.dumps(teams)
    # #print(teamsJson)
    teams = {}
    teams['team1'] = {}
    teams['team2'] = {}
    team1 = allTeams[int(request.args['team1'])]
    team2 = allTeams[int(request.args['team2'])]
    #print(request.args['team1'])
    print(team2)
    newTeam1 = {}
    newTeam2 = {}
    for i in team1:
        newTeam1[i] = getPokemonByID(team1[i]['id'], 'back', team1[i]['moves'])
    for i in team2:
        newTeam2[i] = getPokemonByID(team2[i]['id'], 'front', team2[i]['moves'])
    teams['team1'] = newTeam1
    teams['team2'] = newTeam2
    print(teams)
    teamsJson = json.dumps(teams)
    return render_template("testBattle.html", teams = teams, teamsJson = teamsJson)


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/setupBattle")
def setupBattle():

    return render_template("setup.html", teams = allTeams)

@app.route("/addUser")
def addUser():
    username = request.args["username"]
    password = request.args["password"]
    #print(username)
    #print(password)
    help.register(username,password)
    return render_template("login.html")

@app.route("/auth")
def auth():
    #Should check user and pass against the database and either send user abck to login or to welcome
    username = request.args["username"]
    password = request.args["password"]
    #print(username)
    #print(password)
    if help.validate(username,password) == 1:
        flash("Wrong username or password!")
        return redirect(url_for("first"))
    if help.validate(username,password) == 2:
        flash("Wrong username or password!")
        return redirect(url_for("first"))
    else:
        session["username"] = username
        #print("Logged into account with username: " + username)
        return render_template("index.html")

@app.route("/welcome")
def landing():
    #should get all of the user's data from database
    #should send this data to html file
    #If the user is logging in for the first time, it should gift them their first pokemon
    if "team" in request.args:

        team = json.loads(request.args["team"])
        # if len(allSavedTeams) == 0:
        #     numberSavedTeams = 0
        #print(team)
        totalTeams = len(allTeams)
        allTeams[totalTeams] = team
    #print(allTeams)
    return render_template("index.html")

@app.route("/logout")
def logout():
    print("Logged out of session (username " + session["username"] + ")")
    session.clear()
    return redirect(url_for("first"))


@app.route("/build")
def build():
    allPokemonJson = json.dumps(allPokemon)
    return render_template("build.html", allPokemon = allPokemon, allPokemonJson = allPokemonJson)

@app.route("/")
def first():
    help.createUsers()
    help.createTeams()
    if "username" in session:
        return redirect(url_for("welcome"))
    else:
        return render_template("login.html")

""" @app.route("/setupBattle")
def setupBattle():
    #takes in selected pokemon for battle
    #checks whether battle is set for pvp or pvNPC
    #depending on this, sends user to pvp.html or game.html
    return redirect(url_for("game"))

@app.route("/game")
def game():
    #gets user's selected pokemon
    #run game in javascript
    #oof
    return render_template("game.html")

@app.route("/pvp")
def pvp():
    #should get users selected pokemon
    #runs game in JS
    return render_template("pvp.html") """

def getPokemonByID(i, direction, moveslist):
    link = "https://pokeapi.co/api/v2/pokemon/" + str(i)
    request = urllib.request.Request(link)
    request.add_header('User-Agent', 'yes')
    u = urllib.request.urlopen(request)
    response = u.read()
    teammate = json.loads(response)





    teammateDict = {}
    x = 0
    moves = {}
    stats = {}

    while x < 4:
        link = teammate['moves'][moveslist[x]]["move"]['url']
        request = urllib.request.Request(link)
        request.add_header('User-Agent', 'yes')
        u = urllib.request.urlopen(request)
        response = u.read()
        apimove = json.loads(response)

        move = {
        "accuracy":apimove['accuracy'],
        "power":apimove['power'],
        "dmgclass":apimove['damage_class']['name'],
        "type":apimove['type']['name'],
        'name':apimove['name']
        }
        moves[x] = move
        x = x + 1
    x = 0
    while x < 6:
        stats[teammate['stats'][x]['stat']['name']] = teammate['stats'][x]['base_stat']
        x = x + 1
    stats['startingHp'] = stats['hp']
    teammateDict['moves'] = moves
    if (direction == "front"):
        teammateDict['pic'] = teammate['sprites']['front_default']
    else:
        teammateDict['pic'] = teammate['sprites']['back_default']
    teammateDict['type'] =  teammate['types'][0]['type']['name']
    teammateDict['stats'] = stats
    teammateDict['name'] = teammate['forms'][0]['name']
    return teammateDict

if __name__ == "__main__":
    app.debug = True
    app.run()
