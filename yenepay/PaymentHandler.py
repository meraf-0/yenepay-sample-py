from typing import List, Type

from urllib.parse import parse_qsl
import json
import requests

from yenepay.Models import IPN, PDT, Item


class ProcessType:
    Express: str = "Express"
    Cart: str = "Cart"


class PaymentHandler:

    CHECKOUT_BASE_URL_PROD = "https://endpoints.yenepay.com/api/urlgenerate/getcheckouturl/"
    CHECKOUT_BASE_URL_SANDBOX = "https://testapi.yenepay.com/api/urlgenerate/getcheckouturl/"

    IPN_VERIFY_URL_PROD = "https://endpoints.yenepay.com/api/verify/ipn/"
    IPN_VERIFY_URL_SANDBOX = "https://testapi.yenepay.com/api/verify/ipn/"

    PDT_URL_PROD = "https://endpoints.yenepay.com/api/verify/pdt/"
    PDT_URL_SANDBOX = "https://testapi.yenepay.com/api/verify/pdt/"

    def __init__(self, merchantId: str, useSandbox: bool = True) -> None:

        # set True for testing (to use yenepay sandbox server) 
        # set False for production
        self.useSandbox: bool = useSandbox
        
        # An all numeral (minimum 4-digit) unique seller code used to uniquely identify a merchant on YenePay
        self.merchantId: str = merchantId
        
        # String representing the type of checkout process (check class CheckoutType for full list of valid values)
        self.process: str = ProcessType.Cart

        # Id that identifies the order on the merchant application 
        self.merchantOrderId: str = "0"

        # List of items
        self.items: List[Item] = []
        
        # endpoint url on a merchant site used to send instant payment notifications (IPN)
        self.ipnUrl: str = None

        # endpoint url on a merchant site used to return a customer after a payment is successfully completed on YenePay
        self.successUrl: str = None

        # endpoint url on a merchant site used to return a customer after cancelling a payment on YenePay
        self.cancelUrl: str = None

        # endpoint url on a merchant site used to return a customer when a payment fails on YenePay
        self.failureUrl: str = None

        # The number of minutes before an order expires
        self.expiresAfter: int = None

        # Expiration period for this payment in days
        self.expiresInDays: int = None

        # Total delivery fee for the order (if applicable)
        self.totalItemsDeliveryFee: float = None

        # Total handling fee for the order (if applicable)
        self.totalItemsHandlingFee: float = None

        # Total discount amount for the order (if applicable)
        self.totalItemsDiscount: float = None
        
        # Total VAT amount. Set only for VAT registered merchants
        self.totalItemsTax1: float = None

        # Total TOT amount. Set only for TOT registered merchants
        self.totalItemsTax2: float = None
    
    @property
    def use_sandbox(self) -> bool:

        return self.useSandbox

    @use_sandbox.setter
    def use_sandbox(self, useSandbox) -> None:

        self.useSandbox = useSandbox

    @property
    def merchant_id(self) -> str:

        return self.merchantId
    
    @merchant_id.setter
    def merchant_id(self, id_: str) -> None:

        self.merchantId = id_
    
    @property
    def checkout_process(self) -> str:

        return self.process
    
    @checkout_process.setter
    def checkout_process(self, process: str) -> None:

        if process in ProcessType.__dict__.values():
            self.process = process
        
        else:
            raise TypeError(f"Unknown Process type: {process}")
    
    @property
    def merchant_order_id(self) -> str:

        return self.merchantOrderId
    
    @merchant_order_id.setter
    def merchant_order_id(self, order_id: str) -> None:

        self.merchantOrderId = order_id
    
    @property
    def ipn_url(self) -> str:

        return self.ipnUrl
    
    @ipn_url.setter
    def ipn_url(self, url: str) -> None:

        self.ipnUrl = url
    
    @property
    def success_url(self) -> str:

        return self.successUrl
    
    @success_url.setter
    def success_url(self, url: str) -> None:

        self.successUrl = url

    @property
    def cancel_url(self) -> str:

        return self.cancelUrl
    
    @cancel_url.setter
    def cancel_url(self, url: str) -> None:

        self.cancelUrl = url
    
    @property
    def failure_url(self) -> str:

        return self.failureUrl
    
    @failure_url.setter
    def failure_url(self, url: str) -> None:

        self.failureUrl = url
    
    @property
    def expires_after(self) -> int:

        return self.expiresAfter
    
    @expires_after.setter
    def expires_after(self, minute: int) -> None:

        self.expiresAfter = minute
    
    @property
    def expires_in_days(self) -> int:

        return self.expiresInDays
    
    @expires_in_days.setter
    def expires_in_days(self, day: int) -> None:

        self.expiresInDays = day
    
    @property
    def total_delivery_fee(self) -> float:

        return self.totalItemsDeliveryFee
    
    @total_delivery_fee.setter
    def total_delivery_fee(self, fee: float) -> None:

        if fee < 0:
            fee = 0

        self.totalItemsDeliveryFee = fee
    
    @property
    def total_handling_fee(self) -> float:

        return self.totalItemsHandlingFee
    
    @total_handling_fee.setter
    def total_handling_fee(self, fee: float) -> None:

        if fee < 0:
            fee = 0

        self.totalItemsHandlingFee = fee
    
    @property
    def total_discount(self) -> float:

        return self.totalItemsDiscount
    
    @total_discount.setter
    def total_discount(self, discount: float) -> None:

        if discount < 0:
            discount = 0

        self.totalItemsDiscount = discount
    
    @property
    def total_vat(self) -> float:

        return self.totalItemsTax1
    
    @total_vat.setter
    def total_vat(self, vat: float) -> None:

        if vat < 0:
            vat = 0

        self.totalItemsTax1 = vat
    
    @property
    def total_tot(self) -> float:

        return self.totalItemsTax1
    
    @total_tot.setter
    def total_tot(self, tot: float) -> None:

        if tot < 0:
            tot = 0

        self.totalItemsTax2 = tot
    
    # adds item to items list
    # if item with the same id is found in items list its quantity will be set appropirately
    def add_item(self, item: Item) -> None:

        # a safeguard to prevent adding morethan one item in express mode
        if self.process == ProcessType.Express:
            if self.__len__() == 1 and self.items[0]["itemId"] != item.item_id:
                raise Exception("Can't add morethan one item in Express mode, use Cart mode instead")

        item = item.as_dict()

        for i in self.items:
            if i["itemId"] == item["itemId"]:
                i["quantity"] += item["quantity"]
                break
        
        else:
            self.items.append(item)

    # removes item from items list by id (if found)
    def remove_item(self, id_: str) -> None:
        
        i = 0
        while (i < len(self.items)):
            if self.items[i]["itemId"] == id_:
                del self.items[i]
                break
            
            i += 1

    # resets checkout values to begin new checkout
    def clear(self) -> None:
        self.process: str = ProcessType.Cart
        self.merchantOrderId: str = "0"
        self.items: List[Item] = []
        self.expiresAfter: int = None
        self.expiresInDays: int = None
        self.totalItemsDeliveryFee: float = None
        self.totalItemsHandlingFee: float = None
        self.totalItemsDiscount: float = None
        self.totalItemsTax1: float = None
        self.totalItemsTax2: float = None

    # returns dictionary representation of checkout with keys yenepay expects
    def as_dict(self) -> dict:
        
        # yenepay checkout parameters
        checkout_params = ['merchantId', 'process', 'merchantOrderId', 'items', 'ipnUrl', 'successUrl', 'cancelUrl', 'failureUrl', 'expiresAfter', 'totalItemsDeliveryFee', 'totalItemsHandlingFee', 'totalItemsDiscount', 'totalItemsTax1', 'totalItemsTax2']
        
        d = {}

        for k, v in self.__dict__.items():
            if v != None and k in checkout_params:
                d[k] = v

        return d
    
    # returns checkout url retruned from yenepay api endpoint
    # redirect cliend to this url to complete payment
    def get_checkout_url(self) -> str:
         
        query: json = json.dumps(self.as_dict())

        header: dict = {"Content-Type": "application/json"}

        if self.use_sandbox:
            url = self.CHECKOUT_BASE_URL_SANDBOX
        else:
            url =  self.CHECKOUT_BASE_URL_PROD

        response = requests.post(url, data = query, headers = header)

        return response.json()['result']
    
    # check if IPN model is authentic
    def is_ipn_authentic(self, ipn: IPN) -> bool:
        
        query: json = json.dumps(ipn.as_dict())

        header: dict = {"Content-Type": "application/json"}

        if self.use_sandbox:
            url = self.IPN_VERIFY_URL_SANDBOX
        else:
            url =  self.IPN_VERIFY_URL_PROD
        
        response = requests.post(url, data = query, headers = header)

        if response.status_code == 200:
            return True
        
        return False
    
    # request PDT 
    # returns yenepay response
    def request_pdt(self, pdt: PDT):

        query: json = json.dumps(pdt.as_dict())        

        header: dict = {"Content-Type": "application/json"}

        if self.use_sandbox:
            url = self.PDT_URL_SANDBOX
        else:
            url =  self.PDT_URL_PROD
        
        response = requests.post(url, data = query, headers = header)

        if response.status_code == 200:
            return dict(parse_qsl(response.json()))

        return None
    
    # returns number of items 
    def __len__(self) -> int:
        return len(self.items)
    
    # string representation of checkout
    def __str__(self) -> str:
        
        s = ''
        
        for k, v in self.__dict__.items():
            s += f"{k} : {v}\n"
        
        return s
    

        
