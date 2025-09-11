"""Logout command"""

from termcolor import colored

from tecli import auth, config


def run(all_sessions=False):
    """Logout command"""

    if all_sessions:
        # Logout from all sessions using the logout-all endpoint
        response = auth.make_authenticated_request(
            "POST", config.get("url_api") + "/auth/logout-all"
        )

        if response is None:
            print(colored("Authentication failed. Already logged out.", "yellow"))
        elif response.status_code == 200:
            print(colored("Successfully logged out from all sessions.", "green"))
        else:
            print(colored("Error logging out from all sessions.", "red"))
            return False
    else:
        # Logout from current session only
        response = auth.make_authenticated_request("POST", config.get("url_api") + "/auth/logout")

        if response is None:
            print(colored("Authentication failed. Already logged out.", "yellow"))
        elif response.status_code == 200:
            print(colored("Successfully logged out.", "green"))
        else:
            print(colored("Error logging out.", "red"))
            return False

    # Clear local tokens
    config.unset("JWT", "")
    config.unset("refresh_token", "")
    config.unset("token_expires_at", "")

    return True
