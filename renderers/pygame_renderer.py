import os

import pygame

from model.cell_occupation import CellOccupation
import cv.constants as constants


class PyGameRenderer:

    def __init__(self):
        pygame.init()
        self.width = 500
        self.height = 500
        self.field_edges_color = (64, 128, 255)

        #defaults
        self.field_width_cells = 3
        self.field_height_cells = 3

        self.field_side_dimension = 300

        self.field_cell_width = self.field_side_dimension / self.field_width_cells
        self.field_cell_height = self.field_side_dimension / self.field_height_cells

        self.camera_frame = None
        self.sc = pygame.display.set_mode((constants.UI_WINDOW_WIDTH, constants.UI_WINDOW_HEIGHT))

        # здесь будут рисоваться фигуры

        pygame.display.update()

    def setup_with_field(self, state):
        self.field_height_cells = state.size_y
        self.field_width_cells = state.size_x

        self.field_cell_width = self.field_side_dimension / state.size_x
        self.field_cell_height = self.field_side_dimension / state.size_y

    def __field_coordinates(self):
        return (20, 20, self.field_side_dimension, self.field_side_dimension)

    def __relative_coordinates(self, rect, coordinates):
        return (rect[0] + coordinates[0], rect[1] + coordinates[1])

    def set_camera_frame(self, raw_camera_frame_rgb):
        self.camera_frame = pygame.surfarray.make_surface(raw_camera_frame_rgb)

    def __draw_field(self):
        field_coordinates = self.__field_coordinates()

        pygame.draw.rect(self.sc, self.field_edges_color, field_coordinates, 4)

        for i in range(1, self.field_width_cells):
            pygame.draw.line(self.sc, self.field_edges_color,
                             self.__relative_coordinates(field_coordinates, (self.field_cell_width*i, 0)),
                             self.__relative_coordinates(field_coordinates, (self.field_cell_width*i, self.field_side_dimension)))

        for i in range(1, self.field_height_cells):
            pygame.draw.line(self.sc, self.field_edges_color,
                             self.__relative_coordinates(field_coordinates, (0, self.field_cell_height*i)),
                             self.__relative_coordinates(field_coordinates, (self.field_side_dimension, self.field_cell_height*i)))

    def __get_cell_rect_coordinates(self, coordinate):
        field_coordinates = self.__field_coordinates()
        return self.__relative_coordinates(field_coordinates, (self.field_cell_width*coordinate[0], self.field_cell_height*coordinate[1]))

    def __draw_cross(self, cell_coordinate):
        coordinates = self.__get_cell_rect_coordinates(cell_coordinate)
        pygame.draw.line(self.sc, self.field_edges_color,
                         (coordinates[0], coordinates[1]),
                         (coordinates[0] + self.field_cell_width, coordinates[1]+ self.field_cell_height), 3)
        pygame.draw.line(self.sc, self.field_edges_color,
                         (coordinates[0] + self.field_cell_width, coordinates[1]),
                         (coordinates[0], coordinates[1] + self.field_cell_height), 3)

    def __draw_oval(self, cell_coordinate):
        coordinates = self.__get_cell_rect_coordinates(cell_coordinate)
        pygame.draw.line(self.sc, (255,0,0),
                         (coordinates[0], coordinates[1]),
                         (coordinates[0] + self.field_cell_width, coordinates[1]+ self.field_cell_height), 3)
        pygame.draw.line(self.sc, (255,0,0),
                         (coordinates[0] + self.field_cell_width, coordinates[1]),
                         (coordinates[0], coordinates[1] + self.field_cell_height), 3)

    def __draw_cursor(self, coordinate):
        cell_coordinate = self.__get_cell_rect_coordinates(coordinate)
        pygame.draw.rect(self.sc, (0,255,0), (cell_coordinate[0] + 20, cell_coordinate[1] + 20, self.field_cell_width - 40, self.field_cell_height -40))

    def render(self, state):
        if self.camera_frame is not None:
            self.sc.blit(self.camera_frame, (0,0))
        else:
            self.sc.fill((255,255,255))
        self.__draw_field()


        self.__draw_cursor((state.cursor_position.x, state.cursor_position.y))
        for i in range(state.game_state.size_y):
            for j in range(state.game_state.size_x):
                if state.game_state.field[i][j] == CellOccupation.X:
                    self.__draw_cross((j,i))
                if state.game_state.field[i][j] == CellOccupation.O:
                    self.__draw_oval((j,i))
        pygame.display.update()

        #
        # print('cursor: ' + str(model.cursor_position))
        # print('last move result: ' + str(model.last_move_result))