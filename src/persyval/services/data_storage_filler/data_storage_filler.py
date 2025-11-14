from typing import TYPE_CHECKING, Final

from faker import Faker

from persyval.models.contact import Contact
from persyval.services.data_actions.contact_add import contact_add
from persyval.services.data_storage.data_storage import DataStorage

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Generator

OPERATOR_CODES: Final[list[str]] = [
    "73",
    "93",
    "97",
    "98",
]


def generate_phone_number(
    faker: Faker,
) -> str:
    return "".join(
        [
            "+380",
            faker.random_element(elements=OPERATOR_CODES),
            f"{faker.random_int(min=0, max=9999999):07d}",
        ],
    )


def generate_contact(
    faker: Faker,
) -> Contact:
    return Contact(
        name=faker.name(),
        address=faker.address() if faker.boolean() else None,
        birthday=faker.date_of_birth(minimum_age=1, maximum_age=100) if faker.boolean() else None,
        phones=[generate_phone_number(faker) for _ in range(faker.random_int(min=0, max=10))],
        emails=[faker.email() for _ in range(faker.random_int(min=0, max=10))],
    )


def generate_contacts(
    amount: int,
    faker: Faker,
) -> Generator[Contact]:
    for _ in range(amount):
        yield generate_contact(faker)


def fill_data_storage_by_path(
    *,
    storage_dir: pathlib.Path | None = None,
    amount: int = 10,
    init_only: bool = False,
) -> None:
    with DataStorage.load(
        dir_path=storage_dir,
    ) as data_storage:
        fill_data_storage(
            data_storage=data_storage,
            amount=amount,
            init_only=init_only,
        )


def fill_data_storage(
    *,
    data_storage: DataStorage,
    amount: int = 10,
    init_only: bool = False,
) -> None:
    faker = Faker("uk_UA")

    if init_only and data_storage.data.contacts:
        print("Contacts already exists. Skipping.")
    else:
        for contact in generate_contacts(amount, faker):
            contact_add(
                data_storage=data_storage,
                contact=contact,
            )

    for info in data_storage.get_stats():
        print(info)
