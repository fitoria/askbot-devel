from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'privatebeta.views.invite', name='privatebeta_invite'),
    url(r'^list/$', 'privatebeta.views.invite_list', name='privatebeta_invite_list'),
    url(r'^invite_user/$', 'privatebeta.views.invite_user', name='privatebeta_invite_user'),
    url(r'^resend/$', 'privatebeta.views.resend_invite', name='privatebeta_resend_invite'),
    url(r'^activate/(?P<code>\w+)/$', 'privatebeta.views.activate_invite',
        {'redirect_to': '/register/'}, name='privatebeta_activate_invite'),
    url(r'^sent/$', 'privatebeta.views.sent', name='privatebeta_sent'),
)
