from .help import dp
from .start import dp
from .main_commands import dp

from .admin_panel.cancel import dp
from .admin_panel.admin_command import dp
from .admin_panel.main_menu import dp
from .admin_panel.stocks import dp
from .admin_panel.mailing import dp
from .bonus_system import dp

from handlers.users.choose_city.by_buttons.handlers import dp
from handlers.users.choose_city.by_coordinates.handlers import dp
from handlers.users.choose_city.navigator import navigate
from .echo import dp

__all__ = ["dp"]
