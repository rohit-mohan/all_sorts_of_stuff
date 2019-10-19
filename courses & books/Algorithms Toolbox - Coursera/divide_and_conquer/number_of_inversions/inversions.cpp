#include <iostream>
#include <vector>
#include <cstdlib>
using std::cout;
using std::endl;
using std::vector;

long long get_number_of_inversions(vector<int> &a, vector<int> &b, size_t left, size_t right) {
  long long number_of_inversions = 0;
  if (right <= left + 1) return number_of_inversions;
  
  size_t ave = left + (right - left) / 2;
  number_of_inversions += get_number_of_inversions(a, b, left, ave);
  number_of_inversions += get_number_of_inversions(a, b, ave, right);
  
  //write your code here
  int i  = left, j = ave;
  
  //cout << "END LEFT : " << left << " RIGHT : " << right << " AVE : " << ave << " COUNT : " << number_of_inversions << endl;
  //cout << "ARR : " << endl;
  //for (int index = left; index < right; ++index) cout << a[index] << " ";
  //cout << endl; 
  
 /* 
  cout << "RIGHT : " << endl;
  for (int index = ave; index < right; ++index) cout << a[index] << " ";
  cout << endl; 
  */
  
  for (int index = left; index < right; ++index) {
  	if (i < ave && j < right) {
	  	if (a[i] <= a[j]) {
	  	  
	  		b[index] = a[i];
	  		++i;
	  	}
	  	else {
	  		b[index] = a[j];
	  		++j;
	  		number_of_inversions += (ave - i);
	  	}
  	}
  	else if (i < ave) {
  		b[index] = a[i];
  		++i;
  	}
  	else /*if (j < right)*/ {
  		b[index] = a[j];
  		++j;
  	}
  }
  

  for (int i = left; i < right; ++i) {
  	a[i] = b[i];
  }	
  
  //cout << "Rec done."<<endl;
  return number_of_inversions;
}

long long get_number_of_inversions_naive(vector<int> &a) {
  //cout << "Niave start" << endl;
	long long num_inversions = 0;
	
	for (size_t i = 0; i < a.size(); ++i) {
		for (size_t j = i+1; j < a.size(); ++j) {
			if (a[j] < a[i]) ++num_inversions;
		}
	}
	
	//cout << "Naive stoped." << endl;
	return num_inversions;
}

void test(void) {
  for (int tnum = 0; tnum < 100; ++tnum) {
  
    cout << "Test number : " << tnum+1 << endl;
    int n = rand() % (100000-1) + 1;
    vector<int> a(n), a_naive(n);
    for (int i = 0; i < a.size(); ++i) {
      int num = rand() % (1000000000 - 1) + 1;
      a[i] = a_naive[i] = num;
    }
    
    vector<int> b(n);
    long long a2 = get_number_of_inversions(a, b, 0, a.size());
    long long a1 = get_number_of_inversions_naive(a_naive);
    
    if (a1 != a2) {
      cout <<  "Output : a1 = " << a1 << " a2 = " << a2 << endl;
      cout << "Input : " << n << endl;
      for (int i = 0; i < a_naive.size(); ++i) cout << a_naive[i] << " ";
      cout << endl;
      return;
    }
  }
}

int main() {
  
  int n;
  std::cin >> n;
  vector<int> a(n);
  for (size_t i = 0; i < a.size(); i++) {
    std::cin >> a[i];
  }
  vector<int> b(a.size());
  std::cout << get_number_of_inversions(a, b, 0, a.size()) << '\n';
  
  //test();
}
