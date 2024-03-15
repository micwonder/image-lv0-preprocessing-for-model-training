import uuid
import os
import datetime
import imageio.v3 as iio
from logger import Logger
from shutil import copyfile
from tqdm import tqdm


def convert_files(
    src_dir: str,
    dst_dir: str = None,
    image_format: str = None,
    out_fname_format: str = "%d_%u",
    delete_source: bool = False,
    logger: Logger = Logger(),
):
    """Convert filenames of every images to uuid format.

    ### Function Arguments:
     - src_dir: absolute path of source directory
     - dst_dir `optional`: absolute path of destination directory; default = `src_dir`
     - image_format `optional`: format of output image; defaults to save original format
     - out_fname_format `optional`: template string for output image filename; defaults to `%d_%u`; `%u`: `uuid_v4`; `%d`: `timestamp`
     - delete_source `optional`: delete source images; defaults to `False`
     - logger `optional`: Logger for errors; default save logs to file

    ### Sample Usage:

    ```python
    convert_files(
      src_dir="C:/Users/Admin/Pictures/sample",
      dst_dir="c:/users/admin/pictures/normalized",
      image_format="png",
      out_fname_format="thermal_%d_%u",
      delete_source=False
    )
    ```
    """
    dst_dir = dst_dir or src_dir
    os.makedirs(dst_dir, exist_ok=True)
    src_dir = src_dir

    total_file_count, success_count, skipped_count, written_count, copied_count = (
        0,
        0,
        0,
        0,
        0,
    )
    file_count = sum(len(files) for _, _, files in os.walk(src_dir))

    with tqdm(
        total=file_count,
        desc="Copying files" if not image_format else "Imwriting files",
    ) as pbar:
        for subdir, _, files in os.walk(src_dir):
            for filename in files:
                src_path = os.path.join(subdir, filename)
                if not os.path.isfile(src_path):
                    continue

                _, src_ext = os.path.splitext(filename)
                dst_ext = f".{image_format}" if image_format else src_ext
                dst_filename = out_fname_format.replace(
                    "%u", str(uuid.uuid4())
                ).replace("%d", str(datetime.datetime.now().timestamp()))
                dst_filename += dst_ext

                updated_src = os.path.join(subdir, dst_filename)
                relative_path = os.path.relpath(updated_src, src_dir)
                dst_path = os.path.join(dst_dir, relative_path)

                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                total_file_count += 1
                pbar.update(1)

                determine_format = image_format
                if src_ext == image_format:
                    determine_format = None

                if determine_format:
                    try:
                        img = iio.imread(src_path)
                        iio.imwrite(dst_path, img)
                        written_count += 1
                        if delete_source:
                            os.remove(src_path)
                    except Exception as e:
                        logger.error(f"Error processing image {src_path}: {e}")
                        skipped_count += 1
                        continue

                else:
                    try:
                        if delete_source:
                            os.rename(src_path, dst_path)
                        else:
                            copyfile(src_path, dst_path)
                        copied_count += 1
                    except:
                        logger.error(
                            f"Error copying file from {src_path} to {dst_path}: {e}"
                        )
                        continue

                success_count += 1

    message = f"Converted {success_count} images among {total_file_count} files. {skipped_count} files skipped. {written_count} files written {copied_count} files copied."
    logger.info(message)
    print(message)
