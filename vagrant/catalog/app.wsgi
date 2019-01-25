import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/www/html/catalog')

from catalogMngr import app as application
application.serect_key = 'super_secret_key'
