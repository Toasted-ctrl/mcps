def unpack_hiscore_item(type: str, listing: list) -> dict:
    item = {}
    if type == 'skill':
        item['type'] = 'skill'
        item['ranking'] = listing[0]
        item['level'] = listing[1]
        item['exp'] = listing[2]
    if type == 'activity':
        item['type'] = 'activity'
        item['ranking'] = listing[0]
        item['score'] = listing[1]
    return item

def unpack_hiscore(input: str) -> dict[str, dict[str, int]]:

    """Unpacks the hiscore body of text returned from the RuneScape hiscore API."""

    hiscore_items: list = [
        "Overall",
        "Attack",
        "Defence",
        "Strength",
        "Constitution",
        "Ranged",
        "Prayer",
        "Magic",
        "Cooking",
        "Woodcutting",
        "Fletching",
        "Fishing",
        "Firemaking",
        "Crafting",
        "Smithing",
        "Mining",
        "Herblore",
        "Agility",
        "Thieving",
        "Slayer",
        "Farming",
        "Runecrafting",
        "Hunting",
        "Construction",
        "Summoning",
        "Dungeoneering",
        "Divination",
        "Invention",
        "Archaeology",
        "Necromancy",
        "Bounty Hunter",
        "B.H. Rogues", 
        "Dominion Tower",
        "The Crucible",
        "Castle Wars games",
        "B.A. Attackers",
        "B.A. Defenders",
        "B.A. Collectors",
        "B.A. Healers",
        "Duel Tournament",
        "Mobilising Armies",
        "Conquest",
        "Fist of Guthix",
        "GG: Athletics",
        "GG: Resource Race",
        "WE2: Armadyl Lifetime Contribution",
        "WE2: Bandos Lifetime Contribution",
        "WE2: Armadyl PvP kills",
        "WE2: Bandos PvP kills",
        "Heist Guard Level",
        "Heist Robber Level",
        "CFP: 5 game average",
        "AF15: Cow Tipping",
        "AF15: Rats killed after the miniquest",
        "RuneScore",
        "Clue Scrolls Easy",
        "Clue Scrolls Medium",
        "Clue Scrolls Hard",
        "Clue Scrolls Elite",
        "Clue Scrolls Master",
        "League Points",
        "TEST",
        "TEST2"
    ]

    hiscores = {}
    listings = input.split('\n')
    print(len(listings))

    for idx, line in enumerate(listings):
        listing = line.split(',')
        if idx < 30:
            hiscores[hiscore_items[idx]] = unpack_hiscore_item(type='skill', listing=listing)

    return hiscores
