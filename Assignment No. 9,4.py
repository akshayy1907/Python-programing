import simpy
import random

NUM_CUSTOMERS = 20
INTERARRIVAL_TIME = 3
SERVICE_TIME = 5

waiting_times = []

def customer(env, name, server):
    arrival_time = env.now

    with server.request() as request:
        yield request

        wait = env.now - arrival_time
        waiting_times.append(wait)

        service_time = random.expovariate(1.0 / SERVICE_TIME)
        yield env.timeout(service_time)

def setup(env, server):
    for i in range(NUM_CUSTOMERS):
        yield env.timeout(random.expovariate(1.0 / INTERARRIVAL_TIME))
        env.process(customer(env, f"C{i+1}", server))

env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

env.process(setup(env, server))
env.run()

# Calculate average waiting time
avg_wait = sum(waiting_times) / len(waiting_times)

print("Average waiting time of customers:", round(avg_wait, 2))
