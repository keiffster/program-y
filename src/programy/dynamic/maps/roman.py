from programy.dynamic.maps.map import DynamicMap

# Code stolen from http://code.activestate.com/recipes/81611-roman-numerals/

numeral_map = zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
)

class MapRomanToDecimal(DynamicMap):

    def __init__(self, config):
        DynamicMap.__init__(self, config)

    def map_value(self, bot, clientid, input):
        if type(input) != type(""):
            raise TypeError("expected string, got %s" % type(input))
        input = input.upper()
        nums = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
        ints = [1000, 500, 100, 50, 10, 5, 1]
        places = []
        for c in input:
            if not c in nums:
                raise ValueError("input is not a valid roman numeral: %s" % input)
        for i in range(len(input)):
            c = input[i]
            value = ints[nums.index(c)]
            # If the next place holds a larger number, this value is negative.
            try:
                nextvalue = ints[nums.index(input[i + 1])]
                if nextvalue > value:
                    value *= -1
            except IndexError:
                # there is no next place.
                pass
            places.append(value)
        sum = 0
        for n in places: sum += n
        return str(sum)

class MapDecimalToRoman(DynamicMap):

    def __init__(self, config):
        DynamicMap.__init__(self, config)

    def map_value(self, bot, clientid, value):
        input = int(value)
        if not 0 < input < 4000:
           raise ValueError("Argument must be between 1 and 3999")
        ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
        nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
        result = ""
        for i in range(len(ints)):
           count = int(input / ints[i])
           result += nums[i] * count
           input -= ints[i] * count
        return result