import operator
import matplotlib.pyplot as plt
import networkx as nx
from neo4j.v1 import GraphDatabase, basic_auth
import nxneo4j


# 定义数据
def define_data(G):
    G.add_nodes_from(["John", "Mary", "Jill", "Todd",
                  "iPhone5", "Kindle Fire", "Fitbit Flex Wireless", "Harry Potter", "Hobbit"])
    G.add_edges_from([
        ("John", "iPhone5"),
        ("John", "Kindle Fire"),
        ("Mary", "iPhone5"),
        ("Mary", "Kindle Fire"),
        ("Mary", "Fitbit Flex Wireless"),
        ("Jill", "iPhone5"),
        ("Jill", "Kindle Fire"),
        ("Jill", "Fitbit Flex Wireless"),
        ("Todd", "Fitbit Flex Wireless"),
        ("Todd", "Harry Potter"),
        ("Todd", "Hobbit"),
    ])

# 利用 neo4j生成Graph对象
def neo4j_pagerank():
    G = nxneo4j.Graph(GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "123456")))
    define_data(G)

    pr = nxneo4j.pagerank(G)
    pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)

    print("PageRank")
    for item, score in pr:
        print(item, score)

    cluster = nxneo4j.label_propagation_communities(G)
    print("Clustering Coefficient: {0}".format(cluster))

# 利用networkx生成Graph对象
def nx_pagerank():
    G = nx.Graph()
    define_data(G)

    nx.draw(G)
    plt.show()

    pr = nx.pagerank(G)
    pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)

    print("PageRank")

    for item, score in pr:
        print(item, score)

    print("Personalised PageRank")

    ppr = nx.pagerank(G, personalization={"Mary": 1})
    ppr = sorted(ppr.items(), key=operator.itemgetter(1), reverse=True)

    for item, score in ppr:
        print(item, "{0:.10f}".format(score))

    print(nx.clustering(G))


if __name__ == '__main__':
    # nx_pagerank()
    neo4j_pagerank()