#include <algorithm>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <tuple>
#include <string>
#include <cmath>
#include <limits>
#include <cstdlib>
using std::vector;
using std::tuple;
using std::get;
using std::string;
using std::pair;
using std::sort;
using std::cout;
using std::endl;

bool sort_points_y(tuple<int, int> a, tuple<int, int> b) {
	return get<1>(a) < get<1>(b);
}

bool sort_points_x(tuple<int, int> a, tuple<int, int> b) {
	return get<0>(a) < get<0>(b);
}

double distance(tuple<int, int> a, tuple<int, int> b) {
  double x = get<0>(a) - get<0>(b);
  double y = get<1>(a) - get<1>(b);
  
  return sqrt(x*x + y*y);
}

double find_dist_manual(vector<tuple<int, int>>& px, int left, int right) {
  double dmin = std::numeric_limits<double>::max();
  
  
  for (int i = left; i <= right; ++i) {
    for (int j=i+1; j <= right; ++j) {
      double d = distance(px[i], px[j]);
      if (dmin > d) dmin = d;      
    }
  }
  
  //cout << "MANUAL left : " << left << " right : " << right << " min : " << dmin << endl;
  
  return dmin;
}

double min_distance_recursive(vector<tuple<int, int>>& px, vector<tuple<int, int>> py, int left, int right) {

  if ((right - left) <= 2) /*if there are only 3 points or less*/ {
    return find_dist_manual(px, left, right);
  }
  
  // finding the median point's index
  int mid = left + (right - left)/2;
  //cout << "REC mid : " << mid << endl;
  
  vector<tuple<int, int>> pyl;
  vector<tuple<int, int>> pyr;
  
  for (int i = 0; i < py.size(); ++i) { 
    if (get<0>(py[i]) <= get<0>(px[mid])) {
      pyl.push_back(py[i]);
    }
    else {
      pyr.push_back(py[i]);
    }
  }  
  
  // finding the minimum distance in each partition
  double left_min = min_distance_recursive(px, pyl, left, mid);
  double right_min = min_distance_recursive(px, pyr, mid+1, right);
  double dmin = std::min(left_min, right_min);
  //cout << "REC lmin : " << left_min << " rmin : " << right_min << endl;
  
  
  // get all points in the partition, which is a horizontal distance of atmost 'd'
  // from the median point. 
  vector<tuple<int, int>> strip;
  for (int i = 0; i < py.size(); ++i) {
    if (abs(get<0>(py[i]) - get<0>(px[mid])) < dmin) { 
      strip.push_back(py[i]);
    }  
  }
  
  /*
  cout << "(" << get<0>(px[mid]) << "," << get<1>(px[mid]) << ")" << endl;
  cout << "PY : " << endl;
  for (int i = 0; i < py.size(); ++i) 
    cout << "(" << get<0>(py[i]) << "," << get<1>(py[i]) << ")" << " ";
  cout << endl;
  */
  
  for (int i = 0; i < strip.size(); ++i) {
    for (int j = i+1; j < strip.size() && (get<1>(strip[j]) - get<1>(strip[i])) <= dmin; ++j) {
      double d = distance(strip[i], strip[j]);
      if (d < dmin) {
         //cout << "REC points : (" << get<0>(strip[i]) << "," << get<1>(strip[i]) << "), (" ; 
         //cout << get<0>(strip[j]) << "," << get<1>(strip[j]) << ")" << " Distance : " << d << endl;
         dmin = d; 
      }   
    }
  }
  
  //cout << "REC dmin = " << dmin << endl;
  return dmin;
}

double minimal_distance(vector<int>& x, vector<int>& y) {
  //write your code here
  vector<tuple<int, int>> points(x.size());
  vector<tuple<int, int>> points_sorted_y(x.size());
  
  for (int i = 0; i < x.size(); ++i) {
  	get<0>(points[i]) = x[i];
  	get<1>(points[i]) = y[i];
  }
  
  sort(points.begin(), points.end(), sort_points_y);
  
  for (int i = 0; i < x.size(); ++i) points_sorted_y[i] = points[i];
  
  sort(points.begin(), points.end(), sort_points_x);
  
  double min_dist = min_distance_recursive(points, points_sorted_y, 0, points.size() - 1);
  
  //cout << "MIN dmin returned." << endl;
  return min_dist;
}

double minimal_distance_naive (vector<int>& x, vector<int>& y) {
  double dmin = std::numeric_limits<double>::max();

  for (int i = 0; i < x.size(); ++i) {
    for (int j = i+1; j < x.size(); ++j) {
      double d = sqrt(((x[i] - x[j]) * (x[i]-x[j]) + (y[i]-y[j]) * (y[i]-y[j])));
      if (d < dmin) {
        dmin = d;
      //cout << "NAI points : ( " << x[i] << "," << y[i] << "), (" << x[j] << "," << y[j] << ")" << " Distance : " << d << endl;
      }  
    }
  }
  
  
  return dmin;
}


void test(void) {
  cout << "Lim : " << std::numeric_limits<int>::max() << " " << std::numeric_limits<int>::min();;
  for (int tnum = 1; tnum <= 100; ++tnum) {
    cout << "Test number : " << tnum << endl;
    int n = rand() % (100 - 2) + 2;
    
    vector<int> x(n), y(n);
    
    for (int i = 0; i < n; ++i) {
      x[i] = rand() % 100;
      y[i] = rand() % 100;    
    }
    
    cout << "Start naive" << endl;
    double ans1 = minimal_distance_naive(x, y);
    cout << "End naive" << endl;

    cout << "start fast" << endl;
    double ans2 = minimal_distance(x, y);
    cout << "end fast" << endl;
    
    if (ans1 != ans2) {
      cout << "TEST ans1 = " << ans1 << " ans2 = " << ans2 << endl;
      cout << "Input : " << n << endl;
      
      for (int i = 0; i < n; ++i) {
        cout << x[i] << " " << y[i] << endl;
      }
      
      return;
    }
  }
} 


int main() {
  
  size_t n;
  std::cin >> n;
  vector<int> x(n);
  vector<int> y(n);
  for (size_t i = 0; i < n; i++) {
    std::cin >> x[i] >> y[i];
  }
  std::cout << std::fixed;
  std::cout << std::setprecision(9) << minimal_distance(x, y) << "\n";
  
  //test();
  return 0;
}
