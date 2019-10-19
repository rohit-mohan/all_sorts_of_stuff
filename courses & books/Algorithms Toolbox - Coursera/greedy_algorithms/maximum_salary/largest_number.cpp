#include <algorithm>
#include <sstream>
#include <iostream>
#include <vector>
#include <string>

using std::vector;
using std::string;

bool sortFunction(string a, string b) {
	int r1 = std::stoi(a + b);
	int r2 = std::stoi(b + a);
	
	if (r1 > r2) return true;
	else return false;
}

string largest_number(vector<string> a) {
  //write your code here
  std::stringstream ret;
  
  std::sort(a.begin(), a.end(), sortFunction);
  
  for (size_t i = 0; i < a.size(); i++) {
    ret << a[i];
  }
  string result;
  ret >> result;
  
  return result;
}

int main() {
  int n;
  std::cin >> n;
  vector<string> a(n);
  for (size_t i = 0; i < a.size(); i++) {
    std::cin >> a[i];
  }
  std::cout << largest_number(a);
}
