from flask import Flask, render_template, request, redirect

from yenepay.PaymentHandler import PaymentHandler, ProcessType, PDT, Item, IPN

app = Flask(__name__)

# you can get your merchant code and pdt token from your yenepay dashboard
MERCHANT_CODE = "SB1286"        
PDT_TOKEN = "Q7kc5gDaHEyjBi"

USE_SANDBOX = True              # whether we are using yenepay production or sandbox server - 
                                # set to true if testing

# create PaymentHandler object
handler = PaymentHandler(MERCHANT_CODE, useSandbox=USE_SANDBOX)

# fill required attributes
handler.success_url = "http://localhost:5000/success"
handler.failure_url = "http://localhost:5000/failure"
handler.cancel_url = "http://localhost:5000/cancel"
handler.ipn_url = "http://localhost:5000/ipn"

handler.checkout_process = ProcessType.Express
handler.expires_after = 600
handler.merchant_order_id = "order-001"

# items to sell
# Item(id, name, price, quantity)
car = Item("item-0", "Car", 100, 1)
plane = Item("item-1", "Plane", 120, 1)

items = [car, plane]

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        
        # get what the user selected
        index = int(request.form.get("index"))
        item = items[index]

        # add item to order
        handler.add_item(item)

        # set additional fees
        handler.total_delivery_fee = 0
        handler.total_handling_fee = 0
        handler.total_discount = 0
        handler.total_vat = item.unit_price * item.item_quantity * 0.15

        # generate yenepay checkout url
        url = handler.get_checkout_url()

        # redirect user to yenepay payment url to complete payment
        return redirect(url)

    return render_template("index.html")


# on payment success yenepay redirects here
# you can request pdt at this point and check payment status
@app.route("/success")
def success():
    
    # create pdt object
    pdt = PDT(PDT_TOKEN)

    # we get MerchantOrderId and TransactionId from yenepay response
    # set pdt attributes properly
    pdt.merchant_order_id = request.args.get("MerchantOrderId")
    pdt.transaction_id = request.args.get("TransactionId")

    resp = handler.request_pdt(pdt)

    if resp["result"] == "SUCCESS" and resp["Status"] == "Paid":
        # This means the payment is completed
        # You can mark the order as paid here and start delivery
        return "ok"
    
    else:
        # This means the pdt request has failed.
        return "Pdt request failed"

# canceling payment redirects here
@app.route("/cancel")
def cancel():
    # create pdt object
    pdt = PDT(PDT_TOKEN)

    # we get MerchantOrderId and TransactionId from yenepay response
    # set pdt attributes properly
    pdt.merchant_order_id = request.args.get("MerchantOrderId")
    pdt.transaction_id = request.args.get("TransactionId")

    resp = handler.request_pdt(pdt)

    if resp["result"] == "SUCCESS" and resp["Status"] == "Canceled":
        # This means the payment is canceled
        # You can mark the order as Canceled here
        return "canceled"
    
    else:
        # This means the pdt request has failed.
        return "Pdt request failed"


# on failure we are redirected here
@app.route("/failure")
def failure():
    return "failure"

# accepts Instant payment notification from yenepay and validates it
@app.route("/ipn", methods=["POST"])
def ipn():
    # get yenepay response as dictionary
    response = request.form.to_dict()

    # create ipn object
    ipn = IPN()

    # fill ipn attributes from dictionary(response)
    ipn.from_dict(response)

    if handler.is_ipn_authentic(ipn):
        # This means the payment is completed
	    # You can now mark the order as "Paid" or "Completed" here and start the delivery process
        return "ipn authentic"
    
    else:
        # this means the payment failed
        return "Invalid ipn"


if __name__ == "__main__":
    app.run(debug=True)