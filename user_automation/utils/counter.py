# Counter utility for generating unique usernames
import os

COUNTER_FILE = "data/username_counter.txt"

def get_next_counter():
    """Get the next counter value and increment"""
    os.makedirs("data", exist_ok=True)
    
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            counter = int(f.read().strip())
    else:
        counter = 0
    
    counter += 1
    
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(counter))
    
    return counter

def generate_unique_username(base_username):
    """Generate a unique username with counter suffix"""
    counter = get_next_counter()
    return f"{base_username}{counter:03d}"
