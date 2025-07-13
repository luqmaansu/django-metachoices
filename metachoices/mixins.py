class MetaChoiceMixin:
    """Mixin to provide meta choices functionality to field classes."""

    def __init__(self, *args, choices=None, **kwargs):
        """Initialize the meta choices functionality.

        Args:
            *args: Positional arguments for the field.
            choices: Can be either:
                - Standard Django format: [(key, display), ...]
                - Enhanced meta format: {key: {"display": "...", "attr": "..."}, ...}
            **kwargs: Additional keyword arguments for the field.
        """
        # Parse choices and detect format
        self.meta_choices = {}
        processed_choices = []

        if choices:
            if isinstance(choices, dict):
                # Enhanced meta format: {key: {"display": "...", ...}, ...}
                self.meta_choices = choices

                # Convert to Django's standard choices format
                processed_choices = [
                    (k, v.get("display", k) if isinstance(v, dict) else v)
                    for k, v in choices.items()
                ]
            elif isinstance(choices, list | tuple):
                # Standard Django format: [(key, display), ...]
                processed_choices = choices
                # Convert to meta_choices format for getter methods
                self.meta_choices = {k: {"display": v} for k, v in choices}

        # Set the processed choices
        if processed_choices:
            kwargs["choices"] = processed_choices

        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        """Add dynamic getter methods to the model class."""
        super().contribute_to_class(cls, name, private_only=private_only)

        # Add getter methods for each unique attribute in meta_choices
        if self.meta_choices:
            # Find all unique attributes across all choices
            all_attrs = set()
            for choice_data in self.meta_choices.values():
                if isinstance(choice_data, dict):
                    all_attrs.update(choice_data.keys())

            # Create a getter method for each attribute
            for attr in all_attrs:
                method_name = f"get_{name}_{attr}"
                method = self._make_getter_method(name, attr)
                setattr(cls, method_name, method)

    def _make_getter_method(self, field_name, attr):
        """Create a getter method for a specific attribute."""

        def getter(model_instance):
            value = getattr(model_instance, field_name)

            # Try to find the value in meta_choices
            choice_data = None
            if value in self.meta_choices:
                choice_data = self.meta_choices[value]
            else:
                # If not found, try converting the value to match original key types
                for original_key in self.meta_choices.keys():
                    try:
                        # Try to convert the stored string
                        # value back to the original key type
                        if str(original_key) == str(value):
                            choice_data = self.meta_choices[original_key]
                            break
                    except (ValueError, TypeError):
                        continue

            if choice_data and isinstance(choice_data, dict):
                return choice_data.get(attr, None)

            # For 'display' attribute, fall back to Django's default behavior
            if attr == "display":
                # Return the value itself if not found in meta_choices
                # (Django's default)
                return value

            return None

        return getter
