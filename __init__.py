from netaddr import IPNetwork
from geolite2 import geolite2
import json

import logging

logger = logging.getLogger(__name__)


class IPLookup:
    def __init__(self):
        self.reader = geolite2.reader()

        # Create a few hardcoded strings which will be used multiple times thorough the code as instance attributes.
        # This is done so that if the values change its not a pain to find them through the code and update them.
        # Not always the most necessary but a good practice non the less.
        self.override_sections = ['city', 'continent', 'country', 'location', 'registered_country', 'subdivisions']
        self.names_text = 'names'
        self.lang = 'en'

    def _override_names(self, lookup_result):
        """
        Checks previously defined sections of the nested dict structure for a names field and overrides it with just
        the english name if it can find one.
        """

        for section in self.override_sections:
            # If the section exists as a key and has a names key underneath, update the dict with just english name.
            if lookup_result[section] and isinstance(lookup_result[section], dict):
                if self.names_text in lookup_result[section].keys():
                    try:
                        lookup_result[section].update({'name': lookup_result[section][self.names_text][self.lang]})
                    except KeyError:
                        # Catches the potential key error if the en key doesnt exist and updates the dict to have an
                        # empty name value
                        lookup_result[section].update({'name': 'No English name found.'})
                        # Removes old names key from dict.
                    lookup_result[section].pop(self.names_text, None)

        return lookup_result

    def get_ip(self, ip, with_json=False):
        """
        Lookup an IP in the maxminddb and return a dict (or json) with its result.

        :param ip: IP to lookup in maxminddb
        :type: ip: `str`
        :param with_json: Enable json output when running.
        :type with_json: `bool`
        :return: A dictionary(hash) with helpful information on the IP.
        :rtype: `dict`
        """

        initial_output = self.reader.get(ip)
        # Attempt to mutate the output with private method. Dont fail if it doesnt succeed though.
        # noinspection PyBroadException
        result = self._override_names(initial_output)

        if with_json:
            return json.dumps(result)
        else:
            return result

    def get_cidr(self, block, with_json=False):
        """
        Lookup a CIDR block and find all IPs in it as well as some info on it, then lookup each IP in the block in the
        maxminddb and return a dict (or json) with its result.

        :param block: The cidr block to lookup
        :type: block: `str`
        :param with_json: Enable json output when running.
        :type with_json: `bool`
        :return: A dictionary(hash) with helpful information on the block, with its IPS.
        :rtype: `dict`
        """

        # Strip any whitespace sent in block string
        block = block.strip()

        block_result = IPNetwork(block)
        # Create our result dict and add a few noteworthy items
        result = {'CIDR Block': str(block_result.cidr), 'Basic Info': str(block_result.info),
                  'Block Length': str(block_result.size)}

        # Iterate over each IP and grab the IPs info and add to our result dict.
        result.update({str(ip): self.get_ip(str(ip)) for ip in block_result})

        if with_json:
            result = json.dumps(result)

        return result
