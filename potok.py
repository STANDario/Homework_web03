import os
from pathlib import Path
from threading import Thread
import concurrent.futures
from rich import print as rprint


while True:
    user_input = input("Напишіть шлях до папки: ")
    p = Path(user_input)
    if p.exists():
        break
    else:
        rprint("\n[red]Такого шляху не існує, перевірте ще раз :([red]\n")


expansion = {
    "images": [".JPEG", ".PNG", ".JPG", ".SVG"],
    "video": [".AVI", ".MP4", ".MOV", ".MKV"],
    "documents": [".DOC", ".DOCX", ".TXT", ".PDF", ".XLSX", ".PPTX"],
    "audio": [".MP3", ".OGG", ".WAV", ".AMR"],
    "archives": [".ZIP", ".GZ", ".TAR"]
}


general_list_folder = []
list_files = []


def first_attempt(p: Path):
    for el in p.iterdir():
        if el == p:
            continue
        if el.is_dir():
            general_list_folder.append(el)
        else:
            list_files.append(el)


def another_attempt(folder: Path):
    for el in folder.iterdir():
        if el.is_dir():
            another_attempt(el)
        else:
            list_files.append(el)


def create_folder(p: Path):
    folder_names = [p/"images", p/"video", p/"documents", p/"audio", p/"archives", p/"unknown"]
    for folder in folder_names:
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass


def add_to_folder(file):

        suf = file.suffix.upper()

        if suf in expansion.get("images"):
            images = p / "images"
            os.rename(file, images / file.name)

        elif suf in expansion.get("video"):
            video = p / "video"
            os.rename(file, video / file.name)

        elif suf in expansion.get("documents"):
            doc = p / "documents"
            os.rename(file, doc / file.name)

        elif suf in expansion.get("audio"):
            audio = p / "audio"
            os.rename(file, audio / file.name)
            print("Audio")

        elif suf in expansion.get("archives"):
            arch = p / "archives"
            os.rename(file, arch / file.name)

        else:
            unknown = p / "unknown"
            os.rename(file, unknown / file.name)


def del_folder(path):

    for i in path.iterdir():
        if i.name == "archives":
            continue
        try:
            del_folder(i)
            os.rmdir(i)
        except:
            pass


if __name__ == "__main__":

    first_th = Thread(target=first_attempt, args=(p, ))
    first_th.start()
    first_th.join()

    while True:
        if len(general_list_folder) == 1:
            another_th = Thread(target=first_attempt, args=(general_list_folder[0], ))
            general_list_folder = []
            another_th.start()
            another_th.join()
        else:
            break

    else_thread = []
    for folder in general_list_folder:
        th = Thread(target=another_attempt, args=(folder, ))
        th.start()
        else_thread.append(th)
    [thread.join() for thread in else_thread]

    create_folder(p)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(add_to_folder, list_files)

    delete_th = Thread(target=del_folder, args=(p, ))
    delete_th.start()
    delete_th.join()

    try:
        os.rmdir(p / "archives")
    except OSError:
        pass

    rprint("\n[green]Ваша папка відсортована, вітаю :)[green]\n")
