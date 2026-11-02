from pydantic import BaseModel, ConfigDict


class LoginIn(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"user_id": 123}],
        }
    )

    user_id: int