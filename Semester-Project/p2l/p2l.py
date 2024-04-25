import threading
import time
import os

class LockManager:
    def __init__(self):
        self.locks = {}
        self.locks_condition = threading.Condition()

    def acquire_lock(self, resource_id, transaction_id):
        with self.locks_condition:
            if resource_id not in self.locks:
                self.locks[resource_id] = threading.Lock()

        lock = self.locks[resource_id]
        lock.acquire()
        print(f"Transaction {transaction_id} acquired lock for {resource_id}")

    def release_lock(self, resource_id, transaction_id):
        with self.locks_condition:
            if resource_id in self.locks:
                lock = self.locks[resource_id]
                lock.release()
                print(f"Transaction {transaction_id} released lock for {resource_id}")
            else:
                print(f"Transaction {transaction_id} tried to release lock for non-existing {resource_id}")

class Transaction:
    _id_counter = 0

    def __init__(self, node_id, lock_manager, resource_id, value):
        self.node_id = node_id
        self.lock_manager = lock_manager
        self.resource_id = resource_id
        self.value = value
        self.transaction_id = None

    def start(self):
        self.transaction_id = self._generate_transaction_id()
        print(f"Starting transaction {self.transaction_id} for {self.node_id}")

    def read(self):
        self.lock_manager.acquire_lock(self.resource_id, self.transaction_id)
        time.sleep(1)  # Simulate transaction execution time
        print(f"{self.node_id} transaction {self.transaction_id} read value {self.value}")
        self.lock_manager.release_lock(self.resource_id, self.transaction_id)

    def write(self, new_value):
        self.lock_manager.acquire_lock(self.resource_id, self.transaction_id)
        time.sleep(1)  # Simulate transaction execution time
        self.value = new_value
        print(f"{self.node_id} transaction {self.transaction_id} wrote value {self.value}")
        self.lock_manager.release_lock(self.resource_id, self.transaction_id)

    def commit(self):
        print(f"{self.node_id} transaction {self.transaction_id} committed.")

    def _generate_transaction_id(self):
        Transaction._id_counter += 1
        return Transaction._id_counter

def run_transaction(transaction):
    transaction.start()
    transaction.read()
    transaction.write(transaction.value * 2)
    transaction.commit()

if __name__ == "__main__":
    lock_manager = LockManager()

    # Retrieve environment variables or use defaults
    node_id = os.getenv("NODE_ID", "node0")
    resource_id = os.getenv("RESOURCE_ID", "resource1")
    initial_value = int(os.getenv("INITIAL_VALUE", 10))

    # Create 2 transaction
    transaction1 = Transaction(node_id, lock_manager, resource_id, initial_value)

    transaction2 = Transaction(node_id, lock_manager, resource_id, 30)
    # Run the transaction
    run_transaction(transaction1)
    run_transaction(transaction2)

