import os 
from typing import Optional
from langchain_core.tools import tool
from espn_api.football import League

def get_espn_leagues(league_team_info: tuple, year: int, espn_s2: str, swid: str) -> dict:
    "A way to get your leagues from your config file without sharing your espn info with everyone"
    league_dict = {}
    try:
        for tup in league_team_info:
            name, id, tm_id = tup
            league_dict[name] = {}
            league_dict[name]['league'] = League(league_id=id,year=year,espn_s2=espn_s2,swid=swid)
            league_dict[name]['tm_id'] = tm_id
    except:
        print("""Your config file may not be set up correctly. It needs to contain a variable called league_team_info that is"""
               """list of tuples: (name:str, id:int, tm_id:int)""")
    
    return league_dict

def check_league_roster(league: object, tm_id: int) -> str:
    "Check ESPN for the roster of a specific league"
    players = []
    for player in league.teams[tm_id].roster:
        players.append(player.name)
    return players

def get_rosters(league_dict: dict) -> str:
    "Iterate through a dictionary that contains multiple leagues and return a str with teams and their rosters"

    output_str = "" 
    for name in sorted(league_dict.keys()):
        output_str += f"League: {name} \n"
        output_str += "Players: \n"
        l = league_dict[name]['league']
        l_id = league_dict[name]['tm_id']
        l_players = check_league_roster(l, l_id)
        for player in l_players:
            output_str += player + ", "
        output_str += "\n"
    return output_str

def get_free_agents(league_dict: dict) -> str:
    "Return free agents in all leagues"
    output_str = ""
    for name in sorted(league_dict.keys()):
        output_str += f"Free Agents in League: {name} \n"
        l = league_dict[name]['league']
        l_fa = l.free_agents()
        for player in l_fa:
            output_str += player.name + ", "
    return output_str

def get_roster_and_projections(league_dict: dict) -> str:
    "Iterate through a dictionary that contains multiple leagues and return a str with teams and their rosters"

    output_str = "" 
    for name in sorted(league_dict.keys()):
        output_str += f"League: {name} \n"
        output_str += "Players and Projected Stats: \n"
        l = league_dict[name]['league']
        l_id = league_dict[name]['tm_id']
        l_players = check_league_roster_and_stats(l, l_id)
        for player,proj in l_players:
            output_str += player + " " + str(proj) + ", "
        output_str += "\n"
    return output_str


def check_league_roster_and_stats(league: object, tm_id: int) -> str:
    "Check ESPN for the roster of a specific league"
    players = []
    for player in league.teams[tm_id].roster:
        players.append((player.name, player.stats))
    return players