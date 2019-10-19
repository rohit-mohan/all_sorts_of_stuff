#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

struct Structure  {
	int count, back;
};

vector<int> optimal_sequence(int n) {
	struct Structure T[1000001];
	
	T[1].count = 0;
	T[1].back = 0;
	
	struct Structure a;
	for (int i = 2; i <= n; ++i) {
		
		a.count = T[i - 1].count + 1;
		a.back = i - 1;
		
		if ((i % 2 == 0) && (T[i / 2].count + 1 < a.count)) {
			a.count = T[i / 2].count + 1;
			a.back = i / 2;
		}
			
		if ((i % 3 == 0) && (T[i / 3].count + 1 < a.count)) {
			a.count = T[i / 3].count + 1;
			a.back = i / 3;
		} 
		
		T[i].count = a.count;
		T[i].back = a.back;
	}
	
	vector<int> sequence;
	int i = n;
	while (i >= 1) {
		sequence.push_back(i);
		// cout << i << " : " << T[i].count << ", " << T[i].back << endl;
		i = T[i].back;
	}
	reverse(sequence.begin(), sequence.end());
	return sequence;
}

void test(void) {
	for (int i = 0; i < 100; ++i) {
		std::cout << i << std::endl;
		optimal_sequence(rand()%1000001);
	}
}


int main() {
  //test();
  
  int n;
  std::cin >> n;
  vector<int> sequence = optimal_sequence(n);
  std::cout << sequence.size() - 1 << std::endl;
  for (size_t i = 0; i < sequence.size(); ++i) {
    std::cout << sequence[i] << " ";
  }
  cout << endl;
  
  return 0;
}
