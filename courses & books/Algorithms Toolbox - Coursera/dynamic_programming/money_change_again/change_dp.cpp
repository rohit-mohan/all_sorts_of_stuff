#include <iostream>
#include <vector>

int get_change(int m) {
  //write your code here
  int D[1001];  
  D[0] = 0;
  
  for (int i = 1; i <= m; ++i) {
  	// find best way to change i
	int min = (signed)((unsigned)-1 >> 1);
	int denom;
	
	if (((i - 4) >= 0) && (min > D[i - 4])) min = D[i - 4], denom = 4; 
	if (((i - 3) >= 0) && (min > D[i - 3])) min = D[i - 3], denom = 3;
	if (min > D[i - 3]) min = D[i - 1], denom = 1;
	D[i] = min + 1;
  }
  
  return D[m];
}

int main() {
  int m;
  std::cin >> m;
  std::cout << get_change(m) << '\n';
}
