# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib import unquote
import requests


class PartnerApi:

    def __init__(self, base_url, user_name, password):
        """

        :param base_url: the api endpoint
        :param user_name: the username for authentication
        :param password: the password for authentication
        """
        self.base_url = base_url
        self.username = user_name
        self.password = password

    def retrieve_fee_details(self, request_id, uri, service_params):
        """
        method to retreive student details for the third-party billing system
        :param request_id: a transaction refid for this request
        :param uri: the path the specific api endpoint
        :param service_params: the request parameters
        :return: result : student details
        """
        result = {}
        url = self.base_url + uri

        # add the necessary request params
        service_params['request_id'] = request_id
        service_params['public_key'] = self.username
        service_params['private_key'] = self.password
        fee_type, fee_type_name, entity_type, req_type = unquote(service_params['fee_type']).split(',')
        service_params['fee_type'] = fee_type
        service_params['student_no'] = unquote(service_params['student_no'])
        headers = {}

        # make request to the url endpoint
        resp = requests.post(url, data=service_params, headers=headers, verify=True)

        result['http_status'] = resp.status_code
        result['http_status_desc'] = resp.reason
        if resp.status_code == 200:
            data = resp.json()
            result['data'] = data

        return result

    def submit_payment(self, request_id, uri, service_params):
        """
        method to send payment details to api endpoint
        :param request_id: a transaction refid for this request
        :param uri: the path the specific api endpoint
        :param service_params: the request parameters
        :return: result : student details
        :return:
        """
        result = {}
        url = self.base_url + uri
        service_params['public_key'] = self.username
        service_params['private_key'] = self.password
        service_params['request_id'] = request_id
        fee_type, fee_type_name, entity_type, req_type = unquote(service_params['fee_type']).split(',')
        service_params['trans_date'] = service_params['trans_date'].replace('-', '')
        if req_type == '2':
            service_params['fee_type'] = fee_type
            service_params['student_no'] = unquote(service_params['student_no'])
            service_params.pop('contact', '')
            service_params["req_type"] = "2"
            service_params.pop('name', '')
        elif req_type == '4':
            service_params['prefix'] = 'ADB'
            service_params['mode'] = entity_type.upper()
            service_params['req_type'] = "4"
            service_params.pop('student_no', '')
            service_params.pop('fee_type', '')

        # send request
        resp = requests.post(url, data=service_params, verify=True)

        result['http_status'] = resp.status_code
        result['http_status_desc'] = resp.reason
        if resp.status_code == 200:  # check if request was successful
            data = resp.json()
            result['data'] = data
        else:

            try:
                content = resp.json()
                err_desc = content['MessageDetail']
                result['err_desc'] = err_desc
            except Exception as ex:
                result['err_desc'] = err_desc
        return result
