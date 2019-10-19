#include <iostream>
#include <string>

using namespace std;

int edit_distance(const string &str1, const string &str2) {
  //write your code here
  int T[101][101];
  
  for (int i = 0; i <= 100; ++i)
  	T[i][0] = T[0][i] = i;
  
  int a;
  char d;
  for (int j = 1; j <= str2.length(); ++j) {
  	for (int i = 1; i <= str1.length(); ++i) {
  		
  		//cout << str1.substr(0, i) << ", " << str2.substr(0, j) << " : ";
  		
  		a = T[i][j - 1] + 1;
  		d = 'd';
  		
  		if (T[i - 1][j] + 1 < a) 
  			a = T[i - 1][j] + 1, d = 'i';
  		
  		if (str1[i-1] == str2[j-1] && T[i - 1][j - 1] < a)
  			a = T[i - 1][j - 1], d = 'm';
  		else if (str1[i-1] != str2[j-1] && T[i - 1][j - 1] + 1 < a)
  			a = T[i - 1][j - 1] + 1, d = 't';
  		
  		T[i][j] = a;
  		//cout << a << ", " << d << endl;
  	}
  }
  
  return T[str1.length()][str2.length()];
}

int main() {
  string str1;
  string str2;
  std::cin >> str1 >> str2;
  std::cout << edit_distance(str1, str2) << std::endl;
  return 0;
}
