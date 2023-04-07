from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user, ban_user, get_ban_status
from configs import cfg
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif = [
    'https://graph.org/file/20f059b27bdac54432953.mp4'
]


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m : Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        img = random.choice(gif)
        await app.send_video(kk.id,img, "**Hello {}!\nYour request to join {} is approved by moderators\n\n__Powerd By : @sanusmoviesch __**".format(m.from_user.mention, m.chat.title))
        add_user(kk.id)
    except errors.PeerIdInvalid as e:
        print("user isn't start bot(means group)")
    except Exception as err:
        print(str(err))    
 
@app.on_message(filters.command("start"))
async def op(_, m :Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id) 
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://t.me/sanusmoviesch"),
                        InlineKeyboardButton("💬 group", url="https://t.me/sanusmovies")
                    ],[
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/kwicapprovalbot?startgroup")
                    ]
                ]
            )
            add_user(m.from_user.id)
            await m.reply_photo("https://graph.org/file/8d7f76a7ca1d39251aee7.jpg", caption="**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n__Powerd By : @cinema_kalavara __**".format(m.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard)



@app.on_message(filters.command("ban") & filters.user(cfg.SUDO))

async def ban(_, m : Message):

    ban = await db.get_ban_status(m.from_user)

    await message.reply(f'Sorry Dude, You are Banned to use Me. \nBan Reason: {ban["ban_reason"]}')
    
    
print("I'm Alive Now!")
app.run()
