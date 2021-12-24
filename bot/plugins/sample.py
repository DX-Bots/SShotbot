from pyrogram import filters

from bot.utils import ProcessTypes
from bot.screenshotbot import ScreenShotBot
from bot.processes import ProcessFactory
from bot.messages import Messages as ms
from bot.config import Config
from screenshotbot.bot.database.forcesub import ForceSub


@ScreenShotBot.on_callback_query(
    filters.create(lambda _, __, query: query.data.startswith("smpl"))
)
async def _(c, m):
    forcesub = await ForceSub(c, m)
    if forcesub == 400:
        return
    # c.process_pool.new_task(Utilities().sample_fn(c, m))
    try:
        await m.answer()
    except Exception:
        pass

    await m.edit_message_text(
        ms.ADDED_TO_QUEUE.format(per_user_process_count=Config.MAX_PROCESSES_PER_USER),
    )
    c.process_pool.new_task(
        (
            m.from_user.id,
            ProcessFactory(
                process_type=ProcessTypes.SAMPLE_VIDEO, client=c, input_message=m
            ),
        )
    )
