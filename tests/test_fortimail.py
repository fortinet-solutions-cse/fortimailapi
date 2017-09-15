#!/usr/bin/python
import pytest
import logging
import fortimailapi
from packaging.version import Version

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("fortimailapi")


@pytest.fixture
def session(request):

    session = fortimailapi.FortiMailAPI()
    session.debug("on")
    session.https("off")
    res = session.login("192.168.122.12","admin","")
    log.info(res)
    return session

def test_license(session):

    res = session.license()
    log.info(res)


def test_version(session):
    ver = session.get_version()
    if Version(ver) > Version('5.3'):
        log.info("Version is later than 5.3")
        pass
    else:
        log.error ("Version is older than 5.3")
        assert False, "Version is older than 5.3: "+ver

def test_get_empty_domain(session):

    #Remove, just in case it comes from older execution
    res = session.delete("","dsa.com")
    log.info(res)

    res = session.get("", "dsa.com")
    if not (res["errorType"] == 3):
        log.info(res)
        assert False, "Domain dsa.com is not empty, even after deleting"

def test_create_new_domain(session):

    data = """{  
    'fallbackport':25,
    'disclaimer_outgoing_header_status':False,
    'hide':False,
    'usessl':False,
    'disclaimer_outgoing_body_status':False,
    'recipient_verification_smtp_cmd':0,
    'other_recipient':False,
    'max_user_quota':1000,
    'is_service_domain':False,
    'migration_status':False,
    'max_mailbox':10,
    'mail_access':7,
    'sender_addr_rate_ctrl_max_spam_state':False,
    'recipient_verification_smtp_accept_reply_string_pattern':'',
    'disclaimer_incoming_header_insertion_name':'',
    'relay_auth_status':False,
    'domain_interval':False,
    'system_domain':1,
    'reqAction':1,
    'sender_addr_rate_notification_state':False,
    'disclaimer_incoming_body_location':0,
    'ldap_group_recipient':False,
    'sender_addr_rate_control_max_megabytes':100,
    'ldap_asav_state':False,
    'disclaimer_outgoing_body_location':0,
    'is_subdomain':False,
    'disclaimer_outgoing_header_insertion_name':'',
    'original':False,
    'sender_addr_rate_ctrl_max_spam':5,
    'disclaimer_outgoing_header_insertion_value':'',
    'relay_ip_pool_port':25,
    'relay_ip_pool_ssl':False,
    'sender_addr_rate_ctrl_max_recipients':60,
    'recipient_verification':0,
    'relay_auth_username':'',
    'other_address':'',
    'disclaimer_incoming_header_insertion_value':'',
    'disclaimer_incoming_body_content':'',
    'disclaimer_incoming_body_content_html':'',
    'fallbackhost':'fhtrtt.vom',
    'rcptvrfy_try_mhost':False,
    'relay_auth_type':0,
    'sender_addr_rate_ctrl_exempt':[  

    ],
    'sender_addr_rate_ctrl_max_recipients_state':False,
    'ldap_generic_routing_ssl':False,
    'hours':0,
    'port':25,
    'objectID':'DomainSetting:{D:dsa.com}',
    'sender_addr_rate_control_max_megabytes_state':False,
    'recipient_verification_background':0,
    'relay_auth_password':'******',
    'group_recipient_only':False,
    'max_msg_size':204800,
    'alt_smtp_ena':False,
    'ip':'mysmtp',
    'bypass_bounce_verification':False,
    'ldap_routing_state':False,
    'sender_addr_rate_ctrl_action':512,
    'alternative_domain_name':'',
    'maindomain':'dsa.com',
    'ldap_generic_routing_port':25,
    'addressbook_add_option':2,
    'disclaimer_outgoing_body_content':'',
    'alt_smtp_ssl':False,
    'disclaimer_incoming_header_status':False,
    'remove_outgoing_header':False,
    'sender_addr_rate_control_state':False,
    'mdomain':'dsa.com',
    'sender_addr_rate_control_max_messages_state':True,
    'sender_addr_rate_control_max_messages':30,
    'alt_smtp_port':25,
    'report_template_name':'default',
    'global_bayesian':True,
    'fallbackusessl':False,
    'days':0,
    'disclaimer_status':1,
    'disclaimer_incoming_body_status':False,
    'mxflag':0,
    'ip_pool_direction':1,
    'default_language':'',
    'other_greeting':'',
    'alt_smtp_host':'',
    'domain_recipient':True,
    'ldap_service_status':True,
    'default_theme':8,
    'webmail_service_type':0,
    'disclaimer_outgoing_body_content_html':'',
    'group_exclude_individual':False,
    'domain_report':False
     }"""

    res = session.post("", "dsa.com", data)
    if not (res["mdomain"] == "dsa.com" and
                    res["objectID"] == "DomainSetting:{D:dsa.com}"):
        log.info(res)
        assert 0, "Domain dsa.com was not created correctly"

def test_get_domain(session):

    res = session.get("", "dsa.com")
    if not (res["mdomain"] == "dsa.com" and
                    res["objectID"] == "DomainSetting:{D:dsa.com}"):
        log.info(res)
        assert 0, "Domain dsa.com was not created correctly"

def test_change_attribute_in_domain(session):

    payload = """{    
    "objectID": \"DomainSetting:{D:dsa.com}",
    "mdomain": "dsa.com",
    "max_msg_size": 10800}"""

    res = session.put("", "dsa.com", payload)
    if res["max_msg_size"] != 10800:
        log.info(res)
        assert 0, "Max_msg_size was not changed after put operation:" +\
                  res["max_msg_size"]


    res = session.get("", "dsa.com")
    if res["max_msg_size"] != 10800:
        log.info(res)
        assert 0, "Max_msg_size was not changed after put & get operation:"+\
                  res["max_msg_size"]

def test_delete_domain(session):


    res = session.delete("","dsa.com")
    if res["errorType"] != 0:
        log.info(res)
        assert False, "Domain dsa.com can not be removed"

    res = session.get("", "dsa.com")
    if res["errorType"] == 0:
        log.info(res)
        assert False, "Domain dsa.com can not be removed"




