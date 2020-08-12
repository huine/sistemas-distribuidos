from psutil import Process, cpu_count

print("Process PID: %s" % Process().pid)
print("Number of Cores: %s" % cpu_count())
print("Process CPU Affinity: %s" % Process().cpu_affinity())
# Set process to run only on cpu0
Process().cpu_affinity([0])

print("Process CPU Affinity after set: %s" % Process().cpu_affinity())