import numpy as np


def find_set(elem, parent):
    if elem == parent[int(elem)]:
        return elem
    parent[elem] = find_set(parent[elem], parent)
    return parent[elem]


def union_sets(first_elem, second_elem, rank, parent):
    first_elem = find_set(first_elem, parent)
    second_elem = find_set(second_elem, parent)
    if first_elem != second_elem:
        if rank[first_elem] < rank[second_elem]:
            first_elem, second_elem = second_elem, first_elem
        parent[second_elem] = first_elem
        if rank[first_elem] == rank[second_elem]:
            rank[first_elem] += 1


def clustering(vectors, n_clusters: int, metric=2):
    if n_clusters > len(vectors) or n_clusters < 1:
        raise Exception(
            "number of clusters can't be more than size number of elements in array or less than zero"
        )
    np_vectors = np.array(vectors, dtype="float64")
    list_of_distances = []
    num_clusters = len(vectors)
    parent = np.arange(len(vectors))
    rank = np.zeros(len(vectors))
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            distance = [i, j, np.linalg.norm(np_vectors[i] - np_vectors[j], metric)]
            list_of_distances.append(distance)
    list_of_distances.sort(key=lambda x: x[2])
    for i in range(len(list_of_distances)):
        if num_clusters == n_clusters:
            break
        if find_set(list_of_distances[i][0], parent) != find_set(
            list_of_distances[i][1], parent
        ):
            union_sets(list_of_distances[i][0], list_of_distances[i][1], rank, parent)
            num_clusters -= 1
    clusters = list()
    for elem in range(len(vectors)):
        clusters.append(find_set(elem, parent))
    return clusters


vectors = [[1, 2], [46, 78], [3, 4], [5, 9], [123, 59]]
matrices = [
    [[1, 2, 3], [4, 5, 6]],
    [[152, 223, 3243], [37, 235, 124]],
    [[34, 42, 25], [42, 23, 98]],
    [[1, 2, 3], [0, 0, 0]],
]
print(clustering(vectors, 3))
print(clustering(matrices, 3))
