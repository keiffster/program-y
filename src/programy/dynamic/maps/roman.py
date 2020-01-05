"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.dynamic.maps.map import DynamicMap

# Code stolen from http://code.activestate.com/recipes/81611-roman-numerals/


class MapRomanToDecimal(DynamicMap):

    NAME = "ROMANTODEC"
    NUMS = ('M', 'D', 'C', 'L', 'X', 'V', 'I')
    INTS = (1000, 500, 100, 50, 10, 5, 1)

    def __init__(self, config):
        DynamicMap.__init__(self, config)

    def map_value(self, client_context, input_value):
        if not isinstance(input_value, str):
            raise TypeError("expected string, got %s" % type(input_value))
        input_value = input_value.upper()
        places = []
        for char in input_value:
            if char not in MapRomanToDecimal.NUMS:
                raise ValueError("input_value is not a valid roman numeral: %s" % input_value)

        charnum = 0
        for char in input_value:
            value = MapRomanToDecimal.INTS[MapRomanToDecimal.NUMS.index(char)]
            # If the next place holds a larger number, this value is negative.
            try:
                nextvalue = MapRomanToDecimal.INTS[MapRomanToDecimal.NUMS.index(input_value[charnum + 1])]
                if nextvalue > value:
                    value *= -1
            except IndexError:
                # there is no next place.
                pass
            places.append(value)
            charnum += 1
        total = 0
        for num in places:
            total += num
        return str(total)


class MapDecimalToRoman(DynamicMap):

    NAME = "DECTOROMAN"
    INTS = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    NUMS = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')

    def __init__(self, config):
        DynamicMap.__init__(self, config)

    def map_value(self, client_context, input_value):
        input_value = int(input_value)
        if not 0 < input_value < 4000:
            raise ValueError("Argument must be between 1 and 3999")
        result = ""
        num = 0
        for num_str in MapDecimalToRoman.NUMS:
            # No need to check for div by 0 as the sets of ints does not contain 0
            count = input_value // MapDecimalToRoman.INTS[num]
            result += num_str * count
            input_value -= MapDecimalToRoman.INTS[num] * count
            num += 1
        return result
