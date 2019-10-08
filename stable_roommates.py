def get_ranking_matrix(preference):
    rank = [[None for j in range(len(preference))] for i in range(len(preference))]

    for i in range(len(preference)):
        for j in range(len(preference[i])):
            rank[i][preference[i][j]] = j
    
    return rank

def stable_roommates_phase_1(preference, rank):
    proposal = [None for x in range(len(preference))]
    first = [0 for x in range(len(preference))]
    last = [len(x) for x in preference]
    to_process = [x for x in range(len(preference))]
    
    while len(to_process) > 0:
        i = to_process[0]
        
        # update first pointer if necessary
        while preference[i][first[i]] == None:
            first[i] += 1
            
        top_pick = preference[i][first[i]]
        
        # top pick hasn't been proposed to yet, so they accept
        if proposal[top_pick] == None:
            proposal[top_pick] = i
            
            match_rank = preference[top_pick].index(i)
            
            # all candidates worse than i are rejected, must remove top_pick from their preference list
            for x in range(match_rank+1, last[top_pick]):
                reject = preference[top_pick][x]
                preference[reject][rank[reject][top_pick]] = None
            
            # update last pointer
            last[top_pick] = match_rank
            del to_process[0]
            
            continue
        
        curr_match_idx = rank[top_pick][proposal[top_pick]]
        potential_match_idx = rank[top_pick][i]
        
        if curr_match_idx < potential_match_idx: # current matching is preferred, i is rejected
            preference[top_pick][potential_match_idx] = None
            
            first[i] += 1 # start at next spot
            
            continue
        else: # accept proposal, so old match has to return to their preference list again
            preference[top_pick][curr_match_idx] = None
            
            # old match is rejected by top_pick, must update their list
            top_pick_idx = rank[proposal[top_pick]][top_pick]
            preference[proposal[top_pick]][top_pick_idx] = None
            
            del to_process[0]
            # add old match to to_process
            to_process.insert(0, proposal[top_pick])
            
            proposal[top_pick] = i
            last[top_pick] = potential_match_idx
    
    return first, last, preference

def clean_preferences(first, last, preferences):
    for i in range(len(preferences)):
        for j in range(len(preferences[i])):
            if j < first[i] or j > last[i]:
                preferences[i][j] = None

    return preferences

def find_second_favorite(i, first, last, pref):
    count = 0
    for j in range(first[i], last[i]+1):
        if not pref[j] == None:
            count += 1
        elif count == 0:
            first[i] += 1
        if count == 2:
            return pref[j]
    return None

def find_rotation(i, p, q, first, last, preferences):
    second_favorite = find_second_favorite(p[i], first, last, preferences[p[i]])
    next_p = preferences[second_favorite][last[second_favorite]]
    
    if next_p in p:
        # rotation found!
        j = p.index(next_p)
        q[j] = second_favorite
                
        return p[j:], q[j:]

    q.append(second_favorite)
    p.append(next_p)
    return find_rotation(i+1, p, q, first, last,  preferences)

def eliminate_rotation(p, q, first, last, preferences, rank):
    for i in range(len(p)):
        # q_i rejects p_i so that p_i proposes to q_i+1
        preferences[p[i]][rank[p[i]][q[i]]] = None
        
        # all successors of p_i-1 are removed from q_i's list, and q_i is removed from their lists
        for j in range(rank[q[i]][p[i-1]]+1, last[q[i]]):
            reject = rank[q[i]].index(j) #preferences[q[i]][j]
            preferences[reject][rank[reject][q[i]]] = None
            
        last[q[i]] = rank[q[i]][p[i-1]]

def stable_roommates_phase_2(first, last, preferences, rank):
    while True:
        p, q = None, None
        # find first p_0 to get a rotation from
        # preference list of p_0 must contain at least 2 elements
        for i in range(len(preferences)):
            if last[i] - first[i] > 0 and find_second_favorite(i, first, last, preferences[i]) != None:
                p, q = find_rotation(0, [i], [None], first, last, preferences)
                break
        
        if not p and not q:
            return preferences
        
        # eliminate rotation
        eliminate_rotation(p, q, first, last, preferences, rank)

def match_roommates(preferences):
    rank = get_ranking_matrix(preferences)
    first, last, preferences = stable_roommates_phase_1(preferences, rank)
    stable_roommates_phase_2(first, last, preferences, rank)
    clean_preferences(first, last, preferences)
    
    matches = []
    length = len(preferences)
    visited = set()
    i = 0
    
    for i in range(len(preferences)):
        if not i in visited:
            pair = (i, preferences[i][last[i]])
            visited.add(last[i])
            matches.append(pair)
    
    return matches

preferences = [[2, 3, 1, 5, 4], [5, 4, 3, 0, 2], [1, 3, 4, 0, 5], [4, 1, 2, 5, 0], [2, 0, 1, 3, 5], [4, 0, 2, 3, 1]]

print(match_roommates(preferences))