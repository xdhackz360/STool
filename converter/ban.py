from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from config import OWNER_ID

def is_admin(app, user_id, chat_id):
    try:
        member = app.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "owner"]
    except:
        # If user info cannot be fetched, assume admin/owner
        return True

def handle_error(message):
    message.reply_text("**❌ Looks Like I Am Not Admin Here**", parse_mode=ParseMode.MARKDOWN)

def setup_ban_handlers(app):

    @app.on_message(filters.command(["ban", "fuck"], prefixes=["/", "."]) & (filters.private | filters.group))
    def handle_ban(client, message):
        if message.chat.type == "private":
            message.reply_text("**❌ Sorry, this command only works in groups.**", parse_mode=ParseMode.MARKDOWN)
            return

        chat_id = message.chat.id
        user_id = message.from_user.id if message.from_user else None

        if user_id and not is_admin(app, user_id, chat_id) and user_id != OWNER_ID:
            message.reply_text("**❌ Sorry Bro You Are Not Admin**", parse_mode=ParseMode.MARKDOWN)
            return

        if message.reply_to_message:
            target_user = message.reply_to_message.from_user.id
            reason = " ".join(message.command[1:]) or "No reason"
        else:
            target_users = [word for word in message.command[1:] if word.startswith('@')]
            reason = " ".join([word for word in message.command[1:] if not word.startswith('@')]) or "No reason"
            if not target_users:
                message.reply_text("**❌ Please specify the username or user ID.**", parse_mode=ParseMode.MARKDOWN)
                return

        try:
            if message.reply_to_message:
                app.ban_chat_member(chat_id, target_user)
                user_info = app.get_users(target_user)
                username = user_info.username if user_info.username else user_info.first_name
                message.reply_text(
                    f"**{username} has been banned for [{reason}].** ✅",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Unban", callback_data=f"unban:{target_user}")]]
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                for target_user in target_users:
                    app.ban_chat_member(chat_id, target_user)
                    user_info = app.get_users(target_user)
                    username = user_info.username if user_info.username else user_info.first_name
                    message.reply_text(
                        f"**{username} has been banned for [{reason}].** ✅",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Unban", callback_data=f"unban:{target_user}")]]
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
        except Exception:
            handle_error(message)

    @app.on_message(filters.command(["unban", "unfuck"], prefixes=["/", "."]) & (filters.private | filters.group))
    def handle_unban(client, message):
        if message.chat.type == "private":
            message.reply_text("**❌ Sorry, this command only works in groups.**", parse_mode=ParseMode.MARKDOWN)
            return

        chat_id = message.chat.id
        user_id = message.from_user.id if message.from_user else None

        if user_id and not is_admin(app, user_id, chat_id) and user_id != OWNER_ID:
            message.reply_text("**❌ Sorry Bro You Are Not Admin**", parse_mode=ParseMode.MARKDOWN)
            return

        if message.reply_to_message:
            target_user = message.reply_to_message.from_user.id
        else:
            target_users = [word for word in message.command[1:] if word.startswith('@')]
            if not target_users:
                message.reply_text("**❌ Please specify the username or user ID.**", parse_mode=ParseMode.MARKDOWN)
                return

        try:
            if message.reply_to_message:
                app.unban_chat_member(chat_id, target_user)
                message.reply_text(f"**User {target_user} has been unbanned.** ✅", parse_mode=ParseMode.MARKDOWN)
            else:
                for target_user in target_users:
                    app.unban_chat_member(chat_id, target_user)
                    message.reply_text(f"**User {target_user} has been unbanned.** ✅", parse_mode=ParseMode.MARKDOWN)
        except Exception:
            handle_error(message)

    @app.on_callback_query(filters.regex(r"^unban:(.*)"))
    def callback_unban(client, callback_query):
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id if callback_query.from_user else None
        target_user = callback_query.data.split(":")[1]

        if user_id and not is_admin(app, user_id, chat_id) and user_id != OWNER_ID:
            callback_query.answer("**❌ Sorry Bro You Are Not Admin**", show_alert=True)
            return

        try:
            app.unban_chat_member(chat_id, target_user)
            callback_query.answer("User has been unbanned.")
            callback_query.message.edit_text(f"**User {target_user} has been unbanned.** ✅", parse_mode=ParseMode.MARKDOWN)
        except Exception:
            callback_query.answer("**❌ Looks Like I Am Not Admin Here**", show_alert=True)

    @app.on_message(filters.command(["mute"], prefixes=["/", "."]) & (filters.private | filters.group))
    def handle_mute(client, message):
        if message.chat.type == "private":
            message.reply_text("**❌ Sorry, this command only works in groups.**", parse_mode=ParseMode.MARKDOWN)
            return

        chat_id = message.chat.id
        user_id = message.from_user.id if message.from_user else None

        if user_id and not is_admin(app, user_id, chat_id) and user_id != OWNER_ID:
            message.reply_text("**❌ Sorry Bro You Are Not Admin**", parse_mode=ParseMode.MARKDOWN)
            return

        if message.reply_to_message:
            target_user = message.reply_to_message.from_user.id
            reason = " ".join(message.command[1:]) or "No reason"
        else:
            target_users = [word for word in message.command[1:] if word.startswith('@')]
            reason = " ".join([word for word in message.command[1:] if not word.startswith('@')]) or "No reason"
            if not target_users:
                message.reply_text("**❌ Please specify the username or user ID.**", parse_mode=ParseMode.MARKDOWN)
                return

        try:
            if message.reply_to_message:
                app.restrict_chat_member(chat_id, target_user, permissions=ChatPermissions(can_send_messages=False))
                user_info = app.get_users(target_user)
                username = user_info.username if user_info.username else user_info.first_name
                message.reply_text(
                    f"**{username} has been muted for [{reason}].** ✅",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Unmute", callback_data=f"unmute:{target_user}")]]
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                for target_user in target_users:
                    app.restrict_chat_member(chat_id, target_user, permissions=ChatPermissions(can_send_messages=False))
                    user_info = app.get_users(target_user)
                    username = user_info.username if user_info.username else user_info.first_name
                    message.reply_text(
                        f"**{username} has been muted for [{reason}].** ✅",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Unmute", callback_data=f"unmute:{target_user}")]]
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
        except Exception:
            handle_error(message)

    @app.on_message(filters.command(["unmute"], prefixes=["/", "."]) & (filters.private | filters.group))
    def handle_unmute(client, message):
        if message.chat.type == "private":
            message.reply_text("**❌ Sorry, this command only works in groups.**", parse_mode=ParseMode.MARKDOWN)
            return

        chat_id = message.chat.id
        user_id = message.from_user.id if message.from_user else None

        if user_id and not is_admin(app, user_id, chat_id) and user_id != OWNER_ID:
            message.reply_text("**❌ Sorry Bro You Are Not Admin**", parse_mode=ParseMode.MARKDOWN)
            return

        if message.reply_to_message:
            target_user = message.reply_to_message.from_user.id
        else:
            target_users = [word for word in message.command[1:] if word.startswith('@')]
            if not target_users:
                message.reply_text("**❌ Please specify the username or user ID.**", parse_mode=ParseMode.MARKDOWN)
                return

        try:
            if message.reply_to_message:
                app.restrict_chat_member(chat_id, target_user, permissions=ChatPermissions(can_send_messages=True,
                                                                                            can_send_media_messages=True,
                                                                                            can_send_polls=True,
                                                                                            can_send_other_messages=True,
                                                                                            can_add_web_page_previews=True))
                message.reply_text(f"**User {target_user} has been unmuted.** ✅", parse_mode=ParseMode.MARKDOWN)
            else:
                for target_user in target_users:
                    app.restrict_chat_member(chat_id, target_user, permissions=ChatPermissions(can_send_messages=True,
                                                                                                can_send_media_messages=True,
                                                                                                can_send_polls=True,
                                                                                                can_send_other_messages=True,
                                                                                                can_add_web_page_previews=True))
                    message.reply_text(f"**User {target_user} has been unmuted.** ✅", parse_mode=ParseMode.MARKDOWN)
        except Exception:
            handle_error(message)

    @app.on_callback_query(filters.regex(r"^unmute:(.*)"))
    def callback_unmute(client, callback_query):
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id if callback_query.from_user else None
        target_user = callback_query.data.split(":")[1]

        if user_id and not is_admin(app, user_id, chat_id) and user_id != OWNER_ID:
            callback_query.answer("**❌ Sorry Bro You Are Not Admin**", show_alert=True)
            return

        try:
            app.restrict_chat_member(chat_id, target_user, permissions=ChatPermissions(can_send_messages=True,
                                                                                        can_send_media_messages=True,
                                                                                        can_send_polls=True,
                                                                                        can_send_other_messages=True,
                                                                                        can_add_web_page_previews=True))
            callback_query.answer("User has been unmuted.")
            callback_query.message.edit_text(f"**User {target_user} has been unmuted.** ✅", parse_mode=ParseMode.MARKDOWN)
        except Exception:
            callback_query.answer("**❌ Looks Like I Am Not Admin Here**", show_alert=True)
