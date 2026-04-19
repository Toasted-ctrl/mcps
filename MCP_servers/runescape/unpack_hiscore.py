def unpack_hiscore(input: str) -> dict:

    hiscores = {}
    listings = input.split(sep='\n')
    for i in listings:
        listing = i.split(sep=',')
        if i is 0:
            hiscores['total_level'] = {}
            hiscores['total_level']['type'] = 'skill'
            hiscores['total_level']['ranking'] = listing[0]
            hiscores['total_level']['level'] = listing[1]
            hiscores['total_level']['exp'] = listing[2]

    return hiscores
