class OverviewValidator:
    @staticmethod
    def validate_circular_progress(plan):
        errors = []
        if not isinstance(plan, str):
            errors.append("Plan must be a string.")
        # Add more validation rules as needed
        return errors
