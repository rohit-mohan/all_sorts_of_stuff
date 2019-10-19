package forcomp

import scala.collection.immutable._

object test {
type Word = String
type Occurrences = List[(Char, Int)]
def wordOccurrences(w: Word): Occurrences = w.toLowerCase.groupBy(identity).mapValues((x:String) => x.length).toList.sortWith(_._1 < _._1)
                                                  //> wordOccurrences: (w: forcomp.test.Word)forcomp.test.Occurrences

def wordOccurrence(w: Word): Occurrences = {
    val unsorted = (w.toLowerCase groupBy identity) map { case (c,cs) => (c, cs.length) }

    (SortedMap[Char,Int]() ++ unsorted) toList
}                                                 //> wordOccurrence: (w: forcomp.test.Word)forcomp.test.Occurrences

wordOccurrences("abcd")                           //> res0: forcomp.test.Occurrences = List((a,1), (b,1), (c,1), (d,1))
wordOccurrence("abcd")                            //> res1: forcomp.test.Occurrences = List((a,1), (b,1), (c,1), (d,1))
}