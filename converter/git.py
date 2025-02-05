import requests
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

# ThreadPoolExecutor instance
executor = ThreadPoolExecutor(max_workers=5)  # You can adjust the number of workers

def fetch_repo_info(url):
    api_url = url.replace("https://github.com/", "https://api.github.com/repos/")
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception("❌ Invalid GitHub URL or repository not found.")
    return response.json()

def fetch_repo_branches(url):
    api_url = url.replace("https://github.com/", "https://api.github.com/repos/")
    branches_url = f"{api_url}/branches"
    response = requests.get(branches_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch branches.")
    branches = response.json()
    return [branch['name'] for branch in branches]

def download_repo(repo_info, branch):
    download_url = f"https://github.com/{repo_info['full_name']}/archive/refs/heads/{branch}.zip"
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        zip_file_path = f"{repo_info['name']}.zip"
        with open(zip_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return zip_file_path
    else:
        raise Exception("❌ Failed to download the repository. Please check the URL and branch name.")

async def handle_git_command(client, message, url, branch):
    downloading_message = await message.reply_text(
        "<b>⚡️ Downloading GitHub Repository From URL...⌛️</b>",
        parse_mode=ParseMode.HTML
    )
    try:
        loop = asyncio.get_event_loop()
        repo_info = await loop.run_in_executor(executor, fetch_repo_info, url)
        zip_file_path = await loop.run_in_executor(executor, download_repo, repo_info, branch)
        branches = await loop.run_in_executor(executor, fetch_repo_branches, url)

        await downloading_message.delete()

        await message.reply_document(
            document=zip_file_path,
            caption=(
                "<b>Repository Details</b>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"<b>User:</b> <code>{repo_info['owner']['login']}</code>\n"
                f"<b>Repo Name:</b> <code>{repo_info['name']}</code>\n"
                f"<b>Forks Count:</b> <code>{repo_info['forks_count']}</code>\n"
                f"<b>Repo URL:</b> <code>{repo_info['html_url']}</code>\n"
                f"<b>Description:</b> <code>{repo_info['description']}</code>\n"
                f"<b>Downloaded Branch:</b> <code>{branch}</code>\n"
                f"<b>Available Branches:</b> <code>{', '.join(branches)}</code>"
            ),
            parse_mode=ParseMode.HTML
        )

        os.remove(zip_file_path)
    except Exception as e:
        await downloading_message.edit_text(
            f"<b>Sorry Bro! Wrong URL or Repo Not Found ❌</b>\n<b>Error:</b> {str(e)}",
            parse_mode=ParseMode.HTML
        )

def setup_git_handler(app: Client):
    @app.on_message(filters.command(["git"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def git_command(client, message):
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply_text(
                "<b>❌ Provide a GitHub repository URL after the command.</b>",
                parse_mode=ParseMode.HTML
            )
            return

        url = command_parts[1]
        # Ensure the URL is correct
        if not url.startswith("https://"):
            url = "https://" + url
        branch = command_parts[2] if len(command_parts) > 2 else "main"

        # Run the handle_git_command in the background to handle multiple requests simultaneously
        asyncio.create_task(handle_git_command(client, message, url, branch))
