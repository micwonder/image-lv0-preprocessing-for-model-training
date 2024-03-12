import uuid
import os
import datetime
import imageio.v3 as iio
from logger import Logger
from shutil import copyfile
from tqdm import tqdm


def convert_files(
    src_dir: str,
    dst_dir: str = "",
    image_format: str = "",
    out_fname_format: str = "%d_%u",
    delete_source: bool = False,
    logger: Logger = Logger(),
):
    """Convert filenames of every images to uuid format.

    ### Function Arguments:
     - root_dir: absolute path of source directory
     - dst_dir `optional`: absolute path of destination directory; default = `root_dir`
     - image_format `optional`: format of output image; defaults to save original format
     - out_fname_format `optional`: template string for output image filename; defaults to `%d_%u`; `%u`: `uuid_v4`; `%d`: `timestamp`
     - delete_source `optional`: delete source images; defaults to `False`
     - logger `optional`: Logger for errors; default save logs to file

    ### Sample Usage:

    ```python
    convert_files(
      root_dir="C:/Users/Admin/Pictures/sample",
      dst_dir="c:/users/admin/pictures/normalized",
      image_format="png",
      out_fname_format="thermal_%d_%u",
      delete_source=False
    )
    ```
    """
    root_dir = src_dir

    if not root_dir or not os.path.exists(root_dir) or not os.path.isdir(root_dir):
        return logger.error(f"Cannot read {root_dir}")

    if not dst_dir:
        dst_dir = root_dir

    if not os.path.exists(dst_dir):
        logger.info(f"Directory {dst_dir} created.")
        os.mkdir(dst_dir)

    tot_filecnt, success_cnt, skipped_cnt = 0, 0, 0

    cpt = sum([len(files) for _, _, files in os.walk(root_dir)])

    # for filename in os.listdir(root_dir):
    with tqdm(
        total=cpt, desc="Copying files" if not image_format else "Imwriting files"
    ) as pbar:
        for subdir, dirs, files in os.walk(root_dir):
            for filename in files:
                _, src_ext = os.path.splitext(filename)
                dst_ext = "." + image_format if image_format else src_ext

                # src = root_dir + "\\" + filename
                src = os.path.join(subdir, filename)
                dst_filename = out_fname_format.replace(
                    "%u", str(uuid.uuid4())
                ).replace("%d", str(datetime.datetime.now().timestamp()))
                dst_filename += dst_ext
                updated_src = os.path.join(subdir, dst_filename)
                relative_path = os.path.relpath(updated_src, root_dir)
                dst = os.path.join(dst_dir, relative_path)

                if not os.path.isfile(src):
                    continue

                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(dst), exist_ok=True)

                tot_filecnt += 1
                pbar.update(1)

                if image_format:
                    try:
                        img = iio.imread(src)
                    except:
                        logger.error(f"{src} is not an image. skipped")
                        skipped_cnt += 1
                        continue

                    try:
                        iio.imwrite(dst, img)
                    except:
                        logger.error(f"Error saving image to {dst}.")
                        continue

                    if delete_source:
                        try:
                            os.remove(src)
                        except:
                            logger.error(f"Error removing {src}")

                else:
                    try:
                        if delete_source:
                            os.rename(src, dst)
                        else:
                            copyfile(src, dst)
                    except:
                        logger.error(f"Error handling file {src} to {dst}")

                success_cnt += 1

    message = f"Converted {success_cnt} images among {tot_filecnt} files. {skipped_cnt} files skipped."
    logger.info(message)
    print(message)
