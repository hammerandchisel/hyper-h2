# -*- coding: utf-8 -*-
"""
h2/config
~~~~~~~~~

Objects for controlling the configuration of the HTTP/2 stack.
"""


class _BooleanConfigOption(object):
    """
    Descriptor for handling a boolean config option.  This will block
    attempts to set boolean config options to non-bools.
    """
    def __init__(self, name):
        self.name = name
        self.attr_name = '_%s' % self.name

    def __get__(self, instance, owner):
        return getattr(instance, self.attr_name)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise ValueError("%s must be a bool" % self.name)
        setattr(instance, self.attr_name, value)


class H2Configuration(object):
    """
    An object that controls the way a single HTTP/2 connection behaves.

    This object allows the users to customize behaviour. In particular, it
    allows users to enable or disable optional features, or to otherwise handle
    various unusual behaviours.

    This object has very little behaviour of its own: it mostly just ensures
    that configuration is self-consistent.

    :param client_side: Whether this object is to be used on the client side of
        a connection, or on the server side. Affects the logic used by the
        state machine, the default settings values, the allowable stream IDs,
        and several other properties. Defaults to ``True``.
    :type client_side: ``bool``

    :param header_encoding: Controls whether the headers emitted by this object
        in events are transparently decoded to ``unicode`` strings, and what
        encoding is used to do that decoding. For historical reasons, this
        defaults to ``'utf-8'``. To prevent the decoding of headers (that is,
        to force them to be returned as bytestrings), this can be set to
        ``False`` or the empty string.
    :type header_encoding: ``str``, ``False``, or ``None``

    :param validate_outbound_headers: Controls whether the headers emitted
        by this object are validated against the rules in RFC 7540.
        Disabling this setting will cause outbound header validation to
        be skipped, and allow the object to emit headers that may be illegal
        according to RFC 7540. Defaults to ``True``.
    :type validate_outbound_headers: ``bool``

    :param normalize_outbound_headers: Controls whether the headers emitted
        by this object are normalized before sending.  Disabling this setting
        will cause outbound header normalization to be skipped, and allow
        the object to emit headers that may be illegal according to
        RFC 7540. Defaults to ``True``.
    :type normalize_outbound_headers: ``bool``

    :param validate_inbound_headers: Controls whether the headers received
        by this object are validated against the rules in RFC 7540.
        Disabling this setting will cause inbound header validation to
        be skipped, and allow the object to receive headers that may be illegal
        according to RFC 7540. Defaults to ``True``.
    :type validate_inbound_headers: ``bool``
    """
    client_side = _BooleanConfigOption('client_side')
    validate_outbound_headers = _BooleanConfigOption(
        'validate_outbound_headers'
    )
    normalize_outbound_headers = _BooleanConfigOption(
        'normalize_outbound_headers'
    )
    validate_inbound_headers = _BooleanConfigOption(
        'validate_inbound_headers'
    )

    def __init__(self,
                 client_side=True,
                 header_encoding='utf-8',
                 validate_outbound_headers=True,
                 normalize_outbound_headers=True,
                 validate_inbound_headers=True):
        self.client_side = client_side
        self.header_encoding = header_encoding
        self.validate_outbound_headers = validate_outbound_headers
        self.normalize_outbound_headers = normalize_outbound_headers
        self.validate_inbound_headers = validate_inbound_headers

    @property
    def header_encoding(self):
        """
        Controls whether the headers emitted by this object in events are
        transparently decoded to ``unicode`` strings, and what encoding is used
        to do that decoding. For historical reasons, this defaults to
        ``'utf-8'``. To prevent the decoding of headers (that is, to force them
        to be returned as bytestrings), this can be set to ``False`` or the
        empty string.
        """
        return self._header_encoding

    @header_encoding.setter
    def header_encoding(self, value):
        """
        Enforces constraints on the value of header encoding.
        """
        if not isinstance(value, (bool, str, type(None))):
            raise ValueError("header_encoding must be bool, string, or None")
        if value is True:
            raise ValueError("header_encoding cannot be True")
        self._header_encoding = value
