# Configuration and color scheme for A* Path Planning GUI

# Grid dimensions (matches AStar class)
GRID_WIDTH = 300
GRID_HEIGHT = 200

# Scale factor for canvas (2x for better visibility)
SCALE = 3

# Canvas dimensions
CANVAS_WIDTH = GRID_WIDTH * SCALE
CANVAS_HEIGHT = GRID_HEIGHT * SCALE

# Color scheme (modern dark theme)
COLORS = {
    # Background
    'background': '#1a1a2e',
    'canvas_bg': '#0f0f1a',

    # Obstacles
    'obstacle': '#e94560',
    'obstacle_outline': '#ff6b6b',

    # Free space
    'free_space': '#16213e',

    # Points
    'start': '#00ff88',
    'start_outline': '#ffffff',
    'goal': '#ff6600',
    'goal_outline': '#ffffff',

    # Search visualization
    'explored': '#4a90d9',
    'path': '#f1c40f',
    'path_outline': '#ffffff',

    # UI elements
    'text': '#eaeaea',
    'text_secondary': '#888888',
    'button_bg': '#16213e',
    'button_fg': '#eaeaea',
    'button_active': '#1f4068',
    'slider_trough': '#0f3460',
}

# Default parameter values
DEFAULTS = {
    'radius': 5,
    'clearance': 5,
    'step_size': 1,
    'animation_speed': 1,  # milliseconds delay (lower = faster)
}

# Parameter ranges
PARAM_RANGES = {
    'radius': (0, 20),
    'clearance': (0, 20),
    'step_size': (1, 10),
    'animation_speed': (1, 50),
}

# Point marker size (radius in pixels)
POINT_MARKER_SIZE = 8
