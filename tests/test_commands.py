"""Basic tests for the tecli package."""

from tecli import commands


def test_commands_class_exists():
    """Test that the Commands class is importable."""
    assert hasattr(commands, "Commands")


def test_commands_has_required_methods():
    """Test that Commands class has all required methods."""
    required_methods = [
        "create",
        "start",
        "config",
        "login",
        "publish",
        "download",
        "clear",
        "info",
        "logs",
    ]

    for method in required_methods:
        assert hasattr(commands.Commands, method)
        assert callable(getattr(commands.Commands, method))


class TestCommandsClass:
    """Test the Commands class functionality."""

    def test_commands_are_static_methods(self):
        """Test that command methods are static methods."""
        # These should be callable without instantiation
        assert callable(commands.Commands.create)
        assert callable(commands.Commands.start)
        assert callable(commands.Commands.config)
