"""ASCII Art and decorative elements for the SPARQL tutorial."""

MAIN_BANNER = r"""
  ██████  ██▓███   ▄▄▄       ██▀███    ▄████   ██▓
▒██    ▒ ▓██░  ██▒▒████▄    ▓██ ▒ ██▒ ██▒ ▀█▒ ▓██▒
░ ▓██▄   ▓██░ ██▓▒▒██  ▀█▄  ▓██ ░▄█ ▒▒██░▄▄▄░ ▒██░
  ▒   ██▒▒██▄█▓▒ ▒░██▄▄▄▄██ ▒██▀▀█▄  ░▓█  ██▓ ▒██░
▒██████▒▒▒██▒ ░  ░ ▓█   ▓██▒░██▓ ▒██▒░▒▓███▀▒ ░██████▒
▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░ ░▒   ▒  ░ ▒░▓  ░
░ ░▒  ░ ░░▒ ░       ▒   ▒▒ ░  ░▒ ░ ▒░  ░   ░  ░ ░ ▒  ░
░  ░  ░  ░░         ░   ▒     ░░   ░ ░ ░   ░    ░ ░
      ░                 ░  ░   ░           ░      ░  ░
"""

SUBTITLE = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║          ✦  Interactive SPARQL Tutorial for Beginners  ✦                      ║
║                  Explore the Space Knowledge Graph                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

ROCKET = r"""
        ^
       / \
      /   \
     /     \
    |  NASA |
    |       |
   /|       |\
  / |       | \
 /  |       |  \
|   |_______|   |
|    \     /    |
|     \   /     |
 \     | |     /
  \    | |    /
   \  /   \  /
    \/     \/
     |     |
     |     |
    /       \
   /  FIRE!  \
  /___________\
"""

PLANET = r"""
         _..._
       .'     '.
      /  o   o  \
     |     ^     |
     |  \-----/  |
      \  '---'  /
       '._____.'
"""

SATELLITE = r"""
         .-.
        ( o )
  .------'-'------.
  |  .--.  .--. oo|
  | |    ||    |  |
  |  '--'  '--'   |
  '-------..------'
         /||\
        //||\\
       // || \\
      //  ||  \\
     []   []   []
"""

ASTRONAUT = r"""
     .---.
    /     \
   | () () |
    \  ^  /
     |||||
    /|   |\
   (_|   |_)
"""

STARS_LINE = "✦ · ˚ * . ★ · ✧ . ✦ · ˚ * . ★ · ✧ . ✦ · ˚ * . ★ · ✧ . ✦ · ˚ * . ★"

DIVIDER_DOUBLE = "═" * 80
DIVIDER_SINGLE = "─" * 80
DIVIDER_DOTS = "· " * 40

LESSON_COMPLETE = r"""
  ╔═══════════════════════════════════════╗
  ║                                       ║
  ║    ★  LESSON COMPLETE!  ★            ║
  ║                                       ║
  ╚═══════════════════════════════════════╝
"""

EXERCISE_CORRECT = r"""
    ✓ ═══════════════════════════════════
    ║   CORRECT! Well done, explorer!   ║
    ═══════════════════════════════════ ✓
"""

TROPHY = r"""
       ___________
      '._==_==_=_.'
      .-\:      /-.
     | (|:.     |) |
      '-|:.     |-'
        \::.    /
         '::. .'
           ) (
         _.' '._
        '-------'
"""

HINT_ICON = r"""
    ┌───┐
    │ ? │
    └───┘
"""

def get_progress_bar(current: int, total: int, width: int = 40) -> str:
    """Generate an ASCII progress bar."""
    filled = int(width * current / total) if total > 0 else 0
    empty = width - filled
    percentage = int(100 * current / total) if total > 0 else 0

    bar = f"[{'█' * filled}{'░' * empty}] {current}/{total} ({percentage}%)"
    return bar

def get_menu_header(title: str) -> str:
    """Generate a decorated menu header."""
    width = 60
    padding = (width - len(title) - 4) // 2

    return f"""
╔{'═' * width}╗
║{' ' * padding}★ {title} ★{' ' * (width - padding - len(title) - 4)}║
╚{'═' * width}╝
"""

def get_lesson_header(number: int, title: str) -> str:
    """Generate a lesson header with number and title."""
    return f"""
┌────────────────────────────────────────────────────────────────────────────────┐
│  LESSON {number:02d}: {title:<65} │
└────────────────────────────────────────────────────────────────────────────────┘
"""

def get_section_box(title: str, content: str) -> str:
    """Generate a boxed section with title."""
    lines = content.split('\n')
    max_width = max(len(line) for line in lines)
    max_width = max(max_width, len(title) + 4)

    box = f"┌─ {title} " + "─" * (max_width - len(title) - 3) + "┐\n"
    for line in lines:
        box += f"│ {line:<{max_width}} │\n"
    box += "└" + "─" * (max_width + 2) + "┘"

    return box

GOODBYE = r"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   Thank you for exploring SPARQL with us!                                     ║
║                                                                               ║
║   May your queries always return the data you seek.  ✦                        ║
║                                                                               ║
║        "The cosmos is within us. We are made of star-stuff."                  ║
║                                        - Carl Sagan                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

          *    .  *       .             *
                       *
     *   .        *       .       .       *
       .     *
            .     *  .     . *     .     *
"""
