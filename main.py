from convert import convert_files

if __name__ == "__main__":
  convert_files(
    src_dir=r"E:\Ajin",
    dst_dir=r"E:\Aji",
    image_format="png",
    out_fname_format="thermal_%d_%u",
    delete_source=False
  )
