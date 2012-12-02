#include <iostream>
#include <cstdio>

void printMat4(const mat4 matrix, const char* name) {
	std::cout << name << "\n";
	    for (int i = 0; i < 4; i++) {
	      for (int j = 0; j < 4; j++) {
	        printf("%.2f ", matrix[i][j]);
	      }
	      printf("\n");
	    }
}
