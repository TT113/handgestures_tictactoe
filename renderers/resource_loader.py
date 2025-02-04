import sys
import os
import pygame
from os import chdir

default_layout_params = {
    'board_asset_name': 'field.png',
    'nought_asset_name': 'nought.png',
    'cross_asset_name': 'cross.png',
    'cursor_invalid_asset_name': 'cursor_invalid.png',
    'cursor_valid_asset_name': 'cursor.png',
    'frame_asset_name': 'frame.png',

    'palm_hint_asset_name': 'palm_hint.png',
    'gaming_hint_asset_name': 'gaming_hint.png',
    'calibration_hint_asset_name': 'calibration_hint.png',
    'crosses_wins_asset_name': 'crosses_wins.png',
    'noughts_wins_asset_name': 'nougts_wins.png',
    'start_hint_asset_name': 'start_hint.png',
    'font_type': 'lucidagrande.ttf'
}


default_layout_params_nn = {
    'board_asset_name': 'field.png',
    'nought_asset_name': 'nought.png',
    'cross_asset_name': 'cross.png',
    'cursor_invalid_asset_name': 'cursor_invalid.png',
    'cursor_valid_asset_name': 'cursor.png',
    'frame_asset_name': 'frame.png',
    'calibration_hint_asset_name': 'calibration_hint.png',
    'palm_hint_asset_name': 'palm_hint.png',
    'gaming_hint_asset_name': 'gaming_hint_nn.png',
    'crosses_wins_asset_name': 'crosses_wins.png',
    'noughts_wins_asset_name': 'nougts_wins.png',
    'start_hint_asset_name': 'start_hint.png',
    'font_type': 'lucidagrande.ttf'
}


class ResourceLoader:
    @staticmethod
    def with_default_params():
        return ResourceLoader(default_layout_params)

    @staticmethod
    def with_nn_params():
        return ResourceLoader(default_layout_params_nn)

    def __init__(self, layout_params):
        self.layout_params = layout_params
        self.cached_resources = {}

    @staticmethod
    def get_path_for_asset( name):
        """ support for pyinstaller """
        if hasattr(sys, '_MEIPASS'):
            chdir(sys._MEIPASS)
        elif '_MEIPASS2' in os.environ:
            chdir(os.environ['_MEIPASS2'])
        else:
            pass
        current_path = os.getcwd()
        resource_path = os.path.join(current_path, 'resources')
        image_path = os.path.join(resource_path, name)
        return image_path

    def get_font(self):
        path = self.get_path_for_asset(self.layout_params['font_type'])
        return pygame.font.Font(path, 32)

    def __get_scaled_asset(self, asset_name, size, cached_name=None):
        name_for_cache = asset_name
        if cached_name is not None:
            name_for_cache = cached_name
        if name_for_cache in self.cached_resources:
            return self.cached_resources[name_for_cache]

        asset = pygame.image.load(self.get_path_for_asset(asset_name))
        if size is not None:
            asset = pygame.transform.scale(asset, (int(size[0]), int(size[1])))
        self.cached_resources[name_for_cache] = asset
        return asset

    def get_generic_asset(self, name):
        asset = self.__get_scaled_asset(name, None)
        return asset

    def get_field_asset(self, length):
        asset_name = self.layout_params['board_asset_name']
        return self.__get_scaled_asset(asset_name, (length, length), asset_name + str(length))

    def get_nought_asset(self, length):
        asset_name = self.layout_params['nought_asset_name']
        return self.__get_scaled_asset(asset_name, (length,length), asset_name + str(length))

    def get_cross_asset(self, length):
        asset_name = self.layout_params['cross_asset_name']
        return self.__get_scaled_asset(asset_name, (length,length), asset_name + str(length))

    def get_cursor_asset(self, valid_move, length):
        if valid_move:
            asset_name = self.layout_params['cursor_valid_asset_name']
        else:
            asset_name = self.layout_params['cursor_invalid_asset_name']
        return self.__get_scaled_asset(asset_name, (length, length), asset_name + str(length))

    def get_frame_asset(self, length):
        name = self.layout_params['frame_asset_name']
        return self.__get_scaled_asset(name, (length, length), name + str(length))

    def get_start_hint_asset(self):
        return self.__get_scaled_asset(self.layout_params['start_hint_asset_name'], None)

    def get_in_game_bottom_hint(self):
        return self.__get_scaled_asset(self.layout_params['gaming_hint_asset_name'], None)

    def get_calibration_bottom_hint(self):
        return self.__get_scaled_asset(self.layout_params['calibration_hint_asset_name'], None)
