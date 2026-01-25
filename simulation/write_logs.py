from simulation.run_simulation import run_simulation

def write_logs(filename="logs/network.log"):
    logs = run_simulation()
    with open(filename, "w") as f:
        for line in logs:
            f.write(line + "\n")
