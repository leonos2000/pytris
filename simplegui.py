import os
from colorama import Back
from colorama import Style

class SimplestGui:

    def __init__(self):
        pass
        self._clean()

    def _clean(self):
        if 'nt' in os.name:
            os.system('cls')
        else:
            os.system('clear')

    def render(self, data, hold):
        data = self.mirrorData(data)

        buffer = '╔'

        for i in range(len(data[0])):
            buffer += '═'
        buffer += '╗\r\n'

        for i in data:
            buffer += '║'
            for j in i:
                buffer += self.color(j)
                buffer += ' '
                buffer += Style.RESET_ALL
            buffer += '║\r\n'

        buffer += '╚'
        for i in range(len(data[0])):
            buffer += '═'

        buffer += '╝\r\n'

        for i in hold:
            for j in i:
                buffer += self.color(j)
                buffer += ' '
                buffer += Style.RESET_ALL
            buffer += '\r\n'
        
        self._clean()
        print(buffer)

    def mirrorData(self, data):
        output = []

        for i in range(len(data) -1, -1, -1):
            output.append(data[i])

        return output

    def color(self, color):
        colors = [Back.CYAN, Back.WHITE, Back.BLUE,
                  Back.GREEN, Back.RED, Back.YELLOW, Back.MAGENTA, '']
        try:
            return colors[color]
        except:
            return ''