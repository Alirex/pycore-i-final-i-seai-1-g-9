from persyval.models.contact import (
    ContactUid,
)
from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.data_actions.contact_delete import contact_delete
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message, render_good_message


class ContactDeleteIArgs(HandlerArgsBase):
    uid: ContactUid
    force: bool | None = None


CONTACT_DELETE_I_ARGS_CONFIG = ArgsConfig[ContactDeleteIArgs](
    result_cls=ContactDeleteIArgs,
    args=[
        ArgMetaConfig(
            name="uid",
            required=True,
        ),
        ArgMetaConfig(
            name="force",
            type_=ArgType.BOOL,
            required=True,
            allow_input_on_empty=True,
            alternative_text="Are you sure you want to delete this contact?",
            boolean_text="Yes/No",
        ),
    ],
)


class ContactDeleteIHandler(
    HandlerBase[ContactDeleteIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ContactDeleteIArgs]:
        return CONTACT_DELETE_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ContactDeleteIArgs) -> None:
        if not parsed_args.force:
            render_canceled_message(
                self.console,
                "Contact remove operation cancelled by user.",
            )
            return

        # ---

        contact = contact_delete(data_storage=self.data_storage, contact_uid=parsed_args.uid)

        render_good_message(
            self.console,
            f"Contact '{contact.name}' ({contact.uid}) has been deleted.",
        )

        return
