'''
This is a simple script based on gdax unofficial python library (pip install gdax)  
to quickly view the status of your account.
The output will be like:
-----------------------
Account holdings:
 BTC: 0.0137673900000000
 LTC: 0.1861050000000000
 EUR: 0.0000000000000000
 ETH: 0.0300189900000000
 BCH: 0.0000000000000000


Open orders:
 2017-12-23T08:50:21.30903Z -> LTC-EUR: sell 0.18610500 LTC at 500.00000000 EUR --> 93.0525
 2017-12-23T08:48:05.43861Z -> ETH-EUR: sell 0.03001899 ETH at 730.00000000 EUR --> 21.9138627
 2017-12-22T22:48:50.621473Z -> BTC-EUR: sell 0.00322393 BTC at 15000.00000000 EUR --> 48.35895
 2017-12-20T16:29:32.935117Z -> BTC-EUR: sell 0.01054346 BTC at 17500.00000000 EUR --> 184.51055


Total expected amount in euros of sell orders
 347.8358627 EUR

Last 10 settled fills:
 2017-12-22T22:48:05.087Z -> BTC-EUR: buy 0.00322393 BTC at 13391.10000000 EUR
 2017-12-22T22:44:45.158Z -> BTC-EUR: sell 0.00282647 BTC at 13297.55000000 EUR
 2017-12-20T16:23:38.465Z -> BTC-EUR: buy 0.00434216 BTC at 14146.49000000 EUR
 2017-12-19T13:28:40.392Z -> BTC-EUR: buy 0.00620130 BTC at 15742.80000000 EUR
 2017-12-17T13:46:59.848Z -> BTC-EUR: sell 0.00191312 BTC at 16911.00000000 EUR
 2017-12-16T12:48:27.307Z -> BTC-EUR: buy 0.00191312 BTC at 15642.01000000 EUR
 2017-12-15T10:32:27.848Z -> BTC-EUR: sell 0.00215459 BTC at 15000.00000000 EUR
 2017-12-14T14:51:17.014Z -> BTC-EUR: buy 0.00215459 BTC at 13889.01000000 EUR
 2017-12-22T22:59:52.208Z -> ETH-EUR: buy 0.03001899 ETH at 638.00000000 EUR
 2017-12-22T22:46:09.629Z -> ETH-EUR: sell 0.03977950 ETH at 629.64000000 EUR


Tickers:
 ETH-EUR ticker: 641.34000000
 LTC-EUR ticker: 253.30000000
 BTC-EUR ticker: 13276.18000000
 -----------------------

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
'''

import gdax
import json

def convert_to_eur(amount, exchange_ratio):
	return amount * exchange_ratio

key = 'your_api_key'
passphrase = 'your_passphrase'
b64secret = 'your_one_time_b64secret'

fills_to_show = 10

auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)


accounts = auth_client.get_accounts()
# print json.dumps(accounts, indent=4, sort_keys=True)
print "Account holdings:"
for account in accounts:
	print ' ' + account['currency'] + ": " + account['hold']
print '\n'

total_expected_amount_euros = 0
orders = auth_client.get_orders()[0]
# print json.dumps(orders, indent=4, sort_keys=True)
print "Open orders:"
for order in orders:
	if order['side'] == 'sell':
		expected_amount = convert_to_eur(float(order['size']),float(order['price']))
		total_expected_amount_euros += expected_amount
	print ' ' + order['created_at'] + ' -> ' + order['product_id'] + ": " + order['side'] + ' ' + order['size'] + ' ' + order['product_id'][:3] + ' at ' + order['price'] + ' EUR' + ' --> ' + str(expected_amount)
print '\n'

print 'Total expected amount in euros of sell orders\n ' + str(total_expected_amount_euros) + ' EUR' + '\n' 

fills = auth_client.get_fills(limit=fills_to_show)[0]
# print json.dumps(fills, indent=4, sort_keys=True)
print 'Last ' + str(fills_to_show) + ' settled fills:'
for fill in fills:
	print ' ' + fill['created_at'] + ' -> ' + fill['product_id'] + ": " + fill['side'] + ' ' + fill['size'] + ' ' + fill['product_id'][:3] + ' at ' + fill['price'] + ' EUR'
print '\n'

print "Tickers:"
ETH_EUR_ticker = auth_client.get_product_ticker(product_id='ETH-EUR')['price']
print ' ETH-EUR ticker: ' + ETH_EUR_ticker 
LTC_EUR_ticker = auth_client.get_product_ticker(product_id='LTC-EUR')['price']
print ' LTC-EUR ticker: ' + LTC_EUR_ticker 
BTC_EUR_ticker = auth_client.get_product_ticker(product_id='BTC-EUR')['price']
print ' BTC-EUR ticker: ' + BTC_EUR_ticker 
