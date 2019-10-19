#include <algorithm>
#include <iostream>
#include <climits>
#include <cstdlib>
#include <vector>

using std::cout;
using std::endl;
using std::vector;

struct Segment {
  int start, end;
};

long long power(int base, int n) {
	long long ans = 1;
	for (int i = 0; i < n; ++i)
		ans *= base;
	
	return ans;
}

vector<int> optimal_points_naive(vector<Segment> &segments) {
	int n = segments.size();
	vector<int> points;
	vector<int> result;
	vector<bool> point_flag(2*n);
	
	for (int i = 0; i < n; ++i) {
  		points.push_back(segments[i].start);
  		points.push_back(segments[i].end);
  	}
  
  	int min = 2*n;
  	vector<bool> best;
  	vector<bool> segment_flag(n);
  	for (long long i = 0; i < power(2, 2*n) - 1; ++i) {
  		int count = 0;
  		for (size_t j = 0; j < n; ++j) segment_flag[j] = false; 
  		for (int k = 0; k < 2*n; ++k) {
  			if (i & (1 << k)) {
  				point_flag[k] = true;
  				++count;
  			}
  			else point_flag[k] = false;
  		}
  		
  		for (size_t i = 0; i < n; ++i) {
  			for (size_t k = 0; k < 2*n; ++k) {
  				if (point_flag[k] && points[k] >= segments[i].start && points[k] <= segments[i].end)
  					segment_flag[i] = true;
  			}
  		}
  		
  		bool complete = true;
  		for (size_t i = 0; i < n; ++i)
  			if (!segment_flag[i]) complete = false;
  		
  		if (complete) {
  			if (min >= count) {
  				min = count;
  				best = point_flag;
  			}
  		} 
  	}
  	
  	for (size_t i = 0; i < 2*n; ++i)
  		if (best[i]) result.push_back(points[i]);
  	
  	return result;
}

 

vector<int> how_many_segments(int point, vector<Segment> &segments) {
	vector<int> result;
	for (int i = 0; i < segments.size(); ++i) {
		if (point >= segments[i].start && point <= segments[i].end) {
			result.push_back(i);
		}
	}
	
	return result;
}

int minimum_right_ended_segment(vector<Segment> &segments) {
	int min = 1000000001;
	int loc = -1;
	for (int i = 0; i < segments.size(); ++i) {
		if (segments[i].end <= min) {
			min = segments[i].end;
			loc = i;
		}
	}
	
	return loc;
}

vector<int> optimal_points_fast(vector<Segment> &segments) {
  vector<int> solution;
  
  int n  = segments.size();
  
  int remaining = n;
  
  while(segments.size() > 0) {
  	//cout << "segments size : " << segments.size() << endl;
  	// find segment with minimum right endpoint
  	int min_loc = minimum_right_ended_segment(segments);
  	// add it to the solution
  	solution.push_back(segments[min_loc].end);
  	//cout << "Solution added : " << segments[min_loc].end << endl;
  	// find all segments that include this endpoint
  	vector<int> segs = how_many_segments(segments[min_loc].end, segments);
  	std::sort(segs.begin(), segs.end());
  	// delete all those segments
  	for (int i = segs.size() - 1; i >= 0; --i) {
  		//cout << "deleting segment " << segments[segs[i]].start << " " << segments[segs[i]].end << "index : " << segs[i] << endl;
  		segments.erase(segments.begin() + segs[i]);
  	}
  	
  }
  
  return solution;
}

void test() {
	vector<Segment> segments;
	Segment s;
	for (int i = 0; i < 100; ++i) {
		segments.erase(segments.begin(), segments.end());
		int n = rand() % 10 + 1;
		for (int k = 0; k < n; ++k) {
			
			int r1 = rand() % 20;
			int r2 = rand() % 20;
			
			if (r1 > r2) {
				s.start = r2;
				s.end = r1;
				segments.push_back(s);
			}
			
			else {
				s.start = r1;
				s.end = r2;
				segments.push_back(s);
			}
		}
	
		vector<int> a1 = optimal_points_fast(segments);
		vector<int> a2 = optimal_points_naive(segments);
	
		cout << "Answer : " << a1.size() << " " << a2.size();
		if (a1.size() != a2.size()) {
			cout << " failure" << endl;
			cout << n << endl;
			for (int j = 0; j < n; ++j) {
				cout << segments[j].start << " " << segments[j].end << endl;
 			}
 			cout << "a1" << endl;
 			for (int j = 0; j < a1.size(); ++j) cout << a1[j] << endl;
 			cout << "a2" << endl;
 			for (int j = 0; j < a2.size(); ++j) cout << a2[j] << endl;
 			break;
		}
		
		else cout << " success" << endl;
		
	}
}

int main() {
  
  int n;
  std::cin >> n;
  vector<Segment> segments(n);
  for (size_t i = 0; i < segments.size(); ++i) {
    std::cin >> segments[i].start >> segments[i].end;
  }
  
  //cout << "Calling function" << endl;
  vector<int> points = optimal_points_fast(segments);
  std::cout << points.size() << "\n";
  for (size_t i = 0; i < points.size(); ++i) {
    std::cout << points[i] << " ";
  }
  
  //test();
}
