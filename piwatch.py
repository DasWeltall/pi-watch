import tkinter as tk
from tkinter import ttk
import psutil
import time

def update_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq().current
    net_status = "Connected" if psutil.net_if_stats()['lo'].isup else "Disconnected"
    disk_usage = psutil.disk_usage('/').free // (2**30)
    ram_usage = psutil.virtual_memory().percent
    swap_usage = psutil.swap_memory().percent
    uptime = time.time() - psutil.boot_time()
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))

    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']), 
                       key=lambda p: p.info['cpu_percent'], reverse=True)[:4]

    cpu_label_value.config(text=f"{cpu_usage}% @ {cpu_freq:.2f} MHz")
    net_label_value.config(text=f"{net_status}")
    disk_label_value.config(text=f"{disk_usage} GB")
    ram_label_value.config(text=f"{ram_usage}%")
    swap_label_value.config(text=f"{swap_usage}%")
    uptime_label_value.config(text=f"{uptime_str}")

    # Clear the table
    for row in process_table.get_children():
        process_table.delete(row)

    # Insert processes into the table
    for proc in processes:
        process_table.insert('', 'end', values=(
            proc.info['name'], proc.info['cpu_percent'], round(proc.info['memory_percent'], 1)))

    root.after(500, update_info)

# Root window
root = tk.Tk()
root.title("PiWatch")
root.geometry("310x450")
root.configure(bg="#2d2d2d")

# Styles
label_font = ('Helvetica', 10, 'bold')
value_font = ('Helvetica', 10)
label_color = "#ffffff"
value_color = "#39ff14"

# Create a frame for the content
content_frame = tk.Frame(root, bg="#2d2d2d")
content_frame.pack(pady=10, padx=10, fill="both", expand=True)

# CPU Frame
cpu_frame = tk.Frame(content_frame, bg="#3d3d3d", bd=1, relief="ridge", padx=5, pady=5)
cpu_frame.pack(fill="x", pady=3)
cpu_label = tk.Label(cpu_frame, text="CPU Usage:", font=label_font, fg=label_color, bg="#3d3d3d")
cpu_label.grid(row=0, column=0, sticky="w")
cpu_label_value = tk.Label(cpu_frame, text="Loading...", font=value_font, fg=value_color, bg="#3d3d3d")
cpu_label_value.grid(row=0, column=1, sticky="e")

# Network Frame
net_frame = tk.Frame(content_frame, bg="#3d3d3d", bd=1, relief="ridge", padx=5, pady=5)
net_frame.pack(fill="x", pady=3)
net_label = tk.Label(net_frame, text="Network Status:", font=label_font, fg=label_color, bg="#3d3d3d")
net_label.grid(row=0, column=0, sticky="w")
net_label_value = tk.Label(net_frame, text="Loading...", font=value_font, fg=value_color, bg="#3d3d3d")
net_label_value.grid(row=0, column=1, sticky="e")

# Disk Frame
disk_frame = tk.Frame(content_frame, bg="#3d3d3d", bd=1, relief="ridge", padx=5, pady=5)
disk_frame.pack(fill="x", pady=3)
disk_label = tk.Label(disk_frame, text="Free Disk Space:", font=label_font, fg=label_color, bg="#3d3d3d")
disk_label.grid(row=0, column=0, sticky="w")
disk_label_value = tk.Label(disk_frame, text="Loading...", font=value_font, fg=value_color, bg="#3d3d3d")
disk_label_value.grid(row=0, column=1, sticky="e")

# RAM Frame
ram_frame = tk.Frame(content_frame, bg="#3d3d3d", bd=1, relief="ridge", padx=5, pady=5)
ram_frame.pack(fill="x", pady=3)
ram_label = tk.Label(ram_frame, text="RAM Usage:", font=label_font, fg=label_color, bg="#3d3d3d")
ram_label.grid(row=0, column=0, sticky="w")
ram_label_value = tk.Label(ram_frame, text="Loading...", font=value_font, fg=value_color, bg="#3d3d3d")
ram_label_value.grid(row=0, column=1, sticky="e")

# Swap Frame
swap_frame = tk.Frame(content_frame, bg="#3d3d3d", bd=1, relief="ridge", padx=5, pady=5)
swap_frame.pack(fill="x", pady=3)
swap_label = tk.Label(swap_frame, text="Swap Usage:", font=label_font, fg=label_color, bg="#3d3d3d")
swap_label.grid(row=0, column=0, sticky="w")
swap_label_value = tk.Label(swap_frame, text="Loading...", font=value_font, fg=value_color, bg="#3d3d3d")
swap_label_value.grid(row=0, column=1, sticky="e")

# Uptime Frame
uptime_frame = tk.Frame(content_frame, bg="#3d3d3d", bd=1, relief="ridge", padx=5, pady=5)
uptime_frame.pack(fill="x", pady=3)
uptime_label = tk.Label(uptime_frame, text="System Uptime:", font=label_font, fg=label_color, bg="#3d3d3d")
uptime_label.grid(row=0, column=0, sticky="w")
uptime_label_value = tk.Label(uptime_frame, text="Loading...", font=value_font, fg=value_color, bg="#3d3d3d")
uptime_label_value.grid(row=0, column=1, sticky="e")

# Processes Frame with Table
processes_frame = tk.Frame(content_frame, bg="#3d3d3d", bd=1, relief="ridge", padx=5, pady=5)
processes_frame.pack(fill="both", pady=3, expand=True)
processes_label = tk.Label(processes_frame, text="Top Processes:", font=label_font, fg=label_color, bg="#3d3d3d", justify="left")
processes_label.pack(anchor="w")

# Treeview for processes
columns = ("Process", "CPU (%)", "Memory (%)")
process_table = ttk.Treeview(processes_frame, columns=columns, show="headings", height=4)
process_table.heading("Process", text="Process")
process_table.heading("CPU (%)", text="CPU (%)")
process_table.heading("Memory (%)", text="Memory (%)")
process_table.column("Process", width=100)
process_table.column("CPU (%)", width=50, anchor="center")
process_table.column("Memory (%)", width=50, anchor="center")
process_table.pack(fill="both", expand=True)

# Apply styling to Treeview
style = ttk.Style()
style.configure("Treeview.Heading", font=('Helvetica', 8, 'bold'), background="#444", foreground="white")
style.configure("Treeview", font=('Helvetica', 8), rowheight=20, background="#333", foreground="white", fieldbackground="#333")
style.map('Treeview', background=[('selected', '#565656')], foreground=[('selected', 'white')])

update_info()

root.mainloop()

