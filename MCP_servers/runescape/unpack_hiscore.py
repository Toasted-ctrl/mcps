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
            hiscores['defence'] = {
                'type': 'skill',
                'ranking': listing[0],
                'level': listing[1],
                'exp': listing[2]
            }

    return hiscores
