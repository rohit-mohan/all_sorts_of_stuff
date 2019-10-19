package patmat

import patmat.Huffman._

object test {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(154); 
	val t2 = Fork(Fork(Leaf('a',2), Leaf('b',3), List('a','b'), 5), Leaf('d',4), List('a','b','d'), 9);System.out.println("""t2  : patmat.Huffman.Fork = """ + $show(t2 ));$skip(77); val res$0 = 
 encode(frenchCode)(decodedSecret) == quickEncode(frenchCode)(decodedSecret);System.out.println("""res0: Boolean = """ + $show(res$0))}
 
}
