#!/usr/bin/python
# encoding: utf-8

import argparse
import sys

from authenticator import add_new_service, list_tokens
from keychain import AuthKeys
from workflow import Workflow3


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--add',
        dest='service',
        nargs=2,
        metavar=('service', 'secret_key'),
    )
    args = parser.parse_args(args)
    return args


def main(wf):
    wf.logger.debug(wf.args)
    args = parse_args(wf.args)
    keychain = AuthKeys(wf)

    if args.service:
        service, secret_key = args.service
        wf.logger.debug("service = %s; secret_key = %s" % (service, secret_key))
        service = service.strip()
        secret_key = secret_key.strip().replace(' ', '')

        add_new_service(keychain, wf, service, secret_key)
        return 0

    list_tokens(keychain, wf)
    return 0


if __name__ == '__main__':
    workflow = Workflow3()
    sys.exit(workflow.run(main))
