# Models

Model weights are downloaded at runtime from Hugging Face and are not committed to this repository.

Default model: `Qwen/Qwen3-1.7B`.

The runtime is hardware-aware:
- CUDA GPU: uses the available GPU(s) automatically.
- CPU: loads on CPU.
- Later: a GGUF/llama.cpp backend can be added for low-memory CPU inference.
