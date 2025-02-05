from pyrogram import Client
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ParseMode

def setup_alive_handler(app: Client):
    @app.on_chat_member_updated()
    async def member_status_change(client: Client, chat_member_updated: ChatMemberUpdated):
        chat_id = chat_member_updated.chat.id
        new_member = chat_member_updated.new_chat_member
        old_member = chat_member_updated.old_chat_member

        # Check if the bot is added to the group as a member or admin
        if new_member and new_member.user.is_self:
            if new_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]:
                await client.send_message(
                    chat_id,
                    "**Thank You For Adding Me In This Group! 👨‍💻**\n\n"
                    "**I'm here to assist you with various tasks and make your group experience better. "
                    "Feel free to explore my features and let me know if you need any help! 😊**",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("➕ Add Me", url="https://t.me/ItsSmartToolBot?startgroup=new&admin=post_messages+delete_messages+edit_messages+pin_messages+change_info+invite_users+promote_members"),
                         InlineKeyboardButton("My Dev👨‍💻", user_id=7303810912)]
                    ])
                )

        # Check if a user joined the group
        if new_member and new_member.status == ChatMemberStatus.MEMBER:
            if not new_member.user.is_self:
                await client.send_message(
                    chat_id,
                    f"**🎉 Welcome [{new_member.user.first_name}](tg://user?id={new_member.user.id}) to the group!**\n\n"
                    "**We're thrilled to have you here! Feel free to introduce yourself and let us know how we can assist you. 😊**",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("➕ Add Me", url="https://t.me/ItsSmartToolBot?startgroup=new&admin=post_messages+delete_messages+edit_messages+pin_messages+change_info+invite_users+promote_members"),
                         InlineKeyboardButton("My Dev👨‍💻", user_id=7303810912)]
                    ])
                )

        # Check if a user left the group
        if old_member and new_member:
            if old_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR] and new_member.status == ChatMemberStatus.LEFT:
                if not old_member.user.is_self:
                    await client.send_message(
                        chat_id,
                        f"**😢 [{old_member.user.first_name}](tg://user?id={old_member.user.id}) has left the group.**",
                        parse_mode=ParseMode.MARKDOWN
                    )
