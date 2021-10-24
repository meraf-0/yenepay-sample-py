class Item:

    def __init__(self, itemId, itemName, itemPrice, totalQuantity):
        
        # Unique identifier of the item
        self.itemId: str = itemId

        # Name of the item
        self.itemName: str = itemName

        # Unit price of the item
        self.unitPrice: float = itemPrice

        # Total quantity of the item.
        self.quantity: int = totalQuantity
    
    @property
    def item_id(self):

        return self.itemId
    
    @item_id.setter
    def item_id(self, id_):

        self.itemId = id_
    
    @property
    def item_name(self):

        return self.itemName
    
    @item_name.setter
    def item_name(self, name):

        self.itemName = name
    
    @property
    def unit_price(self):

        return self.unitPrice
    
    @unit_price.setter
    def unit_price(self, price):

        if price < 0:
            raise ValueError(f"Invalid Price: got negative price {price}")

        self.unitPrice = price
    
    @property
    def item_quantity(self):

        return self.quantity
    
    @item_quantity.setter
    def item_quantity(self, q):

        if q < 0:
            raise ValueError(f"Invalid Quantity: got negative quantity {q}")

        self.quantity = q
    
    # dictionary representation of Item
    def as_dict(self):
        
        d = {}

        for k, v in self.__dict__.items():
            if v != None:
                d[k] = v

        return d

# Payment data transfer
class PDT:

    def __init__(self, pdtToken: str):

        # PDT Request Type
        self.requestType: str = "PDT"

        # merchant PDT Token
        self.pdtToken: str = pdtToken

        # the YenePay transaction id of the order being requested
        self.transactionId: str = ""

        # The merchant order id
        self.merchantOrderId: str =  ""
    
    @property
    def pdt_token(self) -> str:

        return self.pdtToken
    
    @pdt_token.setter
    def pdt_token(self, token: str) -> None:

        self.pdtToken = token
    
    @property
    def transaction_id(self) -> str:

        return self.transactionId
    
    @transaction_id.setter
    def transaction_id(self, id_: str) -> None:

        self.transactionId = id_
    
    @property
    def merchant_order_id(self) -> str:

        return self.merchantOrderId
    
    @merchant_order_id.setter
    def merchant_order_id(self, id_: str) -> None:

        self.merchantOrderId = id_

    # dictionary representation of PDT
    def as_dict(self):

        return self.__dict__
    
    # string representation of PDT
    def __str__(self) -> str:
        
        s = ''
        
        for k, v in self.__dict__.items():
            s += f"{k} : {v}\n"
        
        return s


# Instant Payment Notification
class IPN:

    def __init__(self):
        
        # Total amount paid
        self.totalAmount: float = None
        
        # The customer's id on YenePay
        self.buyerId: str = None

        # Id that identifies the order on the merchant application
        self.merchantOrderId: str = None

        # your YenePay merchant account unique identifier
        self.merchantId: str = None

        # your YenePay merchant account code (minimum 4-digit)
        self.merchantCode: str = None

        # an identifier for the payment order assigned by YenePay
        self.transactionId: str = None

        # an order code for the payment order assigned by YenePay
        self.transactionCode: str = None

        # Order status value for the payment
        self.status: str = None

        # Currency code used for payment
        self.currency: str = None

        # digital signature of the ipn
        self.signature: str = None
    
    @property
    def total_amount(self) -> float:
        return self.totalAmount
    
    @total_amount.setter
    def total_amount(self, amount: float) -> None:
        self.totalAmount = amount
    
    @property
    def buyer_id(self) -> str:
        return self.buyerId
    
    @buyer_id.setter
    def buyer_id(self, id_: str) -> None:
        self.buyerId = id_
    
    @property
    def merchant_order_id(self) -> str:
        return self.merchantOrderId
    
    @merchant_order_id.setter
    def merchant_order_id(self, id_: str) -> None:
        self.merchantOrderId = id_
    
    @property
    def merchant_id(self) -> str:
        return self.merchantId
    
    @merchant_id.setter
    def merchant_id(self, id_: str) -> None:
        self.merchantId = id_
    
    @property
    def merchant_code(self) -> str:
        return self.merchantCode
    
    @merchant_code.setter
    def merchant_code(self, id_: str) -> None:
        self.merchantCode = id_

    @property
    def transaction_id(self) -> str:
        return self.transactionId
    
    @transaction_id.setter
    def transaction_id(self, id_: str) -> None:
        self.transactionId = id_
    
    @property
    def transaction_code(self) -> str:
        return self.transactionCode
    
    @transaction_code.setter
    def transaction_code(self, id_: str) -> None:
        self.transactionCode = id_
    
    @property
    def payment_status(self) -> str:
        return self.status
    
    @payment_status.setter
    def payment_status(self, stat: str) -> None:
        self.status = stat
    
    @property
    def payment_currency(self) -> str:
        return self.currency
    
    @payment_currency.setter
    def payment_currency(self, currency: str) -> None:
        self.currency = currency
    
    @property
    def payment_signature(self) -> str:
        return self.signature
    
    @payment_signature.setter
    def payment_signature(self, signature: str) -> None:
        self.signature = signature
    
    # fill IPN object attributes from dictionary
    def from_dict(self, d: dict) -> None:
        
        self.totalAmount = d["TotalAmount"]
        self.buyerId = d["BuyerId"]
        self.merchantOrderId = d["MerchantOrderId"]
        self.merchantId = d["MerchantId"]
        self.merchantCode = d["MerchantCode"]
        self.transactionId = d["TransactionId"]
        self.transactionCode = d["TransactionCode"]
        self.status = d["Status"]
        self.currency = d["Currency"]
        self.signature = d["Signature"]
    
    def as_dict(self) -> dict:
        d = {}

        for k, v in self.__dict__.items():
            if v != None:
                d[k] = v

        return d