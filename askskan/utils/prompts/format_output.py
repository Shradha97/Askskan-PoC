from pydantic import BaseModel, Field


class FormatCodeOutput(BaseModel):
    Query: str = Field(description="The generated Spark SQL query")
    Code: str = Field(description="Python code generated to run the Spark SQL query")
    Skan_Bot: str = Field(
        description="The final answer printed by the python code in a friendly tone. Place the answer between ##"
    )


class FormatDoubtOutput(BaseModel):
    Doubt: str = Field(description="The clarification point asked by the bot")


class FormatFallbackOutput(BaseModel):
    Fallback: str = Field(description="The fallback message in case of any error")
