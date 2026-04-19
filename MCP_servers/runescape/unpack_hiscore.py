def unpack_skill_item(type: str, listing: list) -> dict:
    skill_item = {}
    if type == 'skill':
        skill_item['type'] = 'skill'
        skill_item['ranking'] = listing[0]
        skill_item['level'] = listing[1]
        skill_item['exp'] = listing[2]
    return skill_item

def unpack_hiscore(input: str) -> dict:

    """Unpacks the hiscore body of text returned from the RuneScape hiscore API."""

    hiscores = {}
    listings = input.split('\n')

    for idx, line in enumerate(listings):
        listing = line.split(',')

        if idx == 0:
            hiscores['total_level'] = {
                'type': 'skill',
                'ranking': listing[0],
                'level': listing[1],
                'exp': listing[2],
            }

        elif idx == 1:
            hiscores['attack'] = {
                'type': 'skill',
                'ranking': listing[0],
                'level': listing[1],
                'exp': listing[2]
            }

        elif idx == 2:
            hiscores['defence'] = unpack_skill_item(type='skill', listing=listing)

        elif idx == 3:
            hiscores['strength'] = unpack_skill_item(type='skill', listing=listing)

    return hiscores
