import simpy
import random

RANDOM_SEED = 42
NUM_CUSTOMERS = 20
INTERARRIVAL_TIME = 3
SERVICE_TIME = 5

random.seed(RANDOM_SEED)

waiting_times = []

def customer(env, name, server):
    arrival_time = env.now
    print(f"{name} arrives at {arrival_time:.2f}")

    with server.request() as request:
        yield request

        wait = env.now - arrival_time
        waiting_times.append(wait)
        print(f"{name} starts service at {env.now:.2f} (waited {wait:.2f})")

        service_time = random.expovariate(1.0 / SERVICE_TIME)
        yield env.timeout(service_time)u

        print(f"{name} leaves at {env.now:.2f}")

def setup(env, server):
    for i in range(NUM_CUSTOMERS):
        yield env.timeout(random.expovariate(1.0 / INTERARRIVAL_TIME))
        env.process(customer(env, f"Customer {i+1}", server))

# Run simulation
env = simpy.Environment()
server = simpy.Resource(env, capacity=1)   # Single server

env.process(setup(env, server))
env.run()

# Average waiting time
avg_wait = sum(waiting_times) / len(waiting_times)
print("\nAverage waiting time:", round(avg_wait, 2))