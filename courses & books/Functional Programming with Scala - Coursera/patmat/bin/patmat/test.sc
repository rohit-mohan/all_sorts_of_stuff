package patmat

import patmat.Huffman._

object test {
	val t2 = Fork(Fork(Leaf('a',2), Leaf('b',3), List('a','b'), 5), Leaf('d',4), List('a','b','d'), 9)
                                                  //> t2  : patmat.Huffman.Fork = Fork(Fork(Leaf(a,2),Leaf(b,3),List(a, b),5),Leaf
                                                  //| (d,4),List(a, b, d),9)
 encode(frenchCode)(decodedSecret) == quickEncode(frenchCode)(decodedSecret)
                                                  //> res0: Boolean = true
 
}