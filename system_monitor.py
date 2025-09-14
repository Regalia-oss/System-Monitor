# system_monitor.py
import psutil
import time
from datetime import datetime

LOG_FILE = "system_monitor_log.txt"

def log_event(event):
    """Log events to a file with timestamp"""
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {event}\n")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {event}")

def monitor_cpu(threshold=80):
    """Monitor CPU usage and log if above threshold"""
    usage = psutil.cpu_percent(interval=1)
    if usage > threshold:
        log_event(f"High CPU usage detected: {usage}%")

def monitor_processes():
    """Log newly started processes"""
    current_processes = {p.pid: p.name() for p in psutil.process_iter()}
    return current_processes

def monitor_network():
    """Monitor network connections"""
    connections = psutil.net_connections()
    active_connections = len([c for c in connections if c.status == 'ESTABLISHED'])
    if active_connections > 10:  # arbitrary threshold for example
        log_event(f"High number of active connections: {active_connections}")

def main():
    print("=== System & Network Monitor ===")
    prev_processes = monitor_processes()
    while True:
        try:
            monitor_cpu()
            monitor_network()
            
            # Detect new processes
            current_processes = monitor_processes()
            new_procs = [name for pid, name in current_processes.items() if pid not in prev_processes]
            for proc in new_procs:
                log_event(f"New process started: {proc}")
            prev_processes = current_processes
            
            time.sleep(5)  # check every 5 seconds
        except KeyboardInterrupt:
            print("Monitoring stopped by user.")
            break

if __name__ == "__main__":
    main()
