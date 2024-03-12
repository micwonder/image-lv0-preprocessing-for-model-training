from convert import convert_files

if __name__ == "__main__":
    convert_files(
        src_dir=r"F:\Training_Data_YOLO\AMPV",
        dst_dir=r"E:\Aji",
        image_format="png",
        # image_format=None,
        out_fname_format="thermal_%d_%u",
        delete_source=False,
    )
