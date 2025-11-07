from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel


class AnalystType(str, Enum):
    STRATEGIC = "market"
    OPERATIONAL = "fundamentals"
    MARKETING_CUSTOMER = "social"
    RISK_EXTERNAL = "news"
