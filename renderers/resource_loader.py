import cv.constants as constants
import os
import pygame

default_layout_params = {
    'board_length_px': 300,
    'nought_cross_size_px' : 60,
    'board_asset_name': 'field.png',
    'nought_asset_name': 'nought.png',
    'cross_asset_name': 'cross.png',
    'cursor_invalid_asset_name': 'cursor_invalid.png',
    'cursor_valid_asset_name': 'cursor.png',
    'cursor_size_px': 150
}


class ResourceLoader:

    @staticmethod
    def with_default_params():
        return ResourceLoader(default_layout_params)

    def __init__(self, layout_params):
        self.layout_params = layout_params
        self.cached_resources = {}

    def __get_path_for_asset(self, name):
        current_path = os.getcwd()  # Where your .py file is located
        resource_path = os.path.join(current_path, 'resources')  # The resource folder path
        image_path = os.path.join(resource_path, name)
        return image_path

    def __get_scaled_asset(self, asset_name, size):
        if asset_name in self.cached_resources:
            return self.cached_resources[asset_name]

        asset = pygame.image.load(self.__get_path_for_asset(asset_name))
        asset = pygame.transform.scale(asset, size)
        self.cached_resources[asset_name] = asset
        return asset


    def get_field_asset(self):
        asset_name = self.layout_params['board_asset_name']
        board_length = self.layout_params['board_length_px']
        return self.__get_scaled_asset(asset_name, (board_length, board_length))

    def get_nought_asset(self):
        asset_name = self.layout_params['nought_asset_name']
        length = self.layout_params['nought_cross_size_px']
        return self.__get_scaled_asset(asset_name, (length,length))

    def get_cross_asset(self):
        asset_name = self.layout_params['cross_asset_name']
        length = self.layout_params['nought_cross_size_px']
        return self.__get_scaled_asset(asset_name, (length,length))

    def get_cursor_asset(self, valid_move):
        if valid_move:
            asset_name = self.layout_params['cursor_valid_asset_name']
        else:
            asset_name = self.layout_params['cursor_invalid_asset_name']
        length = self.layout_params['cursor_size_px']
        return self.__get_scaled_asset(asset_name, (length, length))

