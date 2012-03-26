from datetime import datetime
import functools

from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from askbot.skins.loaders import render_into_skin
from askbot.views.users import owner_or_moderator_required

from privatebeta.forms import InviteRequestForm, InviteApprovalForm
from privatebeta.models import InviteRequest

def owner_or_moderator_required(f):
    @functools.wraps(f)
    def wrapped_func(request, *args, **kwargs):
        if request.user.is_authenticated() and (request.user.is_moderator() or request.user.is_superuser):
            pass
        else:
            params = '?next=%s' % request.path
            return HttpResponseRedirect(reverse('user_signin') + params)
        return f(request, *args, **kwargs)
    return wrapped_func

def invite(request, form_class=InviteRequestForm,
        template_name="privatebeta/invite.html",
        extra_context=None):
    """
    Allow a user to request an invite at a later date by entering their email address.

    **Arguments:**

    ``template_name``
        The name of the tempalte to render.  Optional, defaults to
        privatebeta/invite.html.

    ``extra_context``
        A dictionary to add to the context of the view.  Keys will become
        variable names and values will be accessible via those variables.
        Optional.

    **Context:**

    The context will contain an ``InviteRequestForm`` that represents a
    :model:`invitemelater.InviteRequest` accessible via the variable ``form``.
    If ``extra_context`` is provided, those variables will also be accessible.

    **Template:**

    :template:`privatebeta/invite.html` or the template name specified by
    ``template_name``.
    """
    form = form_class(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('privatebeta_sent'))

    context = {'form': form}

    if extra_context is not None:
        context.update(extra_context)

    return render_into_skin(template_name, context, request)

def sent(request, template_name="privatebeta/sent.html", extra_context={}):
    """
    Display a message to the user after the invite request is completed
    successfully.

    **Arguments:**

    ``template_name``
        The name of the tempalte to render.  Optional, defaults to
        privatebeta/sent.html.

    ``extra_context``
        A dictionary to add to the context of the view.  Keys will become
        variable names and values will be accessible via those variables.
        Optional.

    **Context:**

    There will be nothing in the context unless a dictionary is passed to
    ``extra_context``.

    **Template:**

    :template:`privatebeta/sent.html` or the template name specified by
    ``template_name``.
    """
    return render_into_skin(template_name, extra_context, request)

def activate_invite(request, code,
                    template_name='privatebeta/activate_invite.html',
                    redirect_to=None):
    '''Activates a invitation from email'''
    invite_request = get_object_or_404(InviteRequest,
            invitation_code=code, used_invitation = False)

    #checkout if the invite was expired
    time_diff = datetime.today() - invite_request.invited_date
    #if PRIVATEBETA_EXPIRE_DAYS is 0 invites can't be expired
    if time_diff.days > askbot_settings.PRIVATEBETA_INVITE_DURATION and \
            settings.PRIVATEBETA_EXPIRE_DAYS > 0:
        return render_into_skin('privatebeta/expired_invite.html',
                                  {'invite': invite_request}, request
                                 )

    #set session variable to be able to bypass the middleware
    request.session['invite_code'] = code

    if redirect_to:
        return redirect(redirect_to)
    else:
        context = {}
        return render_into_skin(template_name, context, request)


def resend_invite(request, form_class=InviteRequestForm,
        template_name="privatebeta/invite.html", extra_context=None):
    '''Resend invite callback the same as invite but deletes a previous invite if already exists'''
    form = form_class(request.POST or None)
    if request.method=="POST":
        email = request.POST['email']
        invite = get_object_or_404(InviteRequest, email=email)
        invite.delete()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('privatebeta_sent'))

        context = {'form': form}

        if extra_context is not None:
            context.update(extra_context)

        return render_into_skin(template_name, context, request)
    else:
        return redirect(settings.ASKBOT_URL)

@owner_or_moderator_required
def invite_list(request):
    '''displays a list of invites and the option of inviting people'''

    if request.method == 'POST':
        form = InviteApprovalForm(None, data=request.POST)
        if form.is_valid():
            cleaned_data = dict.copy(form.fields)
            del cleaned_data['select_all']
            for field in cleaned_data.values():
                field.invite.send_invite()
        else:
            context = {'form': form}
            return render_into_skin('privatebeta/invite_list.html', context, request)
        invites = InviteRequest.objects.filter(invited=False)
        form = InviteApprovalForm(invites)
    else:
        invites = InviteRequest.objects.filter(invited=False)
        form = InviteApprovalForm(invites)

    context = {'form': form, 'invite_form': InviteRequestForm()}
    return render_into_skin('privatebeta/invite_list.html', context, request)

@owner_or_moderator_required
def invite_user(request):
    '''called from invite/list'''
    if request.method == "POST":
        form = InviteRequestForm(request.POST)
        if form.is_valid():
            invite = form.save()
            invite.send_invite()
            request.user.message_set.create(message='Invite sent to: %s' % invite.email)
            return redirect(reverse('privatebeta_invite_list'))
    else:
        return HttpResponseForbiden()
