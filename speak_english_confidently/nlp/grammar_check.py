import language_tool_python
class GrammarChecker:
    def __init__(self):
        self.tool = language_tool_python.LanguageTool("en-US")
    def check_grammar(self, text):
        matches = self.tool.check(text)
        return {"errors": len(matches), "suggestions": [str(m) for m in matches]}
