from dataclasses import dataclass


@dataclass
class User(PG_config):
    id : int = None