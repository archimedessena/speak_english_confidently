import pytest
from conversation.state_manager import ConversationState
from conversation.feedback_engine import generate_feedback

def test_state_update():
    state = ConversationState()
    state.update("test", "response", "feedback")
    assert len(state.history) == 1

def test_generate_feedback():
    feedback = generate_feedback("test", ["fix"], 50, 160, [1.0])
    assert "Slow down" in feedback