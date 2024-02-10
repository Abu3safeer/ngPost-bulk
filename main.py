from pathlib import Path

COMMAND = [
    'ngPostv4.16.1_x64/ngPost.exe',
    '-i',
    'files\%%~nxf',
    '-o',
    'nzb\%%~nxf.nzb',
    '-c',
    'ngPostv4.16.1_x64/ngPost.conf',
    '--gen_par2'
]
DELETE = True
main_path = Path('C:/Users/Abu3safeerPC/Documents/apps/ngPost')
files_path = main_path / 'files'
nzb_path = main_path / 'nzb'


def delete_with_parent(path: Path):
    parent = Path(path.parent)  # store the parent to use it later

    # This checks if the path is files path, then ignore it
    if path == files_path:
        pass

    elif path.is_file():  # check if the path is a file
        path.unlink()  # delete the file
        if not any(parent.iterdir()):  # check if parent folder is empty
            delete_with_parent(parent)  # call the function again to delete the parent folder

    elif path.is_dir():  # check if the path is folder
        if not any(path.iterdir()):  # Check if the folder is empty
            path.rmdir()  # delete the empty folder
            if not any(parent.iterdir()):  # check if parent folder is empty
                delete_with_parent(parent)  # call the function again to delete the parent folder


def run():

    # Note: There is a weired behavior when iterate on glob result, returns an error when iterating
    # on the last file, so as a workaround it will be appended on a list, then process it from there
    files_glob = files_path.glob('**/*')
    files = []
    for file in files_glob:
        if file.exists():
            files.append(file)

    # Start processing the files
    for file in files:
        if file.exists():  # Check if the file exists, just in case some files deleted by user or other ways
            if file.is_file():  # Check if the file is actually a file, not a directory or folder
                print('processing ', file)

                # If file deletion is enabled
                if DELETE:
                    delete_with_parent(file)  # Delete the file, and delete container folder if empty

            # This is useful for deleting empty folders, it will work only if folder is empty,
            # otherwise it does not do anything.
            elif file.is_dir():
                delete_with_parent(file)


if __name__ == '__main__':

    run()


