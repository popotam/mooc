// MP 5 Scan
// Given a list (lst) of length n
// Output its prefix sum = {lst[0], lst[0] + lst[1], lst[0] + lst[1] + ... + lst[n-1]}
// Due Tuesday, January 22, 2013 at 11:59 p.m. PST

#include    <wb.h>

#define BLOCK_SIZE 512 //@@ You can change this

#define wbCheck(stmt) do {                                 \
        cudaError_t err = stmt;                            \
        if (err != cudaSuccess) {                          \
            wbLog(ERROR, "Failed to run stmt ", #stmt);    \
            return -1;                                     \
        }                                                  \
    } while(0)

__global__ void scan(float * input, float * output, float * inter, int len, bool save) {
    //@@ Modify the body of this function to complete the functionality of
    //@@ the scan on the device
    //@@ You may need multiple kernel calls; write your kernels before this
    //@@ function and call them from here
	__shared__ float shared[2 * BLOCK_SIZE];

	unsigned int t = threadIdx.x;
	unsigned int b = blockIdx.x;
    unsigned int start = 2 * b * BLOCK_SIZE;
    unsigned int index;
    unsigned int stride;

    // load to shared
    shared[t] = (start + t < len) ? input[start + t] : 0;
    shared[BLOCK_SIZE + t] = (start + BLOCK_SIZE + t < len) ? input[start + BLOCK_SIZE + t] : 0;

    // reduce
    stride = 1;
    while (stride <= BLOCK_SIZE) {
        __syncthreads();
        index = (t + 1) * stride * 2 - 1;
        if (index < 2 * BLOCK_SIZE) {
            shared[index] += shared[index - stride];
        }
        stride *= 2;
    }

    // post reduce
    for (stride = BLOCK_SIZE / 2; stride >= 1; stride /= 2) {
        __syncthreads();
        index = (t + 1) * stride * 2 - 1;
        if (index + stride < 2 * BLOCK_SIZE) {
            shared[index + stride] += shared[index];
        }
    }

    // save in output
    __syncthreads();
    if (start + t < len) {
        output[start + t] = shared[t];
    }
    if (start + BLOCK_SIZE + t < len) {
        output[start + BLOCK_SIZE + t] = shared[BLOCK_SIZE + t];
    }

    // save to intermediary array
    if (save && t == 0) {
        inter[b] = shared[2 * BLOCK_SIZE - 1];
    }
}

__global__ void scan_inter(float * inout, float * blockSums, int len) {
	unsigned int t = threadIdx.x;
	unsigned int b = blockIdx.x;
    unsigned int start = 2 * b * BLOCK_SIZE;
    if (b > 0) {
		if (start + t < len) {
			inout[start + t] += blockSums[b - 1];
		}
		if (start + BLOCK_SIZE + t < len) {
			inout[start + BLOCK_SIZE + t] += blockSums[b - 1];
		}
    }
}

int main(int argc, char ** argv) {
    wbArg_t args;
    float * hostInput; // The input 1D list
    float * hostOutput; // The output list
    float * deviceInput;
    float * deviceOutput;
    float * deviceInterIn;
    float * deviceInterOut;
    int numElements; // number of elements in the list
    int numBlocks;

    args = wbArg_read(argc, argv);

    wbTime_start(Generic, "Importing data and creating memory on host");
    hostInput = (float *) wbImport(wbArg_getInputFile(args, 0), &numElements);
    hostOutput = (float*) malloc(numElements * sizeof(float));
    wbTime_stop(Generic, "Importing data and creating memory on host");

    wbLog(TRACE, "The number of input elements in the input is ", numElements);
    numBlocks = (numElements - 1) / (2 * BLOCK_SIZE) + 1;

    wbTime_start(GPU, "Allocating GPU memory.");
    wbCheck(cudaMalloc((void**)&deviceInput, numElements*sizeof(float)));
    wbCheck(cudaMalloc((void**)&deviceOutput, numElements*sizeof(float)));
    wbCheck(cudaMalloc((void**)&deviceInterIn, numBlocks*sizeof(float)));
    wbCheck(cudaMalloc((void**)&deviceInterOut, numBlocks*sizeof(float)));
    wbTime_stop(GPU, "Allocating GPU memory.");

    wbTime_start(GPU, "Clearing output memory.");
    wbCheck(cudaMemset(deviceOutput, 0, numElements*sizeof(float)));
    wbTime_stop(GPU, "Clearing output memory.");

    wbTime_start(GPU, "Copying input memory to the GPU.");
    wbCheck(cudaMemcpy(deviceInput, hostInput, numElements*sizeof(float), cudaMemcpyHostToDevice));
    wbTime_stop(GPU, "Copying input memory to the GPU.");

    //@@ Initialize the grid and block dimensions here
    dim3 DimGrid(numBlocks, 1, 1);
    dim3 DimBlock(BLOCK_SIZE, 1, 1);

    wbTime_start(Compute, "Performing CUDA computation");
    //@@ Modify this to complete the functionality of the scan
    //@@ on the deivce
    scan<<<DimGrid,DimBlock>>>(deviceInput, deviceOutput, deviceInterIn, numElements, 1);
    if (numBlocks > 1) {
        dim3 InterDimGrid(1, 1, 1);
        dim3 InterDimBlock(BLOCK_SIZE, 1, 1);
        scan<<<InterDimGrid,InterDimBlock>>>(deviceInterIn, deviceInterOut, 0, numBlocks, 0);
        scan_inter<<<DimGrid,DimBlock>>>(deviceOutput, deviceInterOut, numElements);
    }

    cudaDeviceSynchronize();
    wbTime_stop(Compute, "Performing CUDA computation");

    wbTime_start(Copy, "Copying output memory to the CPU");
    wbCheck(cudaMemcpy(hostOutput, deviceOutput, numElements*sizeof(float), cudaMemcpyDeviceToHost));
    wbTime_stop(Copy, "Copying output memory to the CPU");

    wbTime_start(GPU, "Freeing GPU Memory");
    cudaFree(deviceInput);
    cudaFree(deviceOutput);
    wbTime_stop(GPU, "Freeing GPU Memory");

    wbSolution(args, hostOutput, numElements);

    free(hostInput);
    free(hostOutput);

    return 0;
}
