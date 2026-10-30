from enum import Enum


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    PIX = 'pix'
    TED = 'ted'
    TRANSFER = 'transfer'