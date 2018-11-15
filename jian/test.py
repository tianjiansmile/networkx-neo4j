import networkx as nx
from neo4j.v1 import GraphDatabase, basic_auth
import matplotlib.pyplot as plt
import operator
import nxneo4j
#  对比 networkx 和neo4j 的图算法
neo4j_functions = {
    "betweenness_centrality": nxneo4j.betweenness_centrality,
    "closeness_centrality": nxneo4j.closeness_centrality,
    "harmonic_centrality": nxneo4j.harmonic_centrality,
    "pagerank": nxneo4j.pagerank,
    "triangles": nxneo4j.triangles,
    "clustering": nxneo4j.clustering,
    "average_clustering": nxneo4j.average_clustering,
    "label_propagation_communities": nxneo4j.community.label_propagation_communities,
    "shortest_path": nxneo4j.shortest_path,
    "connected_components": nxneo4j.connected_components,
    "number_connected_components": nxneo4j.number_connected_components
}

# 将list按第location个位置排序
def sort_list(alog,location):
    return  sorted(alog.items(), key=operator.itemgetter(location), reverse=True)

def execute_graph(G, functions,type):

    if type == 2:
        # 在屏幕画出图像
        nx.draw(G)
        # plt.savefig("ba.png")  # 输出方式1: 将图像存为一个png格式的图片文件
        plt.show()

    # print("Number of nodes: {0}".format(G.number_of_nodes()))

    # 网络中任意两个节点的所有最短路径，如果这些最短路径中有很多条都经过了某个节点，那么就认为这个节点的Betweenness Centrality高
    between = functions["betweenness_centrality"]
    print("Betweenness : {0}".format(sort_list(between(G),1)))

    # 如果节点到图中其它节点的最短距离都很小，那么我们认为该节点的Closeness Centrality高,
    # 意味着这个节点从几何角度看是出于图的中心位置
    closeness = functions["closeness_centrality"]
    closs = sort_list(closeness(G, wf_improved=True),1)
    print("Closeness (WF): {0}".format(closs))
    # print("Closeness (no WF): {0}".format(sort_list(closeness(G, wf_improved=False),1)))
    # print("Closeness (one node): {0}".format(closeness(G, 'Todd', wf_improved=False)))

    # 接近中心度的代替方案
    harmonic = functions["harmonic_centrality"]
    # print("Harmonic (default): {0}".format(sort_list(harmonic(G),1)))
    # print("Harmonic (nbunch): {0}".format(harmonic(G, nbunch=[1, 2, 3])))
    #
    # pagerank = functions["pagerank"]
    # print("PageRank: {0}".format(sort_list(pagerank(G),1)))
    #
    # triangles = functions["triangles"]
    # print("Triangles: {0}".format(triangles(G)))
    #
    # clustering = functions["clustering"]
    # print("Clustering Coefficient: {0}".format(clustering(G)))
    #
    # average_clustering = functions["average_clustering"]
    # print("Average Clustering Coefficient: {0}".format(average_clustering(G)))
    #
    lpa = functions["label_propagation_communities"]
    print("Label Propagation: {0}".format(list(lpa(G))))

    shortest_path = functions["shortest_path"]
    print("Shortest Path: {0}".format(shortest_path(G, 'Todd', 'John', 'weight')))
    # print("Single Shortest Path: {0}".format(shortest_path(G, 'Todd')))
    #
    connected_components = functions["connected_components"]
    print("Connected Components: {0}".format(list(connected_components(G))))
    #
    number_connected_components = functions["number_connected_components"]
    print("# Connected Components: {0}".format(number_connected_components(G)))



if __name__ == '__main__':
    print("Neo4j")
    # 利用neo4j数据库 来创建图，并且做各种图计算
    execute_graph(nxneo4j.Graph(GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "123456"))),
                  neo4j_functions,1)

    print()

    # print("networkx")
    # # 利用networkx 来创建图，并且做各种图计算
    # execute_graph(nx.Graph(), networkx_functions,2)
