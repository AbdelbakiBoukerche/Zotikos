class ZotikosException(Exception):

    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg


class ZotikosConfigFileNotFound(ZotikosException):

    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg
