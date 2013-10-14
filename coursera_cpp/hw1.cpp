// Homework 1: Convert a C program to C++
//
// Goals:
//   1. change to C++ io
//   2. change to one line comments
//   3. change defines of constants to const
//   4. change array to vector<>
//   5. inline any short function

#include <iostream>
#include <vector>

using namespace std;

// number of consecutive ints that will be summed
const int N = 40;


// Returns the sum of vector contents
//
// @class Summable Any type that provides reasonable addition operation
// @param summed A vector of Summable
// @returns The sum of vector contents
template<class Summable>
inline Summable sum(vector<Summable> summed)
{
  Summable result = 0;
  for (vector<int>::iterator it = summed.begin(); it != summed.end(); ++it)
    result += *it;
  return result;
}


// Controls operation of the program
int main(void)
{
  // prepare a vector with N consecutive natural numbers
  vector<int> data (N);
  for(int i = 0; i < N; ++i)
    data[i] = i;

  // calculate the sum
  int accum = sum(data);

  // print the sum to stdout
  cout << "sum is " << accum << endl;
  return 0;
}
