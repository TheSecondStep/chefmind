"""
上下文信息
"""
from dataclasses import dataclass
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal


@dataclass
class Context():
    """
    上下文信息
    """
    user_id: str


class UserInfo(BaseModel):
    """长期用户画像信息，用于个性化推荐与记忆。"""

    food_preferences: Optional[Dict[str, float]] = Field(
        default_factory=dict,
        description="用户对食材的综合偏好，键为食材名，值为偏好程度（0=极端厌恶，1=极端喜爱）"
    )

    cuisine_preferences: Optional[Dict[str, float]] = Field(
        default_factory=dict,
        description="用户对菜系的综合偏好，键为菜系名，值为偏好程度（0=极端厌恶，1=极端喜爱）"
    )

    taste_preferences: Optional[Dict[
        Literal["spicy", "sweet", "salty", "sour", "bitter", "umami"], float
    ]] = Field(
        default_factory=dict,
        description="用户口味偏好，键为口味类型（spicy/sweet/salty/sour/bitter/umami），值为偏好程度（0~1）"
    )

    ingredients: Optional[List[str]] = Field(
        default_factory=list,
        description="用户当前拥有的食材清单"
    )

    allergies: Optional[List[str]] = Field(
        default_factory=list,
        description="用户过敏的食材列表"
    )

    diet: Optional[List[str]] = Field(
        default_factory=list,
        description="用户的饮食习惯，例如 ['素食', '低糖', '高蛋白']"
    )
