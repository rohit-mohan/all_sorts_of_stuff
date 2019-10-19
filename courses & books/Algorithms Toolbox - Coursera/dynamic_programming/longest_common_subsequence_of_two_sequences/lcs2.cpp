#include <iostream>
#include <vector>

using namespace std;
using std::vector;

int lcs2(vector<int> &a, vector<int> &b) {
//write your code here
  int T[101][101], S[101][101];
  
  for (int i = 0; i <= 100; ++i) {
  	T[i][0] = T[0][i] = i;
  	S[i][0] = S[0][i] = 0;
  }	
  	  
  int c, int d;
  for (int j = 1; j <= b.size(); ++j) {
  	for (int i = 1; i <= a.size(); ++i) {
  		
  		c = T[i][j - 1] + 1, d = S[i][j-1];
  		
  		if (T[i - 1][j] + 1 < c) 
  			c = T[i - 1][j] + 1, d = S[i-1][j];
  		
  		else if (a[i-1] == b[j-1] && T[i - 1][j - 1] < c)
  			c = T[i - 1][j - 1], d = S[i-1][j-1] + 1;
  		
  		
  		T[i][j] = c;
  		S[i][j] = d;
  		
  	}
  }
  
  return S[a.size()][b.size()];
}

int main() {
  size_t n;
  std::cin >> n;
  vector<int> a(n);
  for (size_t i = 0; i < n; i++) {
    std::cin >> a[i];
  }

  size_t m;
  std::cin >> m;
  vector<int> b(m);
  for (size_t i = 0; i < m; i++) {
    std::cin >> b[i];
  }

  std::cout << lcs2(a, b) << std::endl;
}
