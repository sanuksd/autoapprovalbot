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
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/sanufilterv1_bot?startgroup")
                    ]
                ]
            )
            add_user(m.from_user.id)
            await m.reply_photo("https://graph.org/file/8d7f76a7ca1d39251aee7.jpg", caption="**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n__Powerd By : @cinema_kalavara __**".format(m.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard)

        elif m.chat.type == enums.ChatType.GROUP or enums.ChatType.SUPERGROUP:
            keyboar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/sanufilterv1_bot?start=start")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text("**🦊 Hello {}!\nwrite me private for more details**".format(m.from_user.first_name), reply_markup=keyboar)
        print(m.from_user.first_name +" Is started Your Bot!")

    except UserNotParticipant:
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🍀 Check Again 🍀", "chk")
                ]
            ]
        )
        await m.reply_text("**⚠️Access Denied!⚠️\n\nPlease Join @{} to use me.If you joined click check again button to confirm.**".format(cfg.FSUB), reply_markup=key)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb : CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://t.me/sanusmoviesch"),
                        InlineKeyboardButton("💬 group", url="https://t.me/sanusmovies")
                    ],[
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/sanufilterv1_bot?startgroup")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit("**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n__Powerd By : @cinema_kalavara __**".format(cb.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard, disable_web_page_preview=True)
        print(cb.from_user.first_name +" Is started Your Bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined to channel join and try again. 🙅‍♂️")

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")


print("I'm Alive Now!")
app.run()
