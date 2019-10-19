package forcomp

import scala.collection.immutable._

object test {
type Word = String
type Occurrences = List[(Char, Int)];import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(262); 
def wordOccurrences(w: Word): Occurrences = w.toLowerCase.groupBy(identity).mapValues((x:String) => x.length).toList.sortWith(_._1 < _._1);System.out.println("""wordOccurrences: (w: forcomp.test.Word)forcomp.test.Occurrences""");$skip(186); 

def wordOccurrence(w: Word): Occurrences = {
    val unsorted = (w.toLowerCase groupBy identity) map { case (c,cs) => (c, cs.length) }

    (SortedMap[Char,Int]() ++ unsorted) toList
};System.out.println("""wordOccurrence: (w: forcomp.test.Word)forcomp.test.Occurrences""");$skip(25); val res$0 = 

wordOccurrences("abcd");System.out.println("""res0: forcomp.test.Occurrences = """ + $show(res$0));$skip(23); val res$1 = 
wordOccurrence("abcd");System.out.println("""res1: forcomp.test.Occurrences = """ + $show(res$1))}
}
