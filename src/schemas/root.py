from pydantic import BaseModel, ConfigDict


class RootOut(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"message": "Hello World"}],
        }
    )

    message: str
