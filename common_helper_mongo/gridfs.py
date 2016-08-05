def overwrite_file(fs, file_name, binary):
    """
    overwrite a file by name in gridfs

    :param fs: gridFS instance
    :type fs: gridFS
    :param file_name: file to overwrite
    :type file_name: str
    :param mongo_curser: MongoDB curser
    :type mongo_curser: mongo_db_curser
    :return: None
    """
    original_file = fs.find_one({'filename': file_name})
    if original_file is not None:
        fs.delete(original_file._id)
    fs.put(binary, filename=file_name)
