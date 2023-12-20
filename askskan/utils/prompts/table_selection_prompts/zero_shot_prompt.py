from app.configurations.development.settings import TABLE_SELECTION_PROMPT

zero_shot_prompt = open(
    TABLE_SELECTION_PROMPT,
    "r",
).read()
