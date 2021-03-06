import os
import requests
import simplejson as json
import settings
from errors import raise_for_view_error

DOCUMENTS_RESOURCE = '/documents'
SESSIONS_RESOURCE = '/sessions'
VIEW_RESOURCE = '/view'

PROCESSING = 'processing'
DONE = 'done'


class BoxViewClient(object):
    """A simple wrapper around the Box View API

    Args:
        api_token: A valid box view api token, get one here: bit.ly/boxapikey

    Attributes:

    """

    def __init__(self, api_token):

        if api_token is None:
            raise ValueError("api_token is none")

        auth_header = {'Authorization': 'Token {}'.format(api_token)}

        self.requests = requests.session()
        self.requests.headers = auth_header
        self.url = settings.BOXVIEW_VIEW_API_URL
        self.upload_url = settings.BOXVIEW_UPLOAD_VIEW_API_URL

    # Core API Methods

    @raise_for_view_error
    def upload_document(self, url):
        """
        """

        resource = '{}{}'.format(self.url, DOCUMENTS_RESOURCE)
        headers = {'Content-type': 'application/json'}
        data = json.dumps({'url': url})

        response = self.requests.post(resource, headers=headers, data=data)

        return response

    @raise_for_view_error
    def multipart_upload_document(self, document):
        """
        """

        resource = '{}{}'.format(self.upload_url, DOCUMENTS_RESOURCE)
        files = {'file': document}

        response = self.requests.post(resource, files=files)

        return response

    @raise_for_view_error
    def get_document(self, document_id):
        """
        """

        resource = '{}{}/{}'.format(
            self.url,
            DOCUMENTS_RESOURCE,
            document_id
        )

        response = self.requests.get(resource)

        return response

    def delete_document(self, document_id):
        resource = '{}{}/{}'.format(self.url, DOCUMENTS_RESOURCE, document_id)
        response = self.requests.delete(resource)
        return response

    @raise_for_view_error
    def create_session(self, document_id, expires_at='4013-12-23T05:21:09.697Z'):
        """
        """

        resource = '{}{}'.format(self.url, SESSIONS_RESOURCE)
        headers = {'Content-type': 'application/json'}
        data = {'document_id': document_id}
        if expires_at:
            data['expires_at'] = expires_at
        data = json.dumps(data)

        response = self.requests.post(resource, headers=headers, data=data)

        return response

    # Convenience Methods

    def ready_to_view(self, document_id):
        """
        """

        document_status = self.get_document_status(document_id)

        return document_status == DONE

    def get_document_status(self, document_id):
        """
        """

        document = self.get_document(document_id).json()

        return document['status']

    @staticmethod
    def create_session_url(session_id, theme=None):
        """
        """
        return '{}{}/{}/assets'.format(
            settings.BOXVIEW_VIEW_API_URL,
            SESSIONS_RESOURCE,
            session_id
        )

boxview_client = BoxViewClient(settings.BOXVIEW_TOKEN)
