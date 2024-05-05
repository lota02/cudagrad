#include <stdio.h>

namespace cg {

__global__ void helloFromGPU() { printf("Hello, GPU!\n"); }

extern "C" void hello() {
  helloFromGPU<<<1, 1>>>();
  cudaDeviceSynchronize();
}

} // namespace cg
