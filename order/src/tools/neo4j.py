from neo4j import GraphDatabase
from neomodel import config, StructuredNode,RelationshipTo,RelationshipFrom,db
from src.utils.logger import logger

# Create a connection to the Neo4j database
class Neo4jGraphDB:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        config.DATABASE_URL = f"bolt://{user}:{password}@localhost:7687"


    def close(self):
        self._driver.close()

    def query(self, query, parameters=None):
        with self._driver.session() as session:
            result = session.run(query, parameters)
            return list(result)  # Fetch all results as a list (this consumes the result)
        
    def create_node(self,node:StructuredNode):
        ''' create a new node '''
        try:
            self.session = self._driver.session()
            self.node = node
            self.session.close()
            return self.node
        except RuntimeError as e:
            logger.error(f'can not create node with name {self.node.name}')
            logger.error(e)

    def create_relationship_to(self,node:StructuredNode,relationship):
        ''' create a relationship from the node'''
        try:
            self.session = self._driver.session()
            relationship =  RelationshipTo(node, relationship)
            self.session.close()
            return relationship
        except RuntimeError as e:
            logger.error(f'can not creeate relationship {relationship} for node {node.name}')
            logger.error(e)

    def add(self, node: StructuredNode):
        ''' Add data to a particular node, create if not exists, update if exists '''
        try:
            # Check if node with the same unique identifier (e.g., customer_id) exists
            existing_node = self._get_existing_node(node)
            
            if existing_node:
                # If node exists, update it
                for key, value in node.__dict__.items():
                    setattr(existing_node, key, value)
                existing_node.save()  # Save updated node
                logger.info(f"Node with {node.order_id} updated.")
                return existing_node
            else:
                # If node does not exist, create it
                node.save()  # Create new node
                logger.info(f"Node with {node.order_id} created.")
                return node

        except RuntimeError as e:
            logger.error(f"Error adding data to node: {node.order_id}")
            logger.error(e)
            return None

    def _get_existing_node(self, node: StructuredNode):
        ''' Helper function to check if the node already exists based on unique identifier '''
        try:
            # Replace customer_id with the actual unique identifier for your use case
            return node.__class__.nodes.get(order_id=node.order_id)
        except node.__class__.DoesNotExist:
            return None

    def get(self,node:StructuredNode):
        ''' get the data for the given node'''
        try:
            self.session = self._driver.session()
            all_nodes = node.nodes.all()
            self.session.close()
            return all_nodes
        except RuntimeError as e:
            logger.error(f'getting data from from node')
            logger.error(e)
  
    def delete_orphan_nodes():
        try:
            # Run the query to match nodes with no relationships
            query = """
            MATCH (n)
            WHERE NOT (n)-[]-()
            DELETE n
            """
            # Execute the query via the Neo4j connection
            db.cypher_query(query, {})
            print("Orphan nodes deleted successfully.")
        except Exception as e:
            print(f"Error occurred: {e}")