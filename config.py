from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import subprocess
import os
from libqtile import hook
from libqtile.config import Screen
from libqtile import bar, widget

terminal = "alacritty"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([home])


mod = "mod4"
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "mod1"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "mod1"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "mod1"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "mod1"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "shift"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "shift"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "shift"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "shift"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "x", lazy.spawn("firefox"), desc="launch firefox"),
    Key([mod], "c", lazy.spawn("google-chrome-stable"), desc="launch chrome"),
    Key([mod], "a", lazy.spawn("nemo"), desc="launch nemo"),
    Key([mod], "e", lazy.spawn("alacritty -e ranger"), desc="launch ranger"),
    Key([mod], "f", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "r", lazy.spawn("rofi -show combi"), desc="Spawn Rofi"),
    # Toggle between different layouts as defined below
    # Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "mod1"], "e", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "mod1"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]]
group_hotkeys = "123456789"

for g, k in zip(groups, group_hotkeys):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                k,
                lazy.group[g.name].toscreen(),
                desc=f"Switch to group {g.name}",
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                k,
                lazy.window.togroup(g.name, switch_group=False),
                desc=f"Switch to & move focused window to group {g.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# Colors
catppuccin = {
    "flamingo": "#F3CDCD",
    "mauve": "#DDB6F2",
    "pink": "#f5c2e7",
    "maroon": "#e8a2af",
    "red": "#f28fad",
    "peach": "#f8bd96",
    "yellow": "#fae3b0",
    "green": "#abe9b3",
    "teal": "#b4e8e0",
    "blue": "#96cdfb",
    "sky": "#89dceb",
    "white": "#d9e0ee",
    "gray": "#6e6c7e",
    "black": "#1a1826",
    "purp": "#c68aee",
}

layouts = [
    layout.MonadTall(
        margin=3,
        border_width=2,
    ),
    layout.Columns(border_focus_stack=["#89dceb", "#89dceb"], border_width=2),
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=3),
    layout.Max(),
    # layout.Floating(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=16,
    padding=2,
    forground=catppuccin["black"],
)
extension_defaults = widget_defaults.copy()


def get_widgets(primary=False):
    widgets = [
        widget.Spacer(
            length=3,
            background="#00000000",
        ),
        widget.GroupBox(
            highlight_method="line",
            background=catppuccin["black"],
            highlight_color=[catppuccin["mauve"], catppuccin["mauve"]],
            inactive=catppuccin["purp"],
        ),
        widget.WindowName(
            fontsize=16,
            foreground=catppuccin["white"]
        ),
        widget.Volume(
            fmt="墳 {}",
            mute_command="amixer -D pulse set Master toggle",
            background=catppuccin["black"],
            foreground=catppuccin["purp"],
        ),
        widget.TextBox(
            text="|",
            padding=2,
            fontsize=30,
            foreground=catppuccin["purp"],
            background=catppuccin["black"],
        ),
        widget.CPU(
            format=" {load_percent:04}%",
            background=catppuccin["black"],
            foreground=catppuccin["purp"],
        ),
        widget.TextBox(
            text="|",
            padding=2,
            fontsize=30,
            foreground=catppuccin["purp"],
            background=catppuccin["black"],
        ),
        widget.Clock(
            format="%I:%M %p",
            background=catppuccin["black"],
            foreground=catppuccin["purp"],
        ),
    ]
    if primary:
        widgets.insert(10, widget.Systray())
    return widgets


screens = [
    Screen(
        top=bar.Bar(
            get_widgets(primary=True),
            20,
            background="#00000000",
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

screens = [
    Screen()
]

keys = [
    Key([mod, "control"], "r", lazy.reload_config(),
        lazy.spawn("~/.config/polybar/launch.sh")),
]
