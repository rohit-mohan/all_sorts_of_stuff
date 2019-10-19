#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>
#include <cstdlib>

using std::vector;
using std::tuple;
using std::get;
using std::sort;
using std::cout;
using std::endl;

bool sort_function(tuple<int, char, int> a, tuple<int, char, int> b) {
	if (get<0>(a) == get<0>(b)) {
		if (get<1>(a) == 'p' && get<1>(b) == 'l') return false; // make the swap
		else if (get<1>(a) == 'p' && get<1>(b) == 'r') return true; // don't make the swap
		else if (get<1>(b) == 'p'&& get<1>(a) == 'l') return true; // don't make the swap
		else if (get<1>(b) == 'p' && get<1>(a) == 'r') return false; // make the swap
		else if (get<1>(a) == 'r' && get<1>(b) == 'l') return false;
		else if (get<1>(a) == 'l' && get<1>(b) == 'r') return true;
	}
	
	return (get<0>(a) < get<0>(b));
}



vector<int> fast_count_segments(vector<int> starts, vector<int> ends, vector<int> points) {
  vector<int> cnt(points.size());
  //write your code here
  size_t total_size = 2*starts.size() + points.size();
  vector<tuple<int, char, int>> point_list;
  
  for (int i = 0; i < starts.size(); ++i) {
  	point_list.push_back(tuple<int, char, int> (starts[i], 'l', -1));
  	point_list.push_back(tuple<int, char, int> (ends[i], 'r', -1));
  }
  
  for (int i = 0; i < points.size(); ++i) {
  	point_list.push_back(tuple<int, char, int> (points[i], 'p', i));
  }
  
  sort(point_list.begin(), point_list.end(), sort_function);  
  
  /*
  for (int i = 0; i < point_list.size(); ++i) {
  	cout << "( " << get<0>(point_list[i]) << ", " << get<1>(point_list[i]) << ", " << get<2>(point_list[i]) << ") ";
  }
  cout << endl;
  */
  
  int open_intervals = 0;
  for (int i = 0; i < total_size; ++i) {
  	char type = get<1>(point_list[i]);
  	
  	if (type == 'l') ++open_intervals;
  	
  	else if (type == 'r') --open_intervals;
  	
  	else /*if (type == 'p')*/ {
  		int position = get<2>(point_list[i]);
  		cnt[position] = open_intervals;		
  	}
  }
  
  return cnt;
}

vector<int> naive_count_segments(vector<int> starts, vector<int> ends, vector<int> points) {
  vector<int> cnt(points.size());
  for (size_t i = 0; i < points.size(); i++) {
    for (size_t j = 0; j < starts.size(); j++) {
      cnt[i] += starts[j] <= points[i] && points[i] <= ends[j];
    }
  }
  return cnt;
}

void test() {
	for (int index = 0; index < 100; ++index) {
		cout << "Test number : " << index + 1 << endl;
		int n = rand() % 10 + 1;
		int m = rand() % 10 + 1;
	
		vector<int> starts(n), ends(n);
		for (size_t i = 0; i < starts.size(); ++i) {
			int s1 = rand() % 100 - 50;
			int s2 = rand() % 100 - 50;
			if (s1 <= s2) {
				starts[i] = s1;
				ends[i] = s2;
			}
			else {
				starts[i] = s2;
				ends[i] = s1;
			}
		}
	
		vector<int> points(m);
		for (size_t i = 0; i < points.size(); ++i) {
			points[i] = rand() % 100 - 50;
		}
	
		vector<int> c1 = naive_count_segments(starts, ends, points);
		vector<int> c2 = fast_count_segments(starts, ends, points);
	
		for (int i  = 0; i < c1.size(); ++i) {
			if (c1[i] != c2[i]) {
				
				cout << "Input : " << endl;
				cout << n << " " << m << endl;
				for (int j = 0; j < starts.size(); ++j) 
					cout << starts[j] << " " << ends[j] << endl;
				for (int j = 0; j < points.size(); ++j)
					cout << points[j] << " ";
				cout << endl;
				
				cout << "c1 : ";
				for (int j = 0; j < c1.size(); ++j) {
					cout << c1[j] << " ";
				}
				cout << endl;
			
				cout << "c2 : ";
				for (int j = 0; j < c2.size(); ++j) {
					cout << c2[j] << " ";
				}
				cout << endl;
			
				return;
			}
		}
	}
}


int main() {
  
  int n, m;
  std::cin >> n >> m;
  vector<int> starts(n), ends(n);
  for (size_t i = 0; i < starts.size(); i++) {
    std::cin >> starts[i] >> ends[i];
  }
  vector<int> points(m);
  for (size_t i = 0; i < points.size(); i++) {
    std::cin >> points[i];
  }
  //use fast_count_segments
  vector<int> cnt = fast_count_segments(starts, ends, points);
  for (size_t i = 0; i < cnt.size(); i++) {
    std::cout << cnt[i] << ' ';
  }
  
  //test();
}
