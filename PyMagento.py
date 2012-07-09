import xmlrpclib
import random
import csv

class Magento(object):
	''' Add default login details here if required '''
	passwd = 'password'
	usr = 'remote'
	URL = 'http://magento.enterprise.com:10088/magento/index.php/api/xmlrpc/'
	svr = ''
	token = ''
	def __init__(self, URL=None, usr=None, passwd=None):
		if URL<>None:
			self.URL = URL
		if usr<>None:
			self.usr = usr
		if passwd<>None:
			self.passwd = passwd
		random.seed()
	def connect(self, URL=None, usr=None, passwd=None):
		if URL==None:
			URL = self.URL
		if usr==None:
			usr = self.usr
		if passwd==None:
			passwd = self.passwd
		self.svr = xmlrpclib.ServerProxy(URL)
		print passwd, usr
		self.token = self.svr.login(usr, passwd)
		print self.token
	def populateRandomStock(self):
		products = self.svr.call(self.token, 'catalog_product.list')
		for product in products:
			sku = product['sku']
			stock = random.randint(0,1000)
			parms = [sku,{'qty':stock, 'is_in_stock':1}]
			print parms
			status = self.svr.call(self.token, 'product_stock.update', parms)
			print '%s - %s - %s \n' % (sku, stock, status)
	def listOrdersByStatus(self, status):
		filter = [{"status":{"=":status}}]
		orders = self.svr.call(self.token, 'sales_order.list', filter)
		for order in orders:
			info = self.svr.call(self.token, 'sales_order.info', [order['increment_id']])
			print info
	def listOrdersSinceDate(self, orderdate):
		filter = [{"created_at":{"gt":orderdate}}]
		orders = self.svr.call(self.token, 'sales_order.list', filter)
		for order in orders:
			info = self.svr.call(self.token, 'sales_order.info', [order['increment_id']])
			print info
	def listOrdersSinceStatusDate(self, status, orderdate):
		filter = [{"created_at":{"gt":orderdate},"status":{"eq":status}}]
		orders = self.svr.call(self.token, 'sales_order.list', filter)
		for order in orders:
			info = self.svr.call(self.token, 'sales_order.info', [order['increment_id']])
			print info
	def createStockCSV(self, filename):
		outfile = csv.writer(open(filename, 'w'))
		products = self.svr.call(self.token, 'catalog_product.list')
		for product in products:
			sku = product['sku']
			stk = self.svr.call(self.token, 'product_stock.list',[sku])
			if stk[0]['qty'] is None:
				stock = 0
			else:
				stock = stk[0]['qty']
			outfile.writerow([sku, stock])
	def populateStockFromCSV(self, filename):
		infile = csv.reader(open(filename))
		for row in infile:
			sku = row[0]
			stock = row[1]
			parms = [sku,{'qty':stock, 'is_in_stock':1}]
			print parms
			status = self.svr.call(self.token, 'product_stock.update', parms)
			print '%s - %s - %s \n' % (sku, stock, status)
	def populateStockPriceFromCSV(self, filename):
		infile = csv.reader(open(filename))
		for row in infile:
			(sku, stock, is_in_stock, price) = (row[1:5])
			try:
				checkProd=self.svr.call(self.token, 'catalog_product.info',[sku])
			except:
				print 'SKU %s not in database\n' % sku
				pass
			stk = self.svr.call(self.token, 'product_stock.list',[sku])
			prod_id = stk[0]['product_id']
			parms = [sku,{'product_id':prod_id,'qty':str(stock), 'is_in_stock':str(is_in_stock)}]
			status = self.svr.call(self.token, 'product_stock.update', parms)
			print 'Updated stock %s - %s - %s\n' % (sku, stock, status)
			parms = [sku,{'price':str(price)}]
			status = self.svr.call(self.token, 'catalog_product.update', parms)
			print 'Updated price %s - %s - %s\n' % (sku, price, status)
	def getProductArray(self):
		return self.svr.call(self.token, 'catalog_product.list')
	def getImagesForSku(self, sku):
		return self.svr.call(self.token, 'catalog_product_attribute_media.list', [sku])
	def updateImagePos(self, sku, filename, pos):
		parms = [sku, filename, {'position':pos}]
		result = self.svr.call(self.token, 'catalog_product_attribute_media.update', parms)	
		return result
			
		
	
if __name__ == "__main__":
	Mag = Magento()
	Mag.connect()
	Mag.listOrdersByStatus('processing')
	print dir(Mag)
	
""" // - array("from"=>$fromValue, "to"=>$toValue)
// - array("like"=>$likeValue)
// - array("neq"=>$notEqualValue)
// - array("in"=>array($inValues))
// - array("nin"=>array($notInValues))
// - array("eq"=>$equal)
// - array("nlike"=>$notlike )
// - array("is"=>$is )
// - array("gt"=>$greaterthan )
// - array("lt"=>$lessthan )
// - array("gteq"=>$greterthanequal )
// - array("lteq"=>$lessthanequal )
// - array("finset"=>$unknown ) """