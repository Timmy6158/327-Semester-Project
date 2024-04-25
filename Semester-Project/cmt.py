import threading
import time

class Resource:
    def __init__(self):
        self.data = 0
        self.timestamp = 0

    def read(self, transaction_id):
        if self.timestamp > transaction_id:
            print(f"Transaction {transaction_id} aborted due to conflict.")
            return None
        else:
            return self.data

    def write(self, value, transaction_id):
        if self.timestamp > transaction_id:
            print(f"Transaction {transaction_id} aborted due to conflict.")
        else:
            self.data = value
            self.timestamp = transaction_id

class Transaction:
    _id_counter = 0

    def __init__(self, resource, value):
        self.resource = resource
        self.value = value
        self.transaction_id = None

    def start(self):
        self.transaction_id = self._generate_transaction_id()
        print(f"Starting transaction {self.transaction_id}")

    def commit(self):
        self.resource.write(self.value, self.transaction_id)
        print(f"Transaction {self.transaction_id} committed.")
        print(f"Resource data is now {self.resource.read(self.transaction_id)}")

    def _generate_transaction_id(self):
        Transaction._id_counter += 1
        return Transaction._id_counter

def run_transaction(transaction):
    transaction.start()
    time.sleep(1)  # Simulate transaction execution time
    transaction.commit()

if __name__ == "__main__":
    resource = Resource()

    # Create multiple transactions with different values
    transactions = [
        Transaction(resource, 100),
        Transaction(resource, 20),
        Transaction(resource, 50),
        Transaction(resource, 200)
    ]

    # Start and run transactions concurrently
    threads = []
    for transaction in transactions:
        thread = threading.Thread(target=run_transaction, args=(transaction,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # After transactions are completed, print the final state of the resource
    print(f"Final state of resource: {resource.data}")
