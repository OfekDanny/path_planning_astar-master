# Canvas rendering for A* Path Planning GUI

import tkinter as tk
from gui_config import (
    GRID_WIDTH, GRID_HEIGHT, SCALE, CANVAS_WIDTH, CANVAS_HEIGHT,
    COLORS, POINT_MARKER_SIZE
)


class PathCanvas(tk.Canvas):
    """Custom canvas for rendering the A* path planning visualization."""

    def __init__(self, parent, astar_class, **kwargs):
        super().__init__(
            parent,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=COLORS['canvas_bg'],
            highlightthickness=2,
            highlightbackground=COLORS['text_secondary'],
            **kwargs
        )
        self.astar_class = astar_class
        self.start_point = None
        self.goal_point = None
        self.obstacle_items = []
        self.explored_items = []
        self.path_items = []
        self.start_marker = None
        self.goal_marker = None

    def grid_to_canvas(self, row, col):
        """Convert AStar grid coordinates to canvas coordinates.

        AStar uses 1-indexed (row, col) where row 1 is at the bottom.
        Canvas uses 0-indexed (x, y) where y=0 is at the top.
        """
        x = (col - 1) * SCALE
        y = (GRID_HEIGHT - row) * SCALE
        return x, y

    def canvas_to_grid(self, x, y):
        """Convert canvas coordinates to AStar grid coordinates."""
        col = (x // SCALE) + 1
        row = GRID_HEIGHT - (y // SCALE)
        return row, col

    def draw_obstacles(self, radius=0, clearance=0):
        """Draw all obstacles on the canvas using the AStar IsObstacle method."""
        # Clear existing obstacles
        for item in self.obstacle_items:
            self.delete(item)
        self.obstacle_items = []

        # Create a temporary AStar instance to check obstacles
        temp_astar = self.astar_class((1, 1), (1, 1), clearance, radius, 1)

        # Iterate through grid and draw obstacles
        for row in range(1, GRID_HEIGHT + 1):
            for col in range(1, GRID_WIDTH + 1):
                if temp_astar.IsObstacle(row, col):
                    x, y = self.grid_to_canvas(row, col)
                    item = self.create_rectangle(
                        x, y, x + SCALE, y + SCALE,
                        fill=COLORS['obstacle'],
                        outline='',
                        tags='obstacle'
                    )
                    self.obstacle_items.append(item)

    def draw_cell(self, row, col, color, tag='cell'):
        """Draw a single cell at the given grid position."""
        x, y = self.grid_to_canvas(row, col)
        item = self.create_rectangle(
            x, y, x + SCALE, y + SCALE,
            fill=color,
            outline='',
            tags=tag
        )
        return item

    def draw_explored_cell(self, state):
        """Draw an explored state cell."""
        row, col = state
        item = self.draw_cell(row, col, COLORS['explored'], 'explored')
        self.explored_items.append(item)
        return item

    def draw_path_cell(self, state):
        """Draw a path cell with emphasis."""
        row, col = state
        x, y = self.grid_to_canvas(row, col)
        # Draw slightly larger for visibility
        item = self.create_rectangle(
            x, y, x + SCALE, y + SCALE,
            fill=COLORS['path'],
            outline=COLORS['path_outline'],
            width=1,
            tags='path'
        )
        self.path_items.append(item)
        return item

    def set_start(self, row, col):
        """Set and draw the start point."""
        self.start_point = (row, col)
        if self.start_marker:
            self.delete(self.start_marker)

        x, y = self.grid_to_canvas(row, col)
        # Center the marker in the cell
        cx = x + SCALE // 2
        cy = y + SCALE // 2

        self.start_marker = self.create_oval(
            cx - POINT_MARKER_SIZE, cy - POINT_MARKER_SIZE,
            cx + POINT_MARKER_SIZE, cy + POINT_MARKER_SIZE,
            fill=COLORS['start'],
            outline=COLORS['start_outline'],
            width=2,
            tags='start'
        )
        # Raise to top
        self.tag_raise('start')

    def set_goal(self, row, col):
        """Set and draw the goal point."""
        self.goal_point = (row, col)
        if self.goal_marker:
            self.delete(self.goal_marker)

        x, y = self.grid_to_canvas(row, col)
        # Center the marker in the cell
        cx = x + SCALE // 2
        cy = y + SCALE // 2

        self.goal_marker = self.create_oval(
            cx - POINT_MARKER_SIZE, cy - POINT_MARKER_SIZE,
            cx + POINT_MARKER_SIZE, cy + POINT_MARKER_SIZE,
            fill=COLORS['goal'],
            outline=COLORS['goal_outline'],
            width=2,
            tags='goal'
        )
        # Raise to top
        self.tag_raise('goal')

    def clear_path(self):
        """Clear explored states and path, keep start/goal."""
        for item in self.explored_items:
            self.delete(item)
        self.explored_items = []

        for item in self.path_items:
            self.delete(item)
        self.path_items = []

        # Re-raise start and goal markers
        if self.start_marker:
            self.tag_raise('start')
        if self.goal_marker:
            self.tag_raise('goal')

    def clear_all(self):
        """Clear everything including start and goal."""
        self.clear_path()

        if self.start_marker:
            self.delete(self.start_marker)
            self.start_marker = None
        self.start_point = None

        if self.goal_marker:
            self.delete(self.goal_marker)
            self.goal_marker = None
        self.goal_point = None

    def raise_markers(self):
        """Raise start and goal markers above other elements."""
        self.tag_raise('start')
        self.tag_raise('goal')
