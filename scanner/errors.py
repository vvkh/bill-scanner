class ScannerException(Exception):
    pass


class BadFormat(ScannerException):
    pass


class BadCSV(ScannerException):
    pass
