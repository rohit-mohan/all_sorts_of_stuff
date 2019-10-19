#include <iostream>
#include <vector>
#include <cstdlib>

using std::vector;
using std::swap;
using std::cout;
using std::endl;

int partition2(vector<int> &a, int l, int r) {
  int x = a[l];
  int j = l;
  for (int i = l + 1; i <= r; i++) {
    if (a[i] <= x) {
      j++;
      swap(a[i], a[j]);
    }
  }
  swap(a[l], a[j]);
  return j;
}

vector<int> partition3(vector<int> &a, int l, int r) {
	vector<int> ret(2);
	
	int x = a[l];
	int j = l;
	int k = l;
	
	for (int i = l + 1; i <= r; ++i) {
		if (a[i] == x) {
			++k;
			swap(a[k], a[i]);
			
			if (j >= k) {
				++j;
				swap(a[j], a[i]);
			} 
			else {
				j = k;
			}
		}
		
		else if (a[i] < x) {
			++j;
			swap(a[j], a[i]);
		}
	}
	
	for (int i = l; i <= k; ++i) {
		int p = j - (i - l);
		if (p <= k) break;
		else swap(a[i], a[p]);
	}
	
	ret[0] = j - (k - l);
	ret[1] = j;
	
	return ret;
} 

void randomized_quick_sort(vector<int> &a, int l, int r) {
  if (l >= r) {
    return;
  }

  int k = l + rand() % (r - l + 1);
  //cout << "rand choice : " << k << endl;
  swap(a[l], a[k]);
  vector<int> parts = partition3(a, l, r);
  
  randomized_quick_sort(a, l, parts[0] - 1);
  randomized_quick_sort(a, parts[1] + 1, r);
}





int main() {
  int n;
  std::cin >> n;
  vector<int> a(n);
  for (size_t i = 0; i < n; ++i) {
    std::cin >> a[i];
  }
  randomized_quick_sort(a, 0, n - 1);
  for (size_t i = 0; i < n; ++i) {
    std::cout << a[i] << ' ';
  }
}
