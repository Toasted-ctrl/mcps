def unpack_hiscore_item(type: str, listing: list) -> dict:
    item = {}
    if type == 'skill':
        item['type'] = 'skill'
        item['ranking'] = listing[0]
        item['level'] = listing[1]
        item['exp'] = listing[2]
    return item

def unpack_hiscore(input: str) -> dict:

    """Unpacks the hiscore body of text returned from the RuneScape hiscore API."""

    hiscores = {}
    listings = input.split('\n')

    for idx, line in enumerate(listings):
        listing = line.split(',')

        if idx == 0:
            hiscores['total_level'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 1:
            hiscores['attack'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 2:
            hiscores['defence'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 3:
            hiscores['strength'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 4:
            hiscores['constitution'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 5:
            hiscores['ranged'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 6:
            hiscores['prayer'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 7:
            hiscores['magic'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 8:
            hiscores['cooking'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 9:
            hiscores['woodcutting'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 10:
            hiscores['fletching'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 11:
            hiscores['fishing'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 12:
            hiscores['firemaking'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 13:
            hiscores['crafting'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 14:
            hiscores['smithing'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 15:
            hiscores['mining'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 16:
            hiscores['herblore'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 17:
            hiscores['agility'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 18:
            hiscores['thieving'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 19:
            hiscores['slayer'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 20:
            hiscores['farming'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 21:
            hiscores['runecrafting'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 22:
            hiscores['hunting'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 23:
            hiscores['construction'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 24:
            hiscores['summoning'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 25:
            hiscores['dungeoneering'] = unpack_hiscore_item(type='skill', listing=listing)
        
        elif idx == 26:
            hiscores['divination'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 27:
            hiscores['invention'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 28:
            hiscores['archaeology'] = unpack_hiscore_item(type='skill', listing=listing)

        elif idx == 29:
            hiscores['necromancy'] = unpack_hiscore_item(type='skill', listing=listing)

    return hiscores
