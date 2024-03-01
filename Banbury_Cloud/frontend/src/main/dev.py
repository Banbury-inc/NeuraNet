import psutil
import GPUtil
import subprocess
import nvsmi
import pynvml
def get_gpu_usage():
    """
    Returns the GPU usage.
    """

    pynvml.nvmlInit()
    device_count = pynvml.nvmlDeviceGetCount()
    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        print(f"GPU {i} usage is: {util.gpu}%")
    pynvml.nvmlShutdown()


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
