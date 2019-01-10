from pyotp import TOTP
from workflow.notify import notify


def list_tokens(keychain, wf):
    for service, secret_key in keychain.iteritems():
        token = TOTP(secret_key).now()
        _add_workflow_item(wf, service, token)

    wf.send_feedback()


def add_new_service(keychain, wf, service, secret_key):
    wf.logger.debug("secret_key = %s", secret_key)
    try:
        TOTP(secret_key).now()
    except TypeError as e:
        error_msg = u"Error adding %s: %s" % (service, e.message)
        wf.logger.error(error_msg)
        notify(u"Error adding %s" % service, e.message)
        raise

    if service in keychain:
        error_msg = u"Duplicate service name: %s" % service
        wf.logger.error(error_msg)
        notify("Error adding %s" % service, error_msg)
        raise ValueError(error_msg)

    keychain[service] = secret_key
    keychain.save()
    wf.logger.info(u"Added %s", service)


def _add_workflow_item(wf, service, token):
    wf.add_item(
        title=service,
        subtitle=token,
        valid=True,
        arg=token,
        copytext=token,
        largetext=token,
    )
