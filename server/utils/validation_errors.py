from rest_framework.exceptions import ValidationError


class RegisterValidation:
    @staticmethod
    def format_validation_error(ve: ValidationError) -> str:
        errors = ve.detail
        error_message = "Invalid input."

        if "email" in errors:
            for err in errors["email"]:
                if err.code == "unique":
                    return "Account already exists."
                elif err.code in ["required", "blank"]:
                    return "Email is required."
                else:
                    return str(err)

        if "password" in errors:
            for err in errors["password"]:
                if err.code == "min_length":
                    return "Password is too short."
                elif err.code in ["required", "blank"]:
                    return "Password is required."
                else:
                    return str(err)

        return error_message
