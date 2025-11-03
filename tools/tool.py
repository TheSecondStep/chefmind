"""
中华小当家（chefgod）Agent工具代码
"""

from typing import List

from langchain.tools import ToolRuntime, tool
from typing_extensions import Literal

from context import Context


@tool
def update_user_info(runtime: ToolRuntime[Context],
                     food_preferences: dict[str, float],
                     cuisine_preferences: dict[str, float],
                     taste_preferences: dict[Literal["spicy", "sweet",
                                                     "salty", "sour", "bitter", "umami"], float],
                     ingredients: List[dict[str, str]],
                     allergies: List[str],
                     diet: List[str]) -> str:
    """
    增量更新用户画像

    参数：
    - food_preferences: 用户对食材的综合偏好，键为食材名，值为偏好程度（0~1）
    - cuisine_preferences: 用户对菜系的综合偏好，键为菜系名，值为偏好程度（0~1）
    - taste_preferences: 用户口味偏好，键为口味类型（spicy/sweet/salty/sour/bitter/umami），值为偏好程度（0~1）
    - ingredients: 用户当前拥有的食材清单及其生产日期和保质期
    示例：
    [
        {
            "food_type": "西红柿",
            "production_date": "2025-10-20",
            "expiration_date": "2025-10-27"
        },
        {
            "food_type": "鸡蛋",
            "production_date": "-",
            "expiration_date": "-"
        }
    ]
    - allergies: "用户过敏的食材列表"
    - diet: 用户的饮食习惯，例如 ['素食', '低糖', '高蛋白']
    以上所有参数均为必须参数，不能为空。如果不涉及，请传入默认值。
    """
    writer = runtime.stream_writer
    writer(
        f"正在更新用户画像：食物偏好={food_preferences}, 菜系偏好={cuisine_preferences}, 口味偏好={taste_preferences}, 食材清单={ingredients}, 过敏原={allergies}, 饮食偏好={diet}")

    user_id = runtime.context.user_id
    store = runtime.store

    record = store.get(("users",), user_id)
    current_data = record.value if record and record.value else {}

    updates = {}
    if food_preferences is not None:
        updates["food_preferences"] = food_preferences
    if cuisine_preferences is not None:
        updates["cuisine_preferences"] = cuisine_preferences
    if taste_preferences is not None:
        updates["taste_preferences"] = taste_preferences
    if ingredients is not None:
        updates["ingredients"] = ingredients
    if allergies is not None:
        updates["allergies"] = allergies
    if diet is not None:
        updates["diet"] = diet

    merged_data = {**current_data, **updates}

    store.put(("users",), user_id, merged_data)

    print(f"\r[update_user_info] 用户 {user_id} 更新后画像: {merged_data}", end="")
    return "用户画像已增量更新。"


@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """
    获取用户画像
    """
    writer = runtime.stream_writer
    writer("正在获取用户画像...")

    store = runtime.store
    user_id = runtime.context.user_id

    record = store.get(("users",), user_id)
    if record and record.value:
        result = f"ok: {record.value}"
    else:
        result = "用户画像不存在"

    return result
