
def is_valid_path(board, path, words):
    """
    This function checks if the route is a valid route that describes a word that exists in the word collection
    :param board: board game
    :param path: bath on the game board.
    :param words: a list of words
    :return: the word if the path is legal, else None
    """
    if len(path) != len(set(path)):
        return None
    for i in path:
        if i[0] >= len(board) or i[1] >= len(board[0]) or i[0] < 0 or i[1] < 0:
            return None
    for i in range(len(path)-1):
        if path[i+1][0] > path[i][0] + 1 or path[i+1][1] > path[i][1] +1 or path[i+1][0] +1 < path[i][0] or\
         path[i+1][1]+1 < path[i][1]:
            return None
    word = word_in_words(board, path, words)
    return word


def word_in_words(board, path, words):
    """
    This function chick if the word is in the list of words
    :param board: board game
    :param path: bath on the game board.
    :param words: a list of words
    :return: the word if it in the list, else None
    """
    word = ""
    for index in path:
        word += board[index[0]][index[1]]
    if word in words:
        return word
    else:
        return None


def find_length_n_paths(n, board, words):
    """
    This function find the path of length n.
    :param n: an int
    :param board: board game
    :param words: a list of words
    :return:  a list of all n-length paths that describe words in the word collection
    """
    path = []
    for index1 in range(len(board)):
        for index2 in range(len(board[0])):
            path = path + find_length_n_paths_helper(n, board, words, [] + [(index1, index2)], [], index1, index2)
    return path


def find_length_n_paths_helper(n, board, words, lst_of_tup, lst_of_paths, i, j):
    """
    This function find the path of length n.
    :param n: an int
    :param board: board game
    :param words: a list of words
    :param lst_of_tup: a list that contains tuple of index
    :param lst_of_paths: a 2 dimensional list that contain a list of index tuple
    :param i: the x coordination of the word
    :param j: the y coordination of the word
    :return: a list of all n-length paths that describe a word in words
    """
    if len(lst_of_tup) == n:
        if is_valid_path(board, lst_of_tup, words):
            lst_of_paths.append(lst_of_tup)
            return lst_of_paths
        else:
            return []
    neighbors_lst = find_neighbors(board, i, j)
    for k in neighbors_lst:
        if k not in lst_of_tup:
            find_length_n_paths_helper(n, board, words, lst_of_tup + [k], lst_of_paths, k[0], k[1])
    return lst_of_paths


def find_neighbors(board, i, j):
    """
    This function find the neighbors of a (i, j) coordination
    :param board: a board game
    :param i: the x coordination of the word
    :param j: the y coordination of the word
    :return: a list of all the indexes that are next to (i, j)
    """
    lst_neighbors = []
    for row in range(i-1, i+2):
        if row < 0 or row >= len(board):
            continue
        for col in range(j-1, j+2):
            if col < 0 or col >= len(board[0]):
                continue
            lst_neighbors.append((row, col))
    # lst_neighbors.remove((i, j))
    return lst_neighbors


def find_length_n_words(n, board, words):
    """
    This function find the path that fit to a word of length n.
    :param n: an int
    :param board: board game
    :param words: a list of words
    :return: a list of  paths that describe words of length n
    """
    path = []
    for index1 in range(len(board)):
        for index2 in range(len(board[0])):
            path = path + find_length_n_words_helper(n, board, words, [] + [(index1, index2)], [], index1, index2, ""+board[index1][index2],None)
    return path


def find_length_n_words_helper(n, board, words, lst_of_tup, lst_of_paths, i, j, word,d):
    """
    This function find the path that fit to a word of length n.
    :param n: an int
    :param board: board game
    :param words: a list of words
    :param lst_of_tup: a list that contains tuple of index
    :param lst_of_paths: a 2 dimensional list that contain a list of index tuple
    :param i: the x coordination of the word
    :param j: the y coordination of the word
    :param word: a word
    :param d: a dictionary
    :return: a list of  paths that describe words of length n
    """
    if len(word) == n:
        if is_valid_path(board, lst_of_tup, words):
            if d is not None:
                if word not in d:
                    d[word] = lst_of_tup
                else:
                    if len(d[word]) < len(lst_of_tup):
                        d[word] = lst_of_tup
            else:
                lst_of_paths.append(lst_of_tup)
                return lst_of_paths
        else:
            return []
    neighbors_lst = find_neighbors(board, i, j)
    for k in neighbors_lst:
        if k not in lst_of_tup:
            find_length_n_words_helper(n, board, words, lst_of_tup + [k], lst_of_paths, k[0], k[1], word+board[k[0]][k[1]],d)
    return lst_of_paths


def max_score_paths(board, words):
    """
    This function find the paths that have the max score.
    :param board: board game
    :param words: a list of words
    :return: a list of paths
    """
    dic = {}
    len_lst = []
    for word in words:
        n = len(word)
        if n not in len_lst:
            len_lst.append(n)
    for num in len_lst:
        max_helper(num, board, words, dic)
    all_paths = list(dic.values())
    return all_paths


def max_helper(n, board, words, dic):
    """
    This function calling find_length_n_words_helper function.
    :param n: int
    :param board: board game
    :param words: a list of words
    :param dic: a dictionary
    """
    for index1 in range(len(board)):
        for index2 in range(len(board[0])):
            find_length_n_words_helper(n, board, words, [] + [(index1, index2)], [], index1, index2, ""+board[index1][index2],dic)


