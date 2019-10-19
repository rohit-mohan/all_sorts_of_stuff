package recfun

object Main {
  def main(args: Array[String]) {
    println("Pascal's Triangle")
    for (row <- 0 to 10) {
      for (col <- 0 to row)
        print(pascal(col, row) + " ")
      println()
    }
  }

  /**
   * Exercise 1
   */
    def pascal(c: Int, r: Int): Int = 
    	if (c > r) 0
    	else if (c == 0 || r == c) 1
    	else pascal(c, r - 1) + pascal(c - 1, r - 1) 
  
  /**
   * Exercise 2
   */
    def balance(chars: List[Char]): Boolean = {
    
    	def balVal(count: Int, ch: List[Char]):Boolean =
    		if (ch.isEmpty && count == 0) true
    		else if (ch.isEmpty || count < 0) false 
    		else if (ch.head == '(') balVal(count + 1, ch.tail)
    		else if (ch.head == ')') balVal(count - 1, ch.tail)
    		else balVal(count, ch.tail)

		balVal(0, chars)
    }
  
  /**
   * Exercise 3
   */
    def countChange(money: Int, coins: List[Int]): Int =
    	if (coins.isEmpty || money < 0) 0
		else if (money == 0) 1
		else countChange(money - coins.head, coins) + countChange(money, coins.tail)
  }
