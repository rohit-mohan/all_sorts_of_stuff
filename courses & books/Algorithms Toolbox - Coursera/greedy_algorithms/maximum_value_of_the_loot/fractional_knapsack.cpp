#include <iostream>
#include <vector>

using std::vector;
using std::cout;
using std::endl;

double get_optimal_value(int capacity, vector<int> weights, vector<int> values) {
  double value = 0.0;

  // write your code here
  int n = values.size();
  int remaining = capacity;
  
  while (remaining > 0) {
  	double max = 0;
  	int loc = -1;
  	for (size_t i = 0; i < n; ++i) {
  		if (weights[i] <= 0) continue;
  		
  		double frac_val = ((double) values[i]) /weights[i];
  		if (max <= frac_val) {
  			max = frac_val;
  			loc = i;
  		}
  	}
  	
  	if (loc == -1) break;
  	
  	int quantity = 0;
  	if (remaining >= weights[loc]) quantity = weights[loc];
  	else quantity = remaining;
  	
  	value += max * quantity;
  	weights[loc] -= quantity;
  	remaining -= quantity; 
  }
  
  return value;
}

int main() {
  int n;
  int capacity;
  std::cin >> n >> capacity;
  vector<int> values(n);
  vector<int> weights(n);
  for (int i = 0; i < n; i++) {
    std::cin >> values[i] >> weights[i];
  }

  double optimal_value = get_optimal_value(capacity, weights, values);

  std::cout.precision(10);
  std::cout << optimal_value << std::endl;
  return 0;
}
