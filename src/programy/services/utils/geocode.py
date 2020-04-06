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

class GeoCodeUtils:

    @staticmethod
    def float_to_aiml_string(value):
        if value < 0:
            valSign = "NEG"
        else:
            valSign = "POS"

        splits = "{0}".format(abs(value)).split(".")

        valDec = splits[0]
        valFrac = splits[1]

        return "SIGN {0} DEC {1} FRAC {2}".format(valSign, valDec, valFrac)

    @staticmethod
    def aiml_lat_lng(latText, lngText):
        return "LAT {0} LNG {1}".format(latText, lngText)

    @staticmethod
    def aiml_string_to_float(text_sign, text_dec, text_frac):

        if text_sign == 'POS':
            str = "{0}.{1}".format(text_dec, text_frac)

        elif text_sign == 'NEG':
            str = "-{0}.{1}".format(text_dec, text_frac)

        else:
            raise ValueError("Invalid geocode sign value [{0}]".format(text_sign))

        return float(str)
