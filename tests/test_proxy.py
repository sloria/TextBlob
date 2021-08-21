# -*- coding: utf-8 -*-
import time
import json
import unittest
import urllib.request
from nose.tools import *  # PEP8 asserts

from textblob.proxy import set_proxy


class TestProxy(unittest.TestCase):
    def test_proxy(self):
        proxy_service_url = "http://localhost:8118"
        ip_get_url = "http://ip-api.com/json/"
        set_proxy(proxy_service_url)
        collected_ip_addresses = []
        for x in range(5):
            with urllib.request.urlopen(ip_get_url) as url:
                json_data = json.loads(url.read().decode("utf-8"))
                print("IP address:", json_data["query"])
                ip_changed = (
                    True if json_data["query"] not in collected_ip_addresses else False
                )
                self.assertTrue(ip_changed, "IP not changed.")
                collected_ip_addresses.append(json_data["query"])
                time.sleep(2)


if __name__ == "__main__":
    unittest.main()
