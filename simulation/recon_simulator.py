from datetime import datetime, timedelta

def generate_recon_logs(
    src_ip,
    start_time,
    num_ports,
    base_port=20
):
    logs = []
    timestamp = start_time

    for i in range(num_ports):
        logs.append(
            f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} "
            f"{src_ip} 192.168.1.1 {base_port + i}"
        )
        timestamp += timedelta(seconds=2)

    return logs
