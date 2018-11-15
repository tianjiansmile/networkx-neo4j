from neo4j.v1 import GraphDatabase, basic_auth

import nxneo4j

# 创建基础社交网络，merge 默认不存在时创建
create_friends_query = """\
MERGE (mark:Person {name: "Mark"})
MERGE (karin:Person {name: "Karin"})
MERGE (michael:Person {name: "Michael"})
MERGE (ryan:Person {name: "Ryan"})
MERGE (jennifer:Person {name: "Jennifer"})
MERGE (will:Person {name: "Will"})

MERGE (mark)-[:FRIENDS]->(karin)
MERGE (mark)-[:FRIENDS]->(ryan)
MERGE (ryan)-[:FRIENDS]->(michael)
"""


def cypher():
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "123456"))

    with driver.session() as session:
        session.run(create_friends_query)

    config = {
        "node_label": "Person",
        "relationship_type": "FRIENDS",
        "identifier_property": "name"
    }

    G = nxneo4j.Graph(driver, config)

    print(nxneo4j.betweenness_centrality(G))
    # print(nxneo4j.closeness_centrality(G))

    config = {
        "node_label": """\
        MATCH (p:Person) RETURN id(p) AS id
        """,
        "relationship_type": """\
        MATCH (p1:Person)-[:ACTED_IN]-(p2:Person)
        RETURN id(p1) AS source, id(p2) AS target
        """,
        "identifier_property": "name",
        "graph": "cypher"
    }

    G = nxneo4j.Graph(driver, config)
    #
    print(nxneo4j.betweenness_centrality(G))
    # print(nxneo4j.closeness_centrality(G))


if __name__ == '__main__':
    cypher()
