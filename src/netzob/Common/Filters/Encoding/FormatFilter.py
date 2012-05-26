# -*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Frédéric Guihéry                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports
#+---------------------------------------------------------------------------+
import logging
from netzob.Common.Type.Format import Format
from netzob.Common.Filters.EncodingFilter import EncodingFilter
from netzob.Common.Type.TypeConvertor import TypeConvertor
from netzob.Common.Type.UnitSize import UnitSize

#+---------------------------------------------------------------------------+
#| Related third party imports
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Local application imports
#+---------------------------------------------------------------------------+


#+---------------------------------------------------------------------------+
#| FormatFilter:
#|     Definition of an encoding filter which apply a format on a message
#+---------------------------------------------------------------------------+
class FormatFilter(EncodingFilter):

    TYPE = "FormatFilter"

    def __init__(self, name, formatType, unitSize):
        EncodingFilter.__init__(self, FormatFilter.TYPE, name)
        self.formatType = formatType
        self.unitsize = unitSize

    def apply(self, message):

        if self.unitsize != UnitSize.NONE:
            # First we apply the unit size
            # Default modulo = 2 => 8BITS
            modulo = UnitSize.getSizeInBits(self.unitsize) / 4

            splittedData = []
            tmpResult = ""
            for i in range(0, len(message)):
                if i > 0 and i % modulo == 0:
                    splittedData.append(tmpResult)
                    tmpResult = ""
                tmpResult = tmpResult + message[i]
            splittedData.append(tmpResult)
        else:
            splittedData = [message]

        # Now we have the message splitted per unit size
        # we encode each data
        encodedSplittedData = []
        for d in splittedData:
            encodedSplittedData.append(TypeConvertor.encodeNetzobRawToGivenType(d, self.formatType))

        # Before sending back (;D) we join everything
        return " ".join(encodedSplittedData)

    def getConversionAddressingTable(self, message):
        return None