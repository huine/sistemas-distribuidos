class function:

    @staticmethod
    def buscaPrimos(lista):
        """."""
        from ehPrimo import alg3
        array = []
        for item in lista:
            if alg3(item) == 1:
                array.append(item)
        return array

    @staticmethod
    def teste(item):
        item['response-teste'] = 20
        return item

    @staticmethod
    def teste1(item):
        item['response-teste1'] = 30
        return item
