import PyMagento

class Mage_Migrate(object):
	def __init__(self):
		return
	def Migrate(self, src, dest):
		''' Categories '''
		''' Clear out destination '''
		''' Get list '''
		''' For each in list '''
		''' Add to destination '''
		
		''' Products '''
		''' Clear out destination '''
		''' Get list '''
		''' For each in list '''
		''' Add to destination '''
		
		''' Product Links '''
		''' Clear out destination '''
		''' Get list '''
		''' For each in list '''
		''' Add to destination '''
		
		''' Product Imagery '''
		''' Clear out destination '''
		''' Get list '''
		''' For each in list '''
		''' Download '''
		''' Upload '''

if __name__ == "__main__":
	src = PyMagento.Magento()
	src.passwd = 'password'
	src.usr = 'remote'
	src.URL = 'http://magento.enterprise.com:10088/magento/index.php/api/xmlrpc/'
	src.connect()
	
	dest = PyMagento.Magento()
	dest.passwd = 'password'
	dest.usr = 'remote'
	dest.URL = 'http://magento.enterprise.com:10088/magento/index.php/api/xmlrpc/'
	dest.connect()
	MM = Mage_Migrate()
	MM.Migrate(src, dest)