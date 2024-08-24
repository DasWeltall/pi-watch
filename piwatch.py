import tkinter as tk
from tkinter import ttk
import psutil
import time
import socket
import getpass

# Initialize global variables
prev_net_io = None
prev_time = None

def update_cpu_tab():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq().current
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    ram_total = ram.total / (1024 * 1024 * 1024)  # In GB
    ram_used = ram.used / (1024 * 1024 * 1024)  # In GB

    swap = psutil.swap_memory()
    swap_usage = swap.percent
    swap_total = swap.total / (1024 * 1024 * 1024)  # In GB
    swap_used = swap.used / (1024 * 1024 * 1024)  # In GB

    cpu_label_value.config(text=f"{cpu_usage}% @ {cpu_freq:.2f} MHz")
    ram_label_value.config(text=f"{ram_used:.1f} GB / {ram_total:.1f} GB ({ram_usage}%)")
    swap_label_value.config(text=f"{swap_used:.1f} GB / {swap_total:.1f} GB ({swap_usage}%)")

    cpu_progress['value'] = cpu_usage
    ram_progress['value'] = ram_usage
    swap_progress['value'] = swap_usage

    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']), 
                       key=lambda p: p.info['cpu_percent'], reverse=True)[:5]

    for row in process_table.get_children():
        process_table.delete(row)

    for proc in processes:
        process_table.insert('', 'end', values=(
            proc.info['name'], proc.info['cpu_percent'], round(proc.info['memory_percent'], 1)))

def update_network_tab():
    global prev_net_io, prev_time

    net_io = psutil.net_io_counters()
    curr_time = time.time()

    if prev_net_io:
        elapsed_time = curr_time - prev_time
        download_speed = (net_io.bytes_recv - prev_net_io.bytes_recv) / elapsed_time
        upload_speed = (net_io.bytes_sent - prev_net_io.bytes_sent) / elapsed_time

        download_speed_mbps = download_speed / (1024 * 1024)
        upload_speed_mbps = upload_speed / (1024 * 1024)

        download_label_value.config(text=f"{download_speed_mbps:.2f} MB/s")
        upload_label_value.config(text=f"{upload_speed_mbps:.2f} MB/s")

    prev_net_io = net_io
    prev_time = curr_time

    net_stats = psutil.net_if_stats()
    net_addrs = psutil.net_if_addrs()
    active_interface = None
    net_status = "Disconnected"

    for iface, stats in net_stats.items():
        if stats.isup:
            net_status = "Connected"
            active_interface = iface
            break

    net_label_value.config(text=f"{net_status}")
    interface_label_value.config(text=f"{active_interface}")

    ip_info = ""
    for iface, addrs in net_addrs.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_info += f"{iface}: {addr.address}\n"
    ip_label_value.config(text=ip_info.strip())

def update_user_tab():
    uptime = time.time() - psutil.boot_time()
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
    disk = psutil.disk_usage('/')
    disk_free_gb = disk.free / (1024 * 1024 * 1024)  # Free space in GB
    disk_total_gb = disk.total / (1024 * 1024 * 1024)  # Total space in GB
    disk_usage_percent = 100 - (disk.free / disk.total * 100)  # Disk usage percentage

    # Round to the nearest tenth
    disk_usage_percent_rounded = round(disk_usage_percent, 1)

    # User information
    username = getpass.getuser()
    user_id = psutil.Process().uids().real  # User ID of the current process
    num_users = len(psutil.users())

    # System load
    load_avg = psutil.getloadavg()
    load1, load5, load15 = load_avg

    uptime_label_value.config(text=f"{uptime_str}")
    disk_label_value.config(text=f"{disk_free_gb:.1f} GB / {disk_total_gb:.1f} GB ({disk_usage_percent_rounded}%)")
    disk_progress['value'] = disk_usage_percent_rounded

    username_label_value.config(text=f"Username: {username}")
    user_id_label_value.config(text=f"User ID: {user_id}")
    num_users_label_value.config(text=f"Number of Users: {num_users}")
    load_label_value.config(text=f"Load Average: {load1:.2f} (1m), {load5:.2f} (5m), {load15:.2f} (15m)")

def update_info():
    update_cpu_tab()
    update_network_tab()
    update_user_tab()

    root.after(1000, update_info)

root = tk.Tk()
root.title("PiWatch")
root.geometry("320x410")
root.configure(bg="#2d2d2d")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# CPU Tab
cpu_tab = tk.Frame(notebook, bg="#2d2d2d")
notebook.add(cpu_tab, text="CPU")

cpu_label = tk.Label(cpu_tab, text="CPU Usage:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
cpu_label.pack(pady=10)
cpu_label_value = tk.Label(cpu_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
cpu_label_value.pack()
cpu_progress = ttk.Progressbar(cpu_tab, orient="horizontal", length=200, mode='determinate', style="Thin.Horizontal.TProgressbar")
cpu_progress.pack(pady=5)

ram_label = tk.Label(cpu_tab, text="RAM Usage:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
ram_label.pack(pady=10)
ram_label_value = tk.Label(cpu_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
ram_label_value.pack()
ram_progress = ttk.Progressbar(cpu_tab, orient="horizontal", length=200, mode='determinate', style="Thin.Horizontal.TProgressbar")
ram_progress.pack(pady=5)

swap_label = tk.Label(cpu_tab, text="Swap Usage:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
swap_label.pack(pady=10)
swap_label_value = tk.Label(cpu_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
swap_label_value.pack()
swap_progress = ttk.Progressbar(cpu_tab, orient="horizontal", length=200, mode='determinate', style="Thin.Horizontal.TProgressbar")
swap_progress.pack(pady=5)

processes_label = tk.Label(cpu_tab, text="Top Processes:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
processes_label.pack(pady=10)

columns = ("Process", "CPU (%)", "Memory (%)")
process_table = ttk.Treeview(cpu_tab, columns=columns, show="headings", height=5)
process_table.heading("Process", text="Process")
process_table.heading("CPU (%)", text="CPU (%)")
process_table.heading("Memory (%)", text="Memory (%)")
process_table.column("Process", width=150)
process_table.column("CPU (%)", width=75, anchor="center")
process_table.column("Memory (%)", width=75, anchor="center")
process_table.pack(fill="both", expand=True)

# Network Tab
network_tab = tk.Frame(notebook, bg="#2d2d2d")
notebook.add(network_tab, text="Network")

net_label = tk.Label(network_tab, text="Network Status:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
net_label.pack(pady=10)
net_label_value = tk.Label(network_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
net_label_value.pack()

interface_label = tk.Label(network_tab, text="Active Interface:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
interface_label.pack(pady=10)
interface_label_value = tk.Label(network_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
interface_label_value.pack()

ip_label = tk.Label(network_tab, text="IP Address:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
ip_label.pack(pady=10)
ip_label_value = tk.Label(network_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
ip_label_value.pack()

download_label = tk.Label(network_tab, text="Download Speed:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
download_label.pack(pady=10)
download_label_value = tk.Label(network_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
download_label_value.pack()

upload_label = tk.Label(network_tab, text="Upload Speed:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
upload_label.pack(pady=10)
upload_label_value = tk.Label(network_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
upload_label_value.pack()

# User Tab
user_tab = tk.Frame(notebook, bg="#2d2d2d")
notebook.add(user_tab, text="User")

disk_label = tk.Label(user_tab, text="Free Disk Space:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
disk_label.pack(pady=10)
disk_label_value = tk.Label(user_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
disk_label_value.pack()
disk_progress = ttk.Progressbar(user_tab, orient="horizontal", length=250, mode='determinate', style="Thin.Horizontal.TProgressbar")
disk_progress.pack(pady=5)

uptime_label = tk.Label(user_tab, text="System Uptime:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
uptime_label.pack(pady=10)
uptime_label_value = tk.Label(user_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
uptime_label_value.pack()

username_label = tk.Label(user_tab, text="Username:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
username_label.pack(pady=10)
username_label_value = tk.Label(user_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
username_label_value.pack()

user_id_label = tk.Label(user_tab, text="User ID:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
user_id_label.pack(pady=10)
user_id_label_value = tk.Label(user_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
user_id_label_value.pack()

num_users_label = tk.Label(user_tab, text="Number of Users:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
num_users_label.pack(pady=10)
num_users_label_value = tk.Label(user_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
num_users_label_value.pack()

load_label = tk.Label(user_tab, text="System Load Average:", font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#2d2d2d")
load_label.pack(pady=10)
load_label_value = tk.Label(user_tab, text="Loading...", font=('Helvetica', 10), fg="#39ff14", bg="#2d2d2d")
load_label_value.pack()

style = ttk.Style()
style.configure("Treeview.Heading", font=('Helvetica', 8, 'bold'), background="#444", foreground="white")
style.configure("Treeview", font=('Helvetica', 8), rowheight=20, background="#333", foreground="white", fieldbackground="#333")
style.map('Treeview', background=[('selected', '#565656')], foreground=[('selected', 'white')])

style.configure("Thin.Horizontal.TProgressbar", thickness=5)

update_info()

root.mainloop()
