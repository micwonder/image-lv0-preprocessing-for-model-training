# Image preprocessing for the AI model training

## Features
- Convert filenames of every images to certain format based on time and uuid
- Convert different format of images (e.g. jpeg, png, webp) to other format
- Logging errors to log files

## v1 Function Arguments:
- src_dir: absolute path of source directory
- dst_dir `optional`: absolute path of destination directory; default = `src_dir`
- image_format `optional`: format of output image; defaults to save original format
- out_fname_format `optional`: template string for output image filename; defaults to `%d_%u`; `%u`: `uuid_v4`; `%d`: `timestamp`
- delete_source `optional`: delete source images; defaults to `False`
- logger `optional`: Logger for errors; default save logs to file

## Sample Usage:

```python
convert_files(
  src_dir=r"E:\Ajin",
  dst_dir=r"E:\Aji",
  image_format="png",
  out_fname_format="optical_%d_%u",
  delete_source=False
)
```

## v2 updates
os.walk() to iterate through the subdirectories