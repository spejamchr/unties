from numbers import Number

class Counter(dict) :
    def __missing__(self, key) :
        return 0

    def __setitem__(self,key,value) :
        if not isinstance(value, Number) :
            raise Exception('Must be a number')
        super().__setitem__(key,value)
        if self[key] == 0 :
            self.pop(key)

    def __str__(self) :
        strings = [str(x) + self.exp_str(x) for x in sorted(list(self))]
        return ' * '.join(strings)

    def exp_str(self, key) :
        if self[key] == 1 :
            return ''
        else :
            return '**' + str(self[key])

    def present(self) :
        return self
