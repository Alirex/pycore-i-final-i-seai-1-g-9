from prompt_toolkit import HTML, choice


def yes_no_dialog(
    title: str,
    text: str,
) -> bool:
    return choice(
        # message=f"{title}\n{text}",
        message=HTML(f"<b>{title}</b>\n{text}"),
        options=[
            (True, "Yes"),
            (False, "No"),
        ],
    )
