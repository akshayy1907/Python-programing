import simpy
import random

NUM_CUSTOMERS = 20

def run_simulation(interarrival, service):
    print("\n----------------------------------")
    print(f"Interarrival Time = {interarrival}, Service Time = {service}")
    print("----------------------------------")

    waiting_times = []

    def customer(env, name, server):
        arrival_time = env.now

        with server.request() as request:
            yield request
            wait = env.now - arrival_time
            waiting_times.append(wait)

            service_time = random.expovariate(1.0 / service)
            yield env.timeout(service_time)

    def setup(env, server):
        for i in range(NUM_CUSTOMERS):
            yield env.timeout(random.expovariate(1.0 / interarrival))
            env.process(customer(env, f"C{i+1}", server))

    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)

    env.process(setup(env, server))
    env.run()

    avg_wait = sum(waiting_times) / len(waiting_times)
    print("Average Waiting Time:", round(avg_wait, 2))


# Run with different values
run_simulation(3, 5)
run_simulation(2, 5)   # faster arrivals → more waiting
run_simulation(3, 7)   # slower service → more waiting