#include <algorithm>
#include <iostream>
#include <vector>
#include <cstdlib>

using std::vector;
using std::cout;
using std::endl;

int get_maority_element_naive(vector<int> &a) {
	int max_count = 0;
	for (int i = 0; i < a.size(); ++i) {
		int cur_element = a[i];
		int cur_count = 0;
	
		for (int j = 0; j < a.size(); ++j) 
			if (a[j] == cur_element) ++cur_count;
	
		if (cur_count > max_count) max_count = cur_count;
	}
	
	if (max_count > (a.size() / 2)) return 1;
	else return -1;
}


int get_majority_element(vector<int> &a, int left, int right) {
  int out;
  
  if (left == right) out = a[left];
  
  else if (left + 1 == right) {
  	if (a[left] == a[right]) out = a[left];
  	else out = -1;
  }
  
  //write your code here
  else {
	  int mid = (left + right) / 2;
	  
	  int majority1 = get_majority_element(a, left, mid);
	  int majority2 = get_majority_element(a, mid + 1, right);
	  int count1 = 0;
	  int count2 = 0;
	  
	  for (int i = left; i <= right; ++i) {
	  	if (a[i] == majority1) ++count1;
	  	else if (a[i] == majority2) ++count2;
	  }
	  
	  
	  
	  if (count1 > ((right - left + 1) / 2)) out = majority1;
	  else if (count2 > ((right - left + 1) / 2)) out = majority2;
	  else out = -1;
  }
  
  //cout << "left : " << left << ", right : " << right << ", out : " << out << endl;
  
  return out;
}

void test() {
  //cout << "starting test" << endl;
  
	for (int tnum = 0; tnum < 100; ++tnum) {
	cout << "Test number : " << tnum << endl;
		
		int n = rand() % 10 + 1;
		//cout << "number of elements : " << n << endl;
		
		vector<int> a(n);
	  
		int rep_num = rand() % 100000 + 1;
		int rep = rand() % n;
	
		for (int i = 0; i < rep; ++i) {
			int pos = rand() % n;
			a[pos] = rep_num;
		}
	
		for (int i = 0; i < n; ++i) {
			if (!a[i])
				a[i] = rand();
		}
	  
	  //cout << "Input acquired." << endl;
	  
		int a1 = (int) (get_maority_element_naive(a) != -1);
		cout << "a1 : " << a1 << endl;
		int a2 = (int) (get_majority_element(a, 0, a.size() - 1) != -1);
		cout << "a2 : " << a2 << endl;
		
		if (a1 != a2) {
			cout << " ERROR => a1 : " << a1 << ", a2 : " << a2 << endl;
			for (int i = 0; i < a.size(); ++i) {
			  cout << a[i] << " ";
			}
			cout << endl;
			return;
		}
		
		//cout << " SUCCESS" << endl;
	}
}

int main() {
  
  int n;
  std::cin >> n;
  vector<int> a(n);
  for (size_t i = 0; i < a.size(); ++i) {
    std::cin >> a[i];
  }
  std::cout << (get_majority_element(a, 0, a.size() - 1) != -1) << '\n';

 //test();
 return 0;
}
