from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from blockchain import views
from blockchain.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^get_chain$', views.get_chain, name="get_chain"),
    url('^mine_block$', views.mine_block, name="mine_block"),
    url('^add_transaction$', views.add_transaction, name="add_transaction"), #New
    url('^is_valid$', views.is_valid, name="is_valid"), #New
    url('^connect_node$', views.connect_node, name="connect_node"), #New
    url('^replace_chain$', views.replace_chain, name="replace_chain"), #New


    ## iqbals urls 
    url('^add_transaction2$', views.add_transaction2, name="add_transaction2"), #New
    url('^validate_blockchain$', views.validate_blockchain, name="validate_blockchain"), #New
    url('^mine_block2$', views.mine_block2, name="mine_block2"), #New
    url('^get_chain2$', views.get_chain, name="get_chain2"),



]