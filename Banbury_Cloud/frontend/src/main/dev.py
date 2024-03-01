import psutil
import GPUtil
import subprocess
def get_gpu_usage():
    """
    Returns the GPU usage.
    """
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        gpu_id = gpu.id
        gpu_name = gpu.name
        gpu_load = f"{gpu.load*100}%"
        gpu_free_memory = f"{gpu.memoryFree}MB"
        gpu_used_memory = f"{gpu.memoryUsed}MB"
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        gpu_temperature = f"{gpu.temperature} °C"
        list_gpus.append(f"ID: {gpu_id}, Name: {gpu_name}, Load: {gpu_load}, Free Memory: {gpu_free_memory}, Used Memory: {gpu_used_memory}, Total Memory: {gpu_total_memory}, Temperature: {gpu_temperature}")
    return list_gpus


def get_cpu_usage():
    """
    Returns the CPU usage.
    """
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_ram_usage():
    """
    Returns the RAM usage.
    """
    ram = psutil.virtual_memory()
    return f"RAM Usage: {ram.percent}%"

ram = get_ram_usage()
cpu = get_cpu_usage()
gpu = get_gpu_usage()
print(ram, cpu, gpu)
