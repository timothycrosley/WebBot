from WebElements.IteratorUtils import IterableCollectionList

class QueryJoin(IterableCollectionList):
    """
        Enables joining two AppEngine queries (with the implied performance penalty)
    """
    __slots__ = ()

    def __init__(self, queries=()):
        IterableCollectionList.__init__(self)
        for query in queries:
            self.extend(query)

    def search(self, term):
        return self.__class__((iterable.search(term) for iterable in self.iterableItems))

    def filter(self, *args, **kwargs):
        return self.__class__((iterable.filter(*kargs, **kwargs) for iterable in self.iterableItems))

