# Usage

## Connect Devices

neuranet connect --device <device_id>
neuranet connect --status

## Manage File Sharing

neuranet share list
neuranet share add <file_path>
neuranet share remove <file_path>

## Manage Distributed Inference

neuranet inference start --model <model_path> --data <data_path>
neuranet inference status <task_id>
neuranet inference stop <task_id>



