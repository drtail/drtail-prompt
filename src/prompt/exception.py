class DrTailPromptBaseException(Exception):
    pass


class PromptValidationError(DrTailPromptBaseException):
    pass


class PromptVersionMismatchError(DrTailPromptBaseException):
    pass
