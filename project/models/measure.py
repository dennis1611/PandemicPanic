"""
File that contains the Measure class.
"""


class Measure:
    """
    Class that contains all aspects of a measure that can be taken.
    """

    def __init__(self, number, name, desc, factor, active=False):
        self.number = number
        self.name = name
        self.desc = desc
        self.factor = factor
        self.active = active

    def __str__(self):
        """"Return a human readable string."""
        return f"#{self.number}| {self.active}| {self.name}: {self.desc}"

    def __repr__(self):
        """"Return a string to display in the visual mode."""
        return f"{self.number} {self.name}: {self.desc}"

    def menu(self):
        """"Print the description of the measure for the player."""
        print(f"{str(self)}")

    def is_active(self):
        """Returns the active status T|F of the measure."""
        return self.active

    def update_return_factor(self):
        """Switches the measure status and returns the correct effect factor."""
        if not self.active:
            effect = self._activate_return_factor()
        elif self.active:
            effect = self._deactivate_return_factor()
        return effect

    def _activate_return_factor(self):
        """Helper function for update_return_factor -> activates."""
        self.active = True
        effect = self.factor
        return effect

    def _deactivate_return_factor(self):
        """Helper function for update_return_factor -> deactivates."""
        self.active = False
        effect = 1 / self.factor
        return effect
