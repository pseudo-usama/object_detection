class log:
    def __init__(self, fileName):
        self.fileName = fileName

    def info(self, msj):
        print(f'[{self.fileName}] {msj}')
