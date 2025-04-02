from typing import Optional
from dataclasses import dataclass, field
from abc import ABC

import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AppConfig:
    source_folder_path: str = field(default=os.environ["SOURCE_FOLDER_PATH"])
    target_folder_path: str = field(default=os.environ["TARGET_FOLDER_PATH"])