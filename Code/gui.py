#!/usr/bin/env python3
"""
A* Path Planning Visualizer - Interactive GUI

Features:
- Click to set start (left-click) and goal (right-click) points
- Adjustable parameters: robot radius, clearance, step size
- Animated search visualization with speed control
- Modern dark theme
"""

import tkinter as tk
from tkinter import ttk
from utils import AStar
from gui_config import (
    GRID_WIDTH, GRID_HEIGHT, SCALE, COLORS, DEFAULTS, PARAM_RANGES
)
from gui_canvas import PathCanvas


class AStarGUI:
    """Main GUI application for A* path planning visualization."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("A* Path Planning Visualizer")
        self.root.configure(bg=COLORS['background'])
        self.root.resizable(False, False)

        # State
        self.is_animating = False
        self.animation_id = None
        self.explored_states = []
        self.path_states = []
        self.anim_index = 0

        # Setup UI
        self._setup_styles()
        self._setup_ui()
        self._bind_events()

        # Initial obstacle render
        self.root.after(100, self._redraw_obstacles)

    def _setup_styles(self):
        """Configure ttk styles for modern look."""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure scale (slider) style
        style.configure(
            'TScale',
            background=COLORS['background'],
            troughcolor=COLORS['slider_trough'],
        )

        # Configure button style
        style.configure(
            'TButton',
            background=COLORS['button_bg'],
            foreground=COLORS['button_fg'],
            padding=(20, 10),
            font=('Helvetica', 11, 'bold')
        )
        style.map('TButton',
            background=[('active', COLORS['button_active'])]
        )

    def _setup_ui(self):
        """Setup all UI components."""
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(padx=20, pady=20)

        # Title
        title = tk.Label(
            main_frame,
            text="A* Path Planning Visualizer",
            font=('Helvetica', 18, 'bold'),
            fg=COLORS['text'],
            bg=COLORS['background']
        )
        title.pack(pady=(0, 10))

        # Instructions
        instructions = tk.Label(
            main_frame,
            text="Left-click: Set Start  |  Right-click: Set Goal",
            font=('Helvetica', 10),
            fg=COLORS['text_secondary'],
            bg=COLORS['background']
        )
        instructions.pack(pady=(0, 10))

        # Canvas
        self.canvas = PathCanvas(main_frame, AStar)
        self.canvas.pack(pady=10)

        # Control panel
        self._setup_controls(main_frame)

    def _setup_controls(self, parent):
        """Setup the control panel with sliders and buttons."""
        control_frame = tk.Frame(parent, bg=COLORS['background'])
        control_frame.pack(fill='x', pady=10)

        # Left side - coordinates display
        coords_frame = tk.Frame(control_frame, bg=COLORS['background'])
        coords_frame.pack(side='left', padx=20)

        self.start_label = tk.Label(
            coords_frame,
            text="Start: Not set",
            font=('Helvetica', 11),
            fg=COLORS['start'],
            bg=COLORS['background'],
            width=20,
            anchor='w'
        )
        self.start_label.pack(anchor='w')

        self.goal_label = tk.Label(
            coords_frame,
            text="Goal: Not set",
            font=('Helvetica', 11),
            fg=COLORS['goal'],
            bg=COLORS['background'],
            width=20,
            anchor='w'
        )
        self.goal_label.pack(anchor='w')

        # Middle - parameters
        params_frame = tk.Frame(control_frame, bg=COLORS['background'])
        params_frame.pack(side='left', padx=40)

        # Robot Radius
        self._create_slider(
            params_frame, "Robot Radius:", 'radius',
            PARAM_RANGES['radius'][0], PARAM_RANGES['radius'][1],
            DEFAULTS['radius']
        )

        # Clearance
        self._create_slider(
            params_frame, "Clearance:", 'clearance',
            PARAM_RANGES['clearance'][0], PARAM_RANGES['clearance'][1],
            DEFAULTS['clearance']
        )

        # Step Size
        self._create_slider(
            params_frame, "Step Size:", 'step_size',
            PARAM_RANGES['step_size'][0], PARAM_RANGES['step_size'][1],
            DEFAULTS['step_size']
        )

        # Right side - animation speed
        speed_frame = tk.Frame(control_frame, bg=COLORS['background'])
        speed_frame.pack(side='left', padx=40)

        self._create_slider(
            speed_frame, "Animation Speed:", 'speed',
            PARAM_RANGES['animation_speed'][0], PARAM_RANGES['animation_speed'][1],
            DEFAULTS['animation_speed']
        )

        # Buttons frame
        button_frame = tk.Frame(parent, bg=COLORS['background'])
        button_frame.pack(pady=15)

        self.run_button = tk.Button(
            button_frame,
            text="RUN",
            command=self._on_run,
            font=('Helvetica', 12, 'bold'),
            bg=COLORS['start'],
            fg='#000000',
            activebackground='#00cc6a',
            width=10,
            height=1,
            cursor='hand2'
        )
        self.run_button.pack(side='left', padx=10)

        self.stop_button = tk.Button(
            button_frame,
            text="STOP",
            command=self._on_stop,
            font=('Helvetica', 12, 'bold'),
            bg=COLORS['obstacle'],
            fg='#ffffff',
            activebackground='#cc3344',
            width=10,
            height=1,
            cursor='hand2',
            state='disabled'
        )
        self.stop_button.pack(side='left', padx=10)

        self.reset_button = tk.Button(
            button_frame,
            text="RESET",
            command=self._on_reset,
            font=('Helvetica', 12, 'bold'),
            bg=COLORS['button_bg'],
            fg=COLORS['button_fg'],
            activebackground=COLORS['button_active'],
            width=10,
            height=1,
            cursor='hand2'
        )
        self.reset_button.pack(side='left', padx=10)

        # Status frame
        status_frame = tk.Frame(parent, bg=COLORS['background'])
        status_frame.pack(pady=5)

        self.status_label = tk.Label(
            status_frame,
            text="Status: Ready",
            font=('Helvetica', 11),
            fg=COLORS['text'],
            bg=COLORS['background']
        )
        self.status_label.pack(side='left', padx=20)

        self.distance_label = tk.Label(
            status_frame,
            text="Distance: ---",
            font=('Helvetica', 11),
            fg=COLORS['path'],
            bg=COLORS['background']
        )
        self.distance_label.pack(side='left', padx=20)

    def _create_slider(self, parent, label_text, var_name, min_val, max_val, default):
        """Create a labeled slider."""
        frame = tk.Frame(parent, bg=COLORS['background'])
        frame.pack(fill='x', pady=2)

        label = tk.Label(
            frame,
            text=label_text,
            font=('Helvetica', 10),
            fg=COLORS['text'],
            bg=COLORS['background'],
            width=15,
            anchor='e'
        )
        label.pack(side='left')

        var = tk.IntVar(value=default)
        setattr(self, f'{var_name}_var', var)

        slider = ttk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            variable=var,
            orient='horizontal',
            length=120,
            command=lambda v, n=var_name: self._on_slider_change(n)
        )
        slider.pack(side='left', padx=5)

        value_label = tk.Label(
            frame,
            textvariable=var,
            font=('Helvetica', 10, 'bold'),
            fg=COLORS['text'],
            bg=COLORS['background'],
            width=3
        )
        value_label.pack(side='left')

    def _bind_events(self):
        """Bind mouse events to canvas."""
        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<Button-2>", self._on_right_click)  # Middle click (Mac)
        self.canvas.bind("<Button-3>", self._on_right_click)  # Right click
        self.canvas.bind("<Motion>", self._on_mouse_move)

    def _on_slider_change(self, var_name):
        """Handle slider value changes."""
        if var_name in ('radius', 'clearance'):
            self._redraw_obstacles()

    def _redraw_obstacles(self):
        """Redraw obstacles with current radius and clearance."""
        if self.is_animating:
            return
        radius = self.radius_var.get()
        clearance = self.clearance_var.get()
        self.canvas.draw_obstacles(radius, clearance)
        self.canvas.raise_markers()

    def _on_left_click(self, event):
        """Handle left click - set start point."""
        if self.is_animating:
            return

        row, col = self.canvas.canvas_to_grid(event.x, event.y)

        # Validate position
        if not self._is_valid_position(row, col):
            self.status_label.config(text="Status: Invalid position!", fg=COLORS['obstacle'])
            return

        self.canvas.set_start(row, col)
        self.start_label.config(text=f"Start: ({col}, {row})")
        self.status_label.config(text="Status: Start set", fg=COLORS['text'])
        self.canvas.clear_path()

    def _on_right_click(self, event):
        """Handle right click - set goal point."""
        if self.is_animating:
            return

        row, col = self.canvas.canvas_to_grid(event.x, event.y)

        # Validate position
        if not self._is_valid_position(row, col):
            self.status_label.config(text="Status: Invalid position!", fg=COLORS['obstacle'])
            return

        self.canvas.set_goal(row, col)
        self.goal_label.config(text=f"Goal: ({col}, {row})")
        self.status_label.config(text="Status: Goal set", fg=COLORS['text'])
        self.canvas.clear_path()

    def _on_mouse_move(self, event):
        """Show coordinates on mouse hover."""
        if self.is_animating:
            return
        row, col = self.canvas.canvas_to_grid(event.x, event.y)
        if 1 <= row <= GRID_HEIGHT and 1 <= col <= GRID_WIDTH:
            # Could update a coordinate display here if desired
            pass

    def _is_valid_position(self, row, col):
        """Check if a position is valid (in bounds and not obstacle)."""
        radius = self.radius_var.get()
        clearance = self.clearance_var.get()

        temp_astar = AStar((row, col), (row, col), clearance, radius, 1)
        return temp_astar.IsValid(row, col) and not temp_astar.IsObstacle(row, col)

    def _on_run(self):
        """Run the A* search algorithm."""
        if self.is_animating:
            return

        # Validate start and goal
        if not self.canvas.start_point:
            self.status_label.config(text="Status: Set start point first!", fg=COLORS['obstacle'])
            return
        if not self.canvas.goal_point:
            self.status_label.config(text="Status: Set goal point first!", fg=COLORS['obstacle'])
            return

        # Clear previous path
        self.canvas.clear_path()

        # Get parameters
        start = self.canvas.start_point
        goal = self.canvas.goal_point
        radius = self.radius_var.get()
        clearance = self.clearance_var.get()
        step_size = self.step_size_var.get()

        # Create AStar instance and run search
        self.status_label.config(text="Status: Searching...", fg=COLORS['explored'])
        self.root.update()

        astar = AStar(start, goal, clearance, radius, step_size)

        # Validate start and goal with current parameters
        if not astar.IsValid(start[0], start[1]) or astar.IsObstacle(start[0], start[1]):
            self.status_label.config(text="Status: Start is invalid with current params!", fg=COLORS['obstacle'])
            return
        if not astar.IsValid(goal[0], goal[1]) or astar.IsObstacle(goal[0], goal[1]):
            self.status_label.config(text="Status: Goal is invalid with current params!", fg=COLORS['obstacle'])
            return

        # Run search
        explored, path, distance = astar.search()

        self.explored_states = explored
        self.path_states = path
        self.anim_index = 0

        print(f"Search complete: {len(explored)} explored, {len(path)} path nodes, distance={distance}")

        if distance == float('inf') or len(path) == 0:
            self.status_label.config(text="Status: No path found!", fg=COLORS['obstacle'])
            self.distance_label.config(text="Distance: ---")
            # Still show explored states
            if len(explored) > 0:
                self.is_animating = True
                self.run_button.config(state='disabled')
                self.stop_button.config(state='normal')
                self._animate_step()
        else:
            self.distance_label.config(text=f"Distance: {distance:.2f}")
            # Start animation
            self.is_animating = True
            self.run_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self._animate_step()

    def _animate_step(self):
        """Animate one step of the search visualization."""
        if not self.is_animating:
            return

        # Draw batch of explored cells
        batch_size = max(1, len(self.explored_states) // 200)
        for _ in range(batch_size):
            if self.anim_index < len(self.explored_states):
                state = self.explored_states[self.anim_index]
                self.canvas.draw_explored_cell(state)
                self.anim_index += 1

        # Update status
        progress = int((self.anim_index / len(self.explored_states)) * 100) if self.explored_states else 100
        self.status_label.config(text=f"Status: Exploring... {progress}%", fg=COLORS['explored'])

        # Force canvas update
        self.canvas.update_idletasks()

        if self.anim_index < len(self.explored_states):
            # Schedule next frame
            delay = self.speed_var.get()
            self.animation_id = self.root.after(delay, self._animate_step)
        else:
            # Done exploring, draw path
            self._draw_final_path()

    def _draw_final_path(self):
        """Draw the final path after exploration animation."""
        self.canvas.raise_markers()

        if self.path_states:
            for state in self.path_states:
                self.canvas.draw_path_cell(state)
            self.canvas.raise_markers()
            self.status_label.config(text="Status: Path found!", fg=COLORS['path'])
        else:
            self.status_label.config(text="Status: No path found!", fg=COLORS['obstacle'])

        self.is_animating = False
        self.run_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def _on_stop(self):
        """Stop the current animation."""
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        self.is_animating = False
        self.run_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Status: Stopped", fg=COLORS['text'])

    def _on_reset(self):
        """Reset everything to initial state."""
        self._on_stop()
        self.canvas.clear_all()
        self.start_label.config(text="Start: Not set")
        self.goal_label.config(text="Goal: Not set")
        self.status_label.config(text="Status: Ready", fg=COLORS['text'])
        self.distance_label.config(text="Distance: ---")
        self.explored_states = []
        self.path_states = []
        self._redraw_obstacles()

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    app = AStarGUI()
    app.run()


if __name__ == "__main__":
    main()
