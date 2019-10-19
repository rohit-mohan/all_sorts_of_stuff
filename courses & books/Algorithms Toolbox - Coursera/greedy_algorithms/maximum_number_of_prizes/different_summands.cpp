#include <iostream>
#include <vector>

using std::vector;

vector<int> optimal_summands(int n) {
  vector<int> summands;
  //write your code here
  int sum = 0;
  for (int i = 1; i <= n; ++i) {
  	int remaining = n - (sum + i);
  	
  	if (remaining && remaining < (i + 1)) 
  		continue;
  	else {
  		summands.push_back(i);
  		sum += i;	
  	}
  	
  	if (sum == n) break;
  }
  
  return summands;
}

int main() {
  int n;
  std::cin >> n;
  vector<int> summands = optimal_summands(n);
  std::cout << summands.size() << '\n';
  for (size_t i = 0; i < summands.size(); ++i) {
    std::cout << summands[i] << ' ';
  }
}
