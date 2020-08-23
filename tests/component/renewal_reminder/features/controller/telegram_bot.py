from urllib.parse import urljoin

from tests.utils.request import make_request, RequestMethod


class TelegramController:

    def __init__(self, base_url: str):
        self._base_url = base_url

    def health(self):
        url = urljoin(self._base_url, 'health')
        return make_request(method=RequestMethod.GET, url=url)

    def requests(self):
        url = urljoin(self._base_url, 'dev/requests')
        return make_request(method=RequestMethod.GET, url=url)

    def clear_requests(self):
        url = urljoin(self._base_url, 'dev/requests/clear')
        return make_request(method=RequestMethod.GET, url=url)

    def last_request(self):
        url = urljoin(self._base_url, 'dev/requests/last')
        return make_request(method=RequestMethod.GET, url=url)
