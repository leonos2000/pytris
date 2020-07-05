import os

class SimplestGui:

    def __init__(self):
        pass
        self._clean()

    def _clean(self):
        if 'nt' in os.name:
            os.system('cls')
        else:
            os.system('clear')

    def render(self, data):
        data = self.mirrorData(data)

        buffer = '╔'

        for i in range(len(data[0])):
            buffer += '═'
        buffer += '╗\r\n'

        for i in data:
            buffer += '║'
            for j in i:
                buffer += '█' if j else ' '
            buffer += '║\r\n'

        buffer += '╚'
        for i in range(len(data[0])):
            buffer += '═'

        buffer += '╝'
        
        self._clean()
        print(buffer)

    def mirrorData(self, data):
        output = []

        for i in range(len(data) - 1, -1, -1):
            output.append(data[i])

        return output