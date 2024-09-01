from neo4j import GraphDatabase

class ChainGuardGraphDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close the database connection."""
        self.driver.close()

    def create_node(self, label, properties):
        """Create a node with the specified label and properties."""
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_node, label, properties)

    @staticmethod
    def _create_and_return_node(tx, label, properties):
        query = (
            f"CREATE (n:{label} {{"
            + ", ".join([f"{k}: ${k}" for k in properties.keys()])
            + "}}) RETURN n"
        )
        result = tx.run(query, **properties)
        return result.single()[0]

    def create_relationship(self, node1_label, node1_property, node2_label, node2_property, relationship_type):
        """Create a relationship between two nodes."""
        with self.driver.session() as session:
            session.write_transaction(
                self._create_and_return_relationship,
                node1_label, node1_property, node2_label, node2_property, relationship_type
            )

    @staticmethod
    def _create_and_return_relationship(tx, node1_label, node1_property, node2_label, node2_property, relationship_type):
        query = (
            f"MATCH (a:{node1_label} {{name: $node1_property}}), (b:{node2_label} {{name: $node2_property}}) "
            f"CREATE (a)-[r:{relationship_type}]->(b) "
            "RETURN r"
        )
        result = tx.run(query, node1_property=node1_property, node2_property=node2_property)
        return result.single()[0]

    def find_related_anomalies(self, transaction_name):
        """Find all anomalies related to a specific blockchain transaction."""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (t:BlockchainTransaction {name: $transaction_name})-[:DETECTED_IN]->(a:Anomaly) "
                "RETURN a.name, a.type, a.severity",
                transaction_name=transaction_name
            )
            return [record for record in result]

    def find_blockchain_transactions(self, anomaly_name):
        """Find all blockchain transactions related to a specific anomaly."""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:Anomaly {name: $anomaly_name})<-[:DETECTED_IN]-(t:BlockchainTransaction) "
                "RETURN t.name, t.amount, t.timestamp",
                anomaly_name=anomaly_name
            )
            return [record for record in result]

    def validate_blockchain(self):
        """Validate the blockchain (this is a simplified example)."""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:BlockchainTransaction) "
                "RETURN COUNT(b) as transaction_count"
            )
            count = result.single()["transaction_count"]
            # Simplified validation: checks if there are transactions in the blockchain
            return count > 0

# Example usage
if __name__ == "__main__":
    # Connect to the database
    db = ChainGuardGraphDB(uri="bolt://localhost:7687", user="neo4j", password="your_password")

    # Create nodes
    db.create_node("BlockchainTransaction", {"name": "Tx1", "amount": 100, "timestamp": "2024-09-01"})
    db.create_node("Anomaly", {"name": "Anomaly1", "type": "Network", "severity": "High"})

    # Create relationships
    db.create_relationship("BlockchainTransaction", "Tx1", "Anomaly", "Anomaly1", "DETECTED_IN")

    # Query related anomalies for a transaction
    related_anomalies = db.find_related_anomalies("Tx1")
    for anomaly in related_anomalies:
        print(f"Related Anomaly: {anomaly['a.name']}, Type: {anomaly['a.type']}, Severity: {anomaly['a.severity']}")

    # Query related transactions for an anomaly
    related_transactions = db.find_blockchain_transactions("Anomaly1")
    for tx in related_transactions:
        print(f"Related Transaction: {tx['t.name']}, Amount: {tx['t.amount']}, Timestamp: {tx['t.timestamp']}")

    # Validate the blockchain
    is_valid = db.validate_blockchain()
    print(f"Blockchain valid: {is_valid}")

    # Close the connection
    db.close()
