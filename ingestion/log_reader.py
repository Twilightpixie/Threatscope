def read_logs(filepath):
    with open(filepath, "r") as f:
        return f.readlines()
