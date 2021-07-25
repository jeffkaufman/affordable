def max_monthly_payment(
    # Median Family Income (MFI) per HUD for
    # Boston-Cambridge-Quincy
    median_family_income,

    # Are we looking at a sale or rental?
    is_rental,

    # How big is the unit?
    # 0 for studio, 1 for 1br, etc
    n_bedrooms):

  tier3_rental = [
      17.85, 21.00, 24.00, 27.00, 30.00,
      33.00, 36.00, 39.00, 42.00]
  tier3_sale = [
      21.66, 25.48, 29.12, 32.76, 36.40,
      40.04, 43.68, 47.32, 50.96]

  tier3 = tier3_rental if is_rental else tier3_sale

  base_price = (
    median_family_income *
    tier3[n_bedrooms] * 0.01)

  raw_monthly_payment = base_price / 12

  # For rentals:
  #  * utilities
  #  * parking (skip)
  #  * amenities (skip)
  # For sales:
  #  * private mortgage insurance
  #  * real estate taxes,
  #  * condominium fees
  #  * homeowners insurance
  #  * parking fees (skip)
  # This is hard, so just use the $375 which
  # the ordinance gives as an example
  estimated_standard_deduction = 375

  return raw_monthly_payment - \
      estimated_standard_deduction

"""
print("<tr><th>Bedrooms")
for i in range(9):
  v = "%sbr" % i
  if i == 0:
    v = "studio"
  print ("  <th>%s" % v)
print("<tr><th>Rental")
for i in range(9):
  print ("  <td>$%.0f" % (max_monthly_payment(120800, True, i)))
print("<tr><th>Sale")
for i in range(9):
  print ("  <td>$%.0f" % (max_monthly_payment(120800, False, i)))
"""

def monthly_payment(loan_amount, annual_interest_rate):
  monthly_interest_rate = annual_interest_rate / 12
  return (
    loan_amount * monthly_interest_rate *
    (1 + monthly_interest_rate)**360 /
    ((1 + monthly_interest_rate)**360-1))

def max_mortgage_loan(monthly_payment, annual_interest_rate):
  monthly_interest_rate = annual_interest_rate / 12
  return monthly_payment / (
    monthly_interest_rate *
    (1 + monthly_interest_rate)**360 /
    ((1 + monthly_interest_rate)**360-1))

def max_sale_price(
    # Output of max_monthly_payment()
    monthly_payment,
    # 30y fixed conventional
    mortgage_rate):
  monthly_interest_rate = mortgage_rate / 12
  max_mortgage_loan = monthly_payment / (
    monthly_interest_rate *
    (1 + monthly_interest_rate)**360 /
    ((1 + monthly_interest_rate)**360-1))
  return max_mortgage_loan * 1.03

print("<tr><th>Bedrooms")
for i in range(9):
  v = "%sbr" % i
  if i == 0:
    v = "studio"
  print ("  <th>%s" % v)
print("<tr><th>Sale Price")
for i in range(9):
  print ("  <td>$%.0f" % (
    max_sale_price(max_monthly_payment(120800, False, i),
#                   0.0278)))
                   0.05)))
