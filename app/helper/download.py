
import os
import tempfile
import logging

from dispatcher import bot

from mutagen import File


async def download_file(file_id, timeout=300):
    tmpdir = tempfile.TemporaryDirectory()
    path = os.path.join(tmpdir.name, file_id)
    await bot.download_file_by_id(file_id, path, timeout=timeout)

    return tmpdir, path


async def delete_tmpdir(tmpdir):
    try:
        tmpdir.cleanup()
    except Exception as e:
        logging.error(e)


async def download_audio(file_id, timeout=300):
    if not file_id:
        return None

    tmpdir, path = await download_file(file_id, timeout)

    try:
        audio = File(path)
        audio.delete()
        audio.save()
        duration = audio.info.length
    except Exception as e:
        logging.error(e)
        duration = 0

    file = open(path, 'rb')
    await delete_tmpdir(tmpdir)
    
    return file, duration


async def download_image(file_id, timeout=300):
    if not file_id:
        return None

    tmpdir, path = await download_file(file_id, timeout)
    file = open(path, 'rb')
    await delete_tmpdir(tmpdir)
    
    return file

