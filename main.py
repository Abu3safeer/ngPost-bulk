from pathlib import Path
import subprocess

# Windows Command for reference
# "ngPostv4.16.1_x64\ngPost.exe" -i "files\%%~nxf" -o "nzb\%%~nxf.nzb" -c "ngPostv4.16.1_x64\ngPost.conf" --gen_par2

DELETE = True  # Delete files after complete
main_path = Path()
files_path = main_path / 'files'
nzb_path = main_path / 'nzb'
ngPost_exe = main_path / 'ngPostv4.16.1_x64/ngPost.exe'
ngPost_conf = main_path / 'ngPostv4.16.1_x64/ngPost.conf'


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
    # on the last file, so as a workaround it will be appended on a list, then process the list
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
                relative_file_path = file.relative_to(files_path)
                source_file_path = files_path / relative_file_path
                nzb_file_path = nzb_path / relative_file_path.with_name(relative_file_path.name + '.nzb')

                # If nzb folder is not created, then create the whole tree
                if not nzb_file_path.parent.exists():
                    nzb_file_path.parent.mkdir(parents=True, exist_ok=True)

                COMMAND = [
                    f'{ngPost_exe}',
                    '-i',
                    f'{source_file_path}',
                    '-o',
                    f'{nzb_file_path}',
                    '-c',
                    f'{ngPost_conf}',
                    '--gen_par2'
                ]
                subprocess.run(COMMAND)

                # If file deletion is enabled
                if DELETE:
                    delete_with_parent(file)  # Delete the file, and delete container folder if empty

            # This is useful for deleting empty folders, it will work only if folder is empty,
            # otherwise it does not do anything.
            elif file.is_dir():
                delete_with_parent(file)


if __name__ == '__main__':

    run()
    input('Press Enter to exit....')

