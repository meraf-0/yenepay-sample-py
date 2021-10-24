# Sample Shop Application in PHP using YenePay for Payment

This library allows you to quickly and easily add YenePay as a payment method using Python

# Pre-requisite

To add YenePay to your application and start collecting payments, you will first need to register on YenePay as a merchant and get your seller code. You can do that from https://www.yenepay.com/merchant

# Installation

```git clone https://github.com/meraf-0/yenepay-sample-py.git```

You will find the wrapper in yenepay folder

# Usage

Step 1: Import yenepay.PaymentHandler
```from yenepay.PaymentHandler import PaymentHandler, ProcessType, PDT, Item, IPN```

Step 2: Initialize handler
```handler = PaymentHandler('YOUR MERCHANT CODE', useSandbox='TRUE IF YOU ARE TESTING')```

Step 3: Set required fields for more information look at the official yenepay community website
```
handler.success_url = 'YOUR SUCCESS URL'
handler.failure_url = "YOUR FAILURE URL"
handler.cancel_url = "YOUR CANCEL URL"
handler.ipn_url = "YOUR IPN URL"

handler.checkout_process = 'EITHER EXPRESS OR CART'
handler.expires_after = 'MINUTES BEFORE ORDER EXPIRES'
handler.merchant_order_id = 'ORDER ID INSIDE YOUR SYSTEM'
.
.
.
```

Step 4: Add implemetations from PDT, IPN ... (sample example included in this repository)

# Finally
 When you are ready to deploy set ```useSandbox = False``` (look at Step 2)


