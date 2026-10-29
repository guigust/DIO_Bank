class BusinessError(Exception):
    pass


class AccountNotFoundError(BusinessError):
    pass


class AccountInactiveError(BusinessError):
    pass


class InsufficientBalanceError(BusinessError):
    pass