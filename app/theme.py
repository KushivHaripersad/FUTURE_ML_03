import tkinter as tk
from tkinter import ttk
from tkinter import font

class AppTheme:
    def __init__(self):
        # Color Palette (Modern Blue Theme)
        self.colors = {
            'primary': '#2C3E50',      # Dark Blue
            'secondary': '#3498DB',     # Blue
            'accent': '#E74C3C',        # Red
            'success': '#27AE60',       # Green
            'warning': '#F39C12',       # Orange
            'light': '#ECF0F1',         # Light Gray
            'dark': '#2C3E50',          # Dark Blue
            'background': '#FFFFFF',    # White
            'card_bg': '#F8F9FA',       # Light Gray
            'text_primary': '#2C3E50',  # Dark Blue
            'text_secondary': '#7F8C8D',# Gray
            'border': '#BDC3C7'         # Gray
        }
        
        # Fonts
        self.fonts = {
            'title': ('Segoe UI', 18, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'subheading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9)
        }
        
    def apply_theme(self, root):
        """Apply theme to the root window"""
        style = ttk.Style()
        
        # Try to use a modern theme if available
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
        
        # Configure colors
        self._configure_styles(style)
        
        # Set window background
        root.configure(bg=self.colors['background'])
        
        # Create custom fonts
        self._create_fonts()
        
    def _configure_styles(self, style):
        """Configure ttk styles"""
        # Frame styles
        style.configure('Card.TFrame', 
                       background=self.colors['card_bg'],
                       borderwidth=2,
                       relief='solid')
        
        style.configure('Primary.TFrame',
                       background=self.colors['primary'])
        
        # Label styles
        style.configure('Title.TLabel',
                       font=self.fonts['title'],
                       foreground=self.colors['text_primary'],
                       background=self.colors['background'])
        
        style.configure('Heading.TLabel',
                       font=self.fonts['heading'],
                       foreground=self.colors['text_primary'],
                       background=self.colors['background'])
        
        style.configure('Subheading.TLabel',
                       font=self.fonts['subheading'],
                       foreground=self.colors['text_secondary'],
                       background=self.colors['background'])
        
        style.configure('Body.TLabel',
                       font=self.fonts['body'],
                       foreground=self.colors['text_primary'],
                       background=self.colors['background'])
        
        # Button styles
        style.configure('Primary.TButton',
                       font=self.fonts['subheading'],
                       foreground='white',
                       background=self.colors['secondary'],
                       borderwidth=2,
                       focuscolor='none')
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary']),
                           ('pressed', self.colors['dark'])])
        
        style.configure('Secondary.TButton',
                       font=self.fonts['body'],
                       foreground=self.colors['text_primary'],
                       background=self.colors['light'],
                       borderwidth=2)
        
        style.map('Secondary.TButton',
                 background=[('active', self.colors['border']),
                           ('pressed', self.colors['text_secondary'])])
        
        style.configure('Success.TButton',
                       font=self.fonts['body'],
                       foreground='white',
                       background=self.colors['success'])
        
        style.map('Success.TButton',
                 background=[('active', '#229954'),
                           ('pressed', '#1E8449')])
        
        style.configure('Warning.TButton',
                       font=self.fonts['body'],
                       foreground='white',
                       background=self.colors['warning'])
        
        style.map('Warning.TButton',
                 background=[('active', '#E67E22'),
                           ('pressed', '#D35400')])
        
        # Entry styles
        style.configure('Primary.TEntry',
                       fieldbackground='white',
                       foreground=self.colors['text_primary'],
                       borderwidth=2,
                       relief='solid')
        
        # Combobox styles
        style.configure('Primary.TCombobox',
                       fieldbackground='white',
                       foreground=self.colors['text_primary'])
        
        # Scrollbar styles
        style.configure('Vertical.TScrollbar',
                       background=self.colors['light'],
                       troughcolor=self.colors['background'],
                       bordercolor=self.colors['border'],
                       arrowcolor=self.colors['text_primary'])
        
        style.configure('Horizontal.TScrollbar',
                       background=self.colors['light'],
                       troughcolor=self.colors['background'],
                       bordercolor=self.colors['border'],
                       arrowcolor=self.colors['text_primary'])
        
        # Treeview styles
        style.configure('Treeview',
                       background='white',
                       foreground=self.colors['text_primary'],
                       fieldbackground='white',
                       rowheight=25)
        
        style.configure('Treeview.Heading',
                       font=self.fonts['body'],
                       background=self.colors['primary'],
                       foreground='white',
                       relief='flat')
        
        style.map('Treeview.Heading',
                 background=[('active', self.colors['secondary'])])
        
        # Notebook styles
        style.configure('TNotebook',
                       background=self.colors['background'],
                       tabmargins=[2, 5, 2, 0])
        
        style.configure('TNotebook.Tab',
                       font=self.fonts['body'],
                       padding=[15, 5],
                       background=self.colors['light'],
                       foreground=self.colors['text_primary'])
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['secondary']),
                           ('active', self.colors['border'])],
                 foreground=[('selected', 'white'),
                           ('active', self.colors['text_primary'])])
        
        # Progressbar styles
        style.configure('Horizontal.TProgressbar',
                       background=self.colors['secondary'],
                       troughcolor=self.colors['light'],
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['secondary'],
                       darkcolor=self.colors['secondary'])
    
    def _create_fonts(self):
        """Create custom fonts"""
        # These are already defined in the fonts dictionary
        # but we could create tkinter Font objects here if needed
        pass
    
    def create_gradient_frame(self, parent, width, height, color1, color2, **kwargs):
        """Create a gradient frame (for decorative purposes)"""
        frame = tk.Canvas(parent, width=width, height=height, 
                         highlightthickness=0, **kwargs)
        
        # Create gradient
        for i in range(height):
            # Calculate color at this position
            ratio = i / height
            r = int((1 - ratio) * int(color1[1:3], 16) + ratio * int(color2[1:3], 16))
            g = int((1 - ratio) * int(color1[3:5], 16) + ratio * int(color2[3:5], 16))
            b = int((1 - ratio) * int(color1[5:7], 16) + ratio * int(color2[5:7], 16))
            color = f'#{r:02x}{g:02x}{b:02x}'
            
            frame.create_line(0, i, width, i, fill=color)
        
        return frame
    
    def create_card(self, parent, **kwargs):
        """Create a card widget (modern frame with shadow effect)"""
        card_frame = ttk.Frame(parent, style='Card.TFrame', **kwargs)
        return card_frame
    
    def create_icon_button(self, parent, text, icon_char=None, **kwargs):
        """Create a button with optional icon"""
        btn = ttk.Button(parent, text=text, **kwargs)
        
        if icon_char:
            # In a real app, you might use an image here
            # For now, we'll just add the character before text
            btn.configure(text=f"{icon_char} {text}")
        
        return btn
    
    def create_metric_card(self, parent, title, value, unit="", trend=None):
        """Create a metric card for displaying statistics"""
        card = self.create_card(parent)
        
        # Title
        title_label = ttk.Label(card, text=title, style='Subheading.TLabel')
        title_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Value
        value_font = font.Font(family='Segoe UI', size=24, weight='bold')
        value_label = tk.Label(card, text=f"{value}{unit}", 
                              font=value_font,
                              fg=self.colors['text_primary'],
                              bg=self.colors['card_bg'])
        value_label.pack(anchor='w', padx=10, pady=(0, 5))
        
        # Trend indicator (if provided)
        if trend is not None:
            trend_color = self.colors['success'] if trend > 0 else self.colors['accent']
            trend_symbol = "Up" if trend > 0 else "Down"
            trend_label = ttk.Label(card, 
                                   text=f"{trend_symbol} {abs(trend)}%",
                                   style='Small.TLabel',
                                   foreground=trend_color)
            trend_label.pack(anchor='w', padx=10, pady=(0, 10))
        
        return card


class ModernUIComponents:
    """Collection of modern UI components"""
    
    @staticmethod
    def create_header(root, title, subtitle=None):
        """Create a modern header"""
        header_frame = ttk.Frame(root)
        
        # Title
        title_label = tk.Label(header_frame, text=title,
                              font=('Segoe UI', 24, 'bold'),
                              fg='#2C3E50')
        title_label.pack(side='left')
        
        if subtitle:
            subtitle_label = tk.Label(header_frame, text=subtitle,
                                     font=('Segoe UI', 12),
                                     fg='#7F8C8D')
            subtitle_label.pack(side='left', padx=(10, 0))
        
        return header_frame
    
    @staticmethod
    def create_status_indicator(parent, status, size=10):
        """Create a colored status indicator"""
        canvas = tk.Canvas(parent, width=size, height=size, 
                          highlightthickness=0, bg=parent['bg'])
        
        colors = {
            'success': '#27AE60',
            'warning': '#F39C12',
            'error': '#E74C3C',
            'info': '#3498DB',
            'idle': '#95A5A6'
        }
        
        color = colors.get(status.lower(), colors['idle'])
        canvas.create_oval(2, 2, size-2, size-2, fill=color, outline='')
        
        return canvas
    
    @staticmethod
    def create_progress_bar_with_label(parent, value, max_value=100, width=200, height=20):
        """Create a progress bar with percentage label"""
        frame = ttk.Frame(parent)
        
        # Progress bar
        progress = ttk.Progressbar(frame, length=width, 
                                  mode='determinate',
                                  style='Horizontal.TProgressbar')
        progress['value'] = (value / max_value) * 100
        progress.pack(side='left')
        
        # Percentage label
        percentage = (value / max_value) * 100
        label = tk.Label(frame, text=f"{percentage:.1f}%",
                        font=('Segoe UI', 9),
                        fg='#2C3E50')
        label.pack(side='left', padx=(5, 0))
        
        return frame