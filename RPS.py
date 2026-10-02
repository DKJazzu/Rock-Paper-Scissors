# persist opponent history and sequence counts across turns within a match
def player(prev_play, opponent_history=[], play_order={}):
    # reset retained state when a new match begins
    if not prev_play:
        opponent_history.clear()
        play_order.clear()
    else:
        opponent_history.append(prev_play)

    MAX_MEMORY = 5
    for length in range(2, MAX_MEMORY + 1):
        if len(opponent_history) >= length:
            sequence = "".join(opponent_history[-length:])
            play_order[sequence] = play_order.get(sequence, 0) + 1

    # predict the next move using the longest available historical context
    prediction = "P" 
    for length in range(MAX_MEMORY, 1, -1):
        if len(opponent_history) >= length - 1:
            context = "".join(opponent_history[-(length - 1):])
            potential_plays = [context + "R", context + "P", context + "S"]
            
            sub_order = {k: play_order.get(k, 0) for k in potential_plays}
            
            if max(sub_order.values()) > 0:
                prediction = max(sub_order, key=sub_order.get)[-1]
                break 

    ideal_response = {"P": "S", "R": "P", "S": "R"}
    return ideal_response[prediction]
