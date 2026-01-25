from datetime import datetime
from simulation.recon_simulator import generate_recon_logs

def run_simulation():
    logs = []

    # Normal behavior
    logs += generate_recon_logs(
        src_ip="10.0.0.5",
        start_time=datetime(2026, 1, 14, 10, 0, 0),
        num_ports=1
    )

    # Mild recon
    logs += generate_recon_logs(
        src_ip="192.168.1.20",
        start_time=datetime(2026, 1, 14, 10, 1, 0),
        num_ports=4
    )

    # Aggressive recon
    logs += generate_recon_logs(
        src_ip="192.168.1.10",
        start_time=datetime(2026, 1, 14, 10, 2, 0),
        num_ports=12
    )

    return logs
