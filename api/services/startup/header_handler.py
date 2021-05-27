from typing import List, Dict

from django.conf import settings

from . import verification


class HeaderSerializer:
    """VK header serializer"""
    __elements: List[str]

    def __init__(self, header: str):
        if header.startswith('?'):
            header = header[1:]
        self.__elements = header.split('&')

    def serialize(self):
        serialized_header: Dict[str, str] = {}
        for el in self.__elements:
            [key, value] = el.split('=')
            serialized_header[key] = value
        return serialized_header


class HeaderHandler:
    __header: Dict[str, str]
    vk_header: Dict[str, str]

    def __init__(self, header: Dict[str, str]):
        self.__header = header

    def is_headers_valid(self) -> bool:
        if 'HTTP_X_VK_DATA' not in self.__header.keys():
            return False
        self.get_vk_header()
        return True

    def get_vk_header(self):
        serializer: HeaderSerializer = HeaderSerializer(self.__header['HTTP_X_VK_DATA'])
        self.vk_header = serializer.serialize()

    def is_valid(self) -> bool:
        return verification.is_valid(self.vk_header, settings.CLIENT_SECRET_KEY)
