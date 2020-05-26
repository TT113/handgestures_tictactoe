import os

import pygame

from model.cell_occupation import CellOccupation
import cv.constants as constants
from model.move_result import MoveResult
import time
from model.winner import *


class PyGameRenderer:

    def __init__(self, resource_loader):
        pygame.init()
        self.field_edges_color = (64, 128, 255)

        self.resource_loader = resource_loader

        #defaults params
        self.field_width_cells = 3
        self.field_height_cells = 3

        self.field_side_dimension = 450

        self.field_cell_width = self.field_side_dimension / self.field_width_cells
        self.field_cell_height = self.field_side_dimension / self.field_height_cells

        self.rendered_numbers = {}
        myfont = resource_loader.get_font()
        for i in range(0,10):
            textsurface = myfont.render(str(i), 0, (0, 0, 0))
            self.rendered_numbers[str(i)] = textsurface

        self.camera_frame = None
        self.sc = pygame.display.set_mode((constants.UI_WINDOW_WIDTH, constants.UI_WINDOW_HEIGHT))

        pygame.display.update()

    def setup_with_field(self, state):
        self.field_height_cells = state.size_y
        self.field_width_cells = state.size_x

        self.field_cell_width = self.field_side_dimension / state.size_x
        self.field_cell_height = self.field_side_dimension / state.size_y

    def __field_coordinates(self):
        return (700, constants.UI_WINDOW_HEIGHT/2 - self.field_side_dimension/2 - 50, self.field_side_dimension, self.field_side_dimension)

    def __relative_coordinates(self, rect, coordinates):
        return (rect[0] + coordinates[0], rect[1] + coordinates[1])

    def set_camera_frame(self, raw_camera_frame_rgb):
        self.camera_frame = pygame.surfarray.make_surface(raw_camera_frame_rgb)

    def __draw_field(self):
        field_coordinates = self.__field_coordinates()
        field_resource = self.resource_loader.get_field_asset(self.field_side_dimension)
        aka_vertical_padding = 60
        field_frame = self.resource_loader.get_frame_asset(self.field_side_dimension + aka_vertical_padding)

        frame_coordinates = self.__relative_coordinates(field_coordinates, (-aka_vertical_padding/2,-aka_vertical_padding/2))
        self.sc.blit(field_resource, (field_coordinates[0], field_coordinates[1]))
        self.sc.blit(field_frame, (frame_coordinates[0], frame_coordinates[1]))

    def __get_cell_rect_coordinates(self, coordinate):
        field_coordinates = self.__field_coordinates()
        return self.__relative_coordinates(field_coordinates, (self.field_cell_width*coordinate[0], self.field_cell_height*coordinate[1]))

    def __draw_cross(self, cell_coordinate):
        coordinates = self.__get_cell_rect_coordinates(cell_coordinate)
        field_resource = self.resource_loader.get_cross_asset(self.field_side_dimension/5)
        self.sc.blit(field_resource, coordinates)

    def __draw_oval(self, cell_coordinate):
        coordinates = self.__get_cell_rect_coordinates(cell_coordinate)
        field_resource = self.resource_loader.get_nought_asset(self.field_side_dimension/5)
        self.sc.blit(field_resource, coordinates)

    def __draw_cursor(self, coordinate, valid):
        cell_coordinate = self.__get_cell_rect_coordinates(coordinate)
        field_resource = self.resource_loader.get_cursor_asset(valid, self.field_side_dimension/2)
        w, h = field_resource.get_size()
        center_offset = (w - self.field_cell_width) / 2
        length_penalty = coordinate[0] * self.field_side_dimension/10
        self.sc.blit(field_resource, self.__relative_coordinates(cell_coordinate, (-center_offset - length_penalty, -center_offset)))

    def __draw_gesture_field(self):
        field_resource = self.resource_loader.get_frame_asset(400)
        self.sc.blit(field_resource, (100, 170))

    def __draw_gaming_hint(self):
        resource = self.resource_loader.get_generic_asset('gaming_hint.png')
        self.sc.blit(resource, (100, 570))

    def __draw_gesture_field_hint(self):
        palm_hint = self.resource_loader.get_generic_asset('palm_hint.png')
        self.sc.blit(palm_hint, (125, 60))

    def __draw_start_game_hint(self, seconds):
        resource = self.resource_loader.get_start_hint_asset()
        self.sc.blit(resource, (280, 0))

        seconds = str(10 - int(seconds))
        if seconds in self.rendered_numbers:
            second_surface = self.rendered_numbers[seconds]
            self.sc.blit(second_surface, (700,655))

    def __process_game_state_and_cursor(self, state):
        if state.game_state.last_move_coordinate is not None:
            cursor_in_invalid_move_postion = state.scene_state.cursor_position.x == state.game_state.last_move_coordinate.x \
                and state.scene_state.cursor_position.y == state.game_state.last_move_coordinate.y

        cursor_invalid = state.game_state.last_move_result == MoveResult.CELL_OCCUPIED and cursor_in_invalid_move_postion
        self.__draw_cursor((state.scene_state.cursor_position.x, state.scene_state.cursor_position.y), not cursor_invalid)
        for i in range(state.game_state.size_y):
            for j in range(state.game_state.size_x):
                if state.game_state.field[i][j] == CellOccupation.X:
                    self.__draw_cross((j,i))
                if state.game_state.field[i][j] == CellOccupation.O:
                    self.__draw_oval((j,i))

    def __render_recognition_frame_hint(self):
        asset = self.resource_loader.get_generic_asset('recognition_frame_hint.png')
        self.sc.blit(asset, (120, 60))

    def __draw_bottom_hint(self, state):
        if state.scene_state.winner is not None:
            if state.scene_state.winner == Winner.X:
                asset = self.resource_loader.get_generic_asset('crosses_wins.png')
            if state.scene_state.winner == Winner.O:
                asset = self.resource_loader.get_generic_asset('noughts_wins.png')
            if state.scene_state.winner == Winner.NONE:
                asset = self.resource_loader.get_generic_asset('draw.png')
            self.sc.blit(asset,  (100, 570))
        else:
            if state.scene_state.should_render_calibration_tip:
                asset = self.resource_loader.get_generic_asset('calibration_hint.png')
                self.sc.blit(asset, (100, 570))
                time_since_game_begin = time.time() - state.scene_state.game_begin_timestamp
                seconds = str(30 - int(time_since_game_begin))
                if seconds in self.rendered_numbers:
                    second_surface = self.rendered_numbers[seconds]
                    self.sc.blit(second_surface, (770, 645))
            else:
                self.__draw_gaming_hint()

    def render(self, state):
        if self.camera_frame is not None:
            self.sc.blit(self.camera_frame, (0,0))
        else:
            self.sc.fill((255,255,255))

        if state.scene_state.should_render_start_tip:
            self.__draw_start_game_hint(time.time() - state.scene_state.game_begin_timestamp)
        elif state.scene_state.should_render_calibration_tip:
            self.__draw_field()
            self.__draw_gesture_field()
            self.__process_game_state_and_cursor(state)
            self.__draw_bottom_hint(state)
            self.__render_recognition_frame_hint()
        else:
            self.__draw_field()
            self.__draw_gesture_field()
            self.__draw_gesture_field_hint()
            self.__process_game_state_and_cursor(state)
            self.__draw_bottom_hint(state)
        pygame.display.update()
