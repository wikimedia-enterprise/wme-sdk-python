from typing import List, Optional
from datetime import datetime


class Editor:
    def __init__(self,
                 identifier: Optional[int] = None,
                 name: Optional[str] = None,
                 edit_count: Optional[int] = None,
                 groups: Optional[List[str]] = None,
                 is_bot: Optional[bool] = None,
                 is_anonymous: Optional[bool] = None,
                 is_admin: Optional[bool] = None,
                 is_patroller: Optional[bool] = None,
                 has_advanced_rights: Optional[bool] = None,
                 date_started: Optional[datetime] = None):
        self.identifier = identifier
        self.name = name
        self.edit_count = edit_count
        self.groups = groups or []
        self.is_bot = is_bot
        self.is_anonymous = is_anonymous
        self.is_admin = is_admin
        self.is_patroller = is_patroller
        self.has_advanced_rights = has_advanced_rights
        self.date_started = date_started
