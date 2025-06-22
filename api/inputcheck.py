def isvalidinput(input: dict) -> bool:
    # Check that every key is present and is correct type.
    if 'mandates' not in input.keys() or 'preferences' not in input.keys() or 'items' not in input.keys() or not isinstance(input['mandates'], list) or not isinstance(input['preferences'], list) or not isinstance(input['items'], int):
        return False
    # Check that every mandate is a integer
    for i in input['mandates']:
        if not isinstance(i, int):
            return False
    # Check that each party has it's preferences
    if len(input['preferences']) != len(input['mandates']):
        return False
    # Check that every preference is a list of values the size of number of items
    for pref in input['preferences']:
        if not isinstance(pref, list) or len(pref) != input['items']:
            return False
        for val in pref:
            if not isinstance(val, (int, float)):
                return False
    return True
