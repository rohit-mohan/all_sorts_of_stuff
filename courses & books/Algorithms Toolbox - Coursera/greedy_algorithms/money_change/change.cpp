#include <iostream>

int get_change(int m) {
  //write your code here
  
  int remaining = m;
  int coins = 0;
  
  coins += remaining / 10;
  remaining = remaining % 10;
  
  coins += remaining / 5; 
  remaining = remaining % 5;
  
  coins += remaining;
  
  return coins;
}

int main() {
  int m;
  std::cin >> m;
  std::cout << get_change(m) << '\n';
}
