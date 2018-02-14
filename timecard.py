#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Author: aaron@junctionapps.ca
# Project: 3e-timecard

# Copyright 2018 Junction Applications Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import pytz
from datetime import datetime
from requests import Session
from requests_ntlm import HttpNtlmAuth
import xml.etree.ElementTree as ET
from zeep import Client
from zeep.transports import Transport


def attribute(key, value, alias_field=None):
    """ Builds a single attribute node, handling the AliasField attribute if passed in"""
    a = ' AliasField="{af}"'.format(af=alias_field) if alias_field else ''
    return '<{n}{af}>{v}</{n}>'.format(n=key, af=a, v=value) if value is not None else '<{} />'.format(key)


def build_attributes(*args, **kwargs):
    """ Takes a tuple of tuples containing the defaults as arg0,
     order is (key, AliasField, default value)
     and a dictionary of passed in values for this particular build.
     Builds the attributes list appropriately."""
    attr_defaults = args[0]

    axml = []
    for a in attr_defaults:
        axml.append('{}'.format(attribute(a[0],                     # node name
                                          kwargs.get(a[0], a[2]),   # passed in value or default
                                          a[1])))                   # alias field

    return '\n     '.join([' <Attributes>',
                           '\n     '.join(a for a in axml),
                           '</Attributes>'])


def timecard_add_xml(**kwargs):
    """ Returns a value add portion for a process_xml for time cards
    build_attributes will only loop through those we pass in via attribute_defaults, ignoring any
    extra cruft that comes in from **kwargs.
    """
    # todo: should read these from the xsd, however would still want to set the defaults for our use case
    # likely \Inetpub\XML\Object\Schema\Write\TimeCard.xsd
    # see: http://docs.python-zeep.org/en/master/internals_xsd.html

    # Field, AliasField, default
    attribute_defaults = (
        ('OrigTimeIndex', None, None),
        ('IsActive', None, 1),
        ('Office', None, None),
        ('WorkDate', None, None),
        ('PostDate', None, None),
        ('Currency', None, None),
        ('CurrDate', None, None),
        ('Matter', 'Number', None),
        ('BillMatter', 'Number', None),
        ('Timekeeper', 'Number', None),
        ('WorkMattEffDate', None, None),
        ('BillMattEffDate', None, None),
        ('TkprEffDate', None, None),
        ('IsNB', None, 0),
        ('ResPct', None, None),
        ('IsNoCharge', None, 0),
        ('StartTime', None, None),
        ('TimeInterval', None, None),
        ('EntryUnitType', None, None),
        ('EntryUnit', None, None),
        ('WorkHrs', None, None),
        ('WorkRate', None, None),
        ('WorkAmt', None, None),
        ('ChrgCard', None, None),
        ('OrigHrs', None, None),
        ('OrigRate', None, None),
        ('OrigAmt', None, None),
        ('StdCurrency', None, None),
        ('StdRate', None, None),
        ('StdAmt', None, None),
        ('Language', None, None),
        ('Narrative', None, None),
        ('TimeType', None, None),
        ('TransactionType', None, 'FEES'),
        ('TaxJurisdiction', None, None),
        ('Phase', None, None),
        ('Task', None, None),
        ('Activity', None, None),
        ('TaxCode', None, None),
        ('EditTranType', None, None),
        ('ReasonType', None, None),
        ('ProfMaster', None, None),
        ('InvMaster', None, None),
        ('Voucher', None, None),
        ('OrigCurrency', None, None),
        ('WorkType', None, 0),      # default
        ('InputTaxCode', None, None),
        ('PurgeType', None, None),
        ('WIPRemoveDate', None, None),
        ('RefCurrency', None, None),
        ('RefRate', None, None),
        ('RefAmt', None, None),
        ('ReversingCardIdx', None, None),
        ('ModifiedCardIdx', None, None),
        ('RateCalcList', None, None),
        ('WIPHrs', None, None),
        ('WIPRate', None, None),
        ('WIPAmt', None, None),
        ('IsDisplay', None, 1),
        ('LoadNumber', None, None),
        ('LoadSource', None, 'Python Load Demo'),
        ('LoadGroup', None, 'Python'),
        ('Disposition', None, None),
        ('InternalComments', None, None),
        ('GLDate', None, None),
        ('UnitCurrRate', None, None),
        ('FirmCurrRate', None, None),
        ('UnitCurrRateStd', None, None),
        ('FirmCurrRateStd', None, None),
        ('AuthTimekeeper', None, None),
        ('SpvTimekeeper', None, None),
        ('IsFlatFeeComplete', None, 0),
        ('ParTimeIndex', None, None),
        ('UpdateList', None, None),
        ('TimePracticeArea', None, None),
        ('MatrixTaxCode', None, None),
        ('Rpt1CurrRate', None, None),
        ('Rpt2CurrRate', None, None),
        ('Rpt3CurrRate', None, None),
        ('Rpt1CurrRateStd', None, None),
        ('Rpt2CurrRateStd', None, None),
        ('Rpt3CurrRateStd', None, None),
        ('IsTaxAdvice', None, 0),
        ('IsSelected', None, 1),
        ('IsReqChangeInfo', None, 0),
        ('LockTimekeeper', None, None),
        ('LockWorkDate', None, None),
        ('PrevProfMaster', None, None),
        ('IsSplitted', None, 0),
        ('IsExcluded', None, 0),
        ('Notes', None, None),
        ('IsTimer', None, 0),
    )

    prefix = '  <Add>\n    <TimeCard>'
    suffix = '</TimeCard>\n  </Add>'

    return '\n    '.join([
                      prefix,
                      build_attributes(attribute_defaults, **kwargs),
                      suffix
                     ])


def timecards_xml(*args):
    """ builds a timecard process xml using custom process C_TimeCardUpdate_srv, however, TimeCardUpdate can be used,
    but we won't get keys back. C_TimeCardUpdate_srv releases and does some other special things for us.
    Contact Dave Roth at oneFG for help with custom processes.
    """

    prefix = '<TimeCardUpdate xmlns="http://elite.com/schemas/transaction/process/write/TimeCardUpdate"><Initialize xmlns="http://elite.com/schemas/transaction/object/write/TimeCard">'
    suffix = '</Initialize></TimeCardUpdate>'

    # prefix = '<C_TimeCardUpdate_srv xmlns="http://elite.com/schemas/transaction/process/write/C_TimeCardUpdate_srv"><Initialize xmlns="http://elite.com/schemas/transaction/object/write/TimeCard">'
    # suffix = '</Initialize></C_TimeCardUpdate_srv>'

    add_xml = '\n'.join(timecard_add_xml(**a) for a in args[0])
    return '\n'.join([prefix, add_xml, suffix])


def parse_xml_reply(xmlreply):
    root = ET.fromstring(xmlreply)
    result = root.attrib.get('Result', 'Failure')  # default to Failure, expect Success as actual result
    if result == 'Success':
        keys = [TimeCard.attrib['KeyValue'] for Keys in root for TimeCard in Keys]
    else:
        keys = None

    message = {
        'result': result,
        'records': root.attrib.get('Records', 0),
        'keys': keys,
        'procid': root.attrib.get('ProcessItemId', ''),
    }
    return message


def create_timecard_process_xml(tc_attributes):
    """ build the process xml to add timecards """
    # create the process xml string for ExecuteProcess
    return timecards_xml(tc_attributes)


def execute_process(client_3e, process_xml):
    """ call ExecuteProcess web service """
    return client_3e.service.ExecuteProcess(processXML=process_xml, returnInfo=1)


def start_3e_client_session():
    """ Establishes the session with Elite 3E. The environment should have the following
    variables set, however, defaults can be set below as the second parameter to get's
    HTTP_NTLM_AUTH_USER
    HTTP_NTLM_AUTH_PASS
    ELITE_WAPI
    ELITE_INSTANCE
    """
    session = Session()
    # note on user: if with domain, for the default escape the slash: mydomain\\myuser.mysurname
    # but in venv use a single slash
    session.auth = HttpNtlmAuth(os.environ.get('HTTP_NTLM_AUTH_USER', ''),
                                os.environ.get('HTTP_NTLM_AUTH_PASS', ''))

    wapi = os.environ.get('ELITE_WAPI', 'elite1')
    instance = os.environ.get('ELITE_INSTANCE', 'TE_3E_UAT')

    wsdl = "http://{w}/{i}/WebUI/Transactionservice.asmx?wsdl".format(w=wapi, i=instance)

    client_3e = Client(wsdl, transport=Transport(session=session))
    return client_3e


def timecard_attributes():
    """ This would be read from the application's datastore, perhaps even looping over a number of small
    time entries, and summing by timekeeper/date for a single entry in 3E.
    For this demo we'll set it up manually here."""

    # Visit Halifax http://www.novascotia.com/about-nova-scotia/regions/halifax-metro
    # See http://pytz.sourceforge.net/#helpers
    tz = pytz.timezone('America/Halifax')

    matter = '136815'
    tkpr_number = '3171'
    work_amount = '500.0'
    wip_amount = '500.0'
    work_hours = '1.0'
    wip_hours = '1.0'
    # server local timezone, with hour, minute, second zeroed out
    # take appropriate steps to get timekeeper's timezone as needed
    work_date = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    narrative = 'Demonstrated time card creation with Python and Zeep'

    timecard = {'Matter': matter,
                'Timekeeper': tkpr_number,
                'WorkAmt': work_amount,
                'WIPAmt': wip_amount,
                'WorkHrs': work_hours,
                'WIPHrs': wip_hours,
                'WorkDate': work_date,
                'RateCalcList': 'OVR',
                'Narrative': narrative,
                }
    # multiple cards are supported, so we'll be sure to indicate this is iterable
    return (timecard, )


def main():
    tc_attributes = timecard_attributes()
    print('Time card details:')
    print(tc_attributes)

    process_xml = create_timecard_process_xml(tc_attributes)
    print('Process XML to Send to ExecuteProcess webservice')
    print(process_xml)

    print('Call the Web Service')
    client_3e = start_3e_client_session()
    xml_reply = execute_process(client_3e, process_xml)
    print(xml_reply)

    print('Parse the results')
    print(parse_xml_reply(xml_reply))


if __name__ == '__main__':
    main()
