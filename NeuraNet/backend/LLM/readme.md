# Model Paralellism
Said to be the best option for reducing generation times.

split the models individual layers across different devices.
Each device computes a part of the layer, and the outputs are combined.
# Tensor Paralellism
Indiviual layers are split across multiple devices. Each device process
part of the computations for each layer. 
Advantages: Allows for more fine-grained parallelism, which can lead to substantial
speedups, especially for very large models. 
Disadvantages: Requires careful synchronization and communication between devices
# Data Paralellism
Batch Parallelism: Split the input data into smaller batches and process each
batch on a different device. Each device runs a copy of the entire model on its
batch, and the results are combined afterward.
Distributed Training: Use a distributed training framework to train the model
across multiple devices. Gradients are averaged across devices to ensure 
synchronization.
# Parameter Server Architecture
Use a parameter server to maintain a central copy of the model parameters.
Worker devices fetch parameters from the server, perform computations, and send
gradients back to update the paramters. 
# Inference Optimization Techniques
Quantization: Reduce the precision of the model weights to reduce computational 
load and memory usage.
Pruning: Remove unimportant connections in the model to reduce the number of
parameters and computations.

Distillation: Train a smaller model to mimic the behavior of a larger model,
