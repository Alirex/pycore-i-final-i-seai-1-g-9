from prompt_toolkit import HTML, choice


def yes_no_dialog(
    *,
    text: str,
    title: str | None = None,
    boolean_text: str = "Yes/No",
) -> bool:
    message = text
    if title:
        message = f"<b>{title}</b>\n{text}"

    yes, no = boolean_text.split("/")

    options = [
        (True, yes),
        (False, no),
    ]

    return choice(
        message=HTML(message),
        options=options,
    )


def yes_no_skip_dialog(
    *,
    text: str,
    title: str | None = None,
    boolean_text: str = "Yes/No",
    optional: bool = False,
    optional_text: str = "Skip",
) -> bool | None:
    message = text
    if title:
        message = f"<b>{title}</b>\n{text}"

    yes, no = boolean_text.split("/")

    options: list[tuple[bool | None, str]] = [
        (True, yes),
        (False, no),
    ]
    if optional:
        options.append((None, optional_text))

    return choice(
        message=HTML(message),
        options=options,
    )
