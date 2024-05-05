from flask import Flask, request, jsonify
from supabase_py import create_client
import threading
import logging

SUPABASE_URL = "https://quzaibbwuujchjszcnux.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF1emFpYmJ3dXVqY2hqc3pjbnV4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ2MjMxMzksImV4cCI6MjAzMDE5OTEzOX0.d-DG9rkEehljOGGwfhJRtzVKWRgvfBOxIxhbNx0D5sA"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
lock = threading.Lock()

# Configure logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class LockManager:
    def __init__(self):
        self.locks = {}  # Dictionary to store locks for each data item

    def acquire(self, data_item):
        """Acquire lock on a data item"""
        if data_item not in self.locks:
            self.locks[data_item] = threading.Lock()
        self.locks[data_item].acquire()

    def release(self, data_item):
        """Release lock on a data item"""
        if data_item in self.locks:
            self.locks[data_item].release()

lock_manager = LockManager()

@app.route('/health')
def health_check():
    """Endpoint to perform health check"""
    try:
        tasks = supabase.table('tasks').select('*').execute()
        return jsonify({'status': 'OK'}), 200
    except Exception as e:
        return jsonify({'status': 'Error', 'error': str(e)}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Endpoint to retrieve all tasks"""
    lock_manager.acquire('tasks')  # Acquire lock on 'tasks' data item
    tasks = supabase.table('tasks').select('*').execute()
    lock_manager.release('tasks')  # Release lock on 'tasks' data item
    return jsonify(tasks['data']), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    """Endpoint to create a new task"""
    data = request.json
    logging.info(f"Writing task: {data['task']['name']}")
    
    lock_manager.acquire('tasks')  # Acquire lock on 'tasks' data item
    result = supabase.table('tasks').insert(data['task']).execute()
    lock_manager.release('tasks')  # Release lock on 'tasks' data item
    
    if 'error' in result:
        return jsonify({'error': result['error']['message']}), 500
    else:
        return jsonify({'message': 'Task created successfully', 'task': data['task']}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
