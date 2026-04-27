import random

def calculate_cpu(users, instances):
    if instances == 0:
        return 100.0
    base = (users / (instances * 100)) * 100
    jitter = random.uniform(-2, 2)
    return min(max(base + jitter, 0), 100.0)

def calculate_memory(users, instances):
    if instances == 0:
        return 95.0
    base = 15 + (users / (instances * 120)) * 60
    jitter = random.uniform(-1.5, 1.5)
    return min(max(base + jitter, 5), 100.0)
