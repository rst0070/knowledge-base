from neo4j import AsyncGraphDatabase


def get_neo4j_driver(
    uri: str,
    username: str,
    password: str,
):
    return AsyncGraphDatabase.driver(
        uri=uri,
        auth=(username, password),
    )
