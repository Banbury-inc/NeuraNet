import psutil
import GPUtil
import subprocess



def get_gpu_usage():
    """
    Returns the GPU usage.
    """
    try:
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
        return gpu_load
    except Exception as e:
        gpu_load = 0
        return gpu_load


gpu_usage = get_gpu_usage()
print(gpu_usage)





