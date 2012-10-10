

def do_the_stuff(balance, annualInterestRate, monthlyPaymentRate):
    total_paid = 0.0
    month = 0
    while month < 12:
        month += 1
        print "Month:", month
        minimal_payment = round(balance * monthlyPaymentRate, 2)
        total_paid += minimal_payment
        print "Minimum monthly payment:", minimal_payment
        balance = round((balance - minimal_payment)
                        * (1.0 + annualInterestRate / 12.0), 2)
        print "Remaining balance:", balance
    print "Total paid:", total_paid
    print "Remaining balance:", balance
