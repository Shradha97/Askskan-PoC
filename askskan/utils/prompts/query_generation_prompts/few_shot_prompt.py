from app.configurations.development.settings import (
    FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA_FILE,
    FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA_FILE,
    FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA_FILE,
    FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA_FILE,
    MULTITABLE_FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA_FILE,
    MULTITABLE_FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA_FILE,
    MULTITABLE_FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA_FILE,
    MULTITABLE_FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA_FILE,
)

few_shot_prompt_with_additional_instruction_with_persona = open(
    FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA_FILE,
    "r",
).read()

few_shot_prompt_without_additional_instruction_with_persona = open(
    FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA_FILE,
    "r",
).read()


few_shot_prompt_with_additional_instruction_without_persona = open(
    FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA_FILE,
    "r",
).read()


few_shot_prompt_without_additional_instruction_without_persona = open(
    FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA_FILE,
    "r",
).read()

multitable_few_shot_prompt_with_additional_instruction_with_persona = open(
    MULTITABLE_FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA_FILE,
    "r",
).read()

multitable_few_shot_prompt_without_additional_instruction_with_persona = open(
    MULTITABLE_FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA_FILE,
    "r",
).read()


multitable_few_shot_prompt_with_additional_instruction_without_persona = open(
    MULTITABLE_FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA_FILE,
    "r",
).read()

multitable_few_shot_prompt_without_additional_instruction_without_persona = open(
    MULTITABLE_FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA_FILE,
    "r",
).read()
