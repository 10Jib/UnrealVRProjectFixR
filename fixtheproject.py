import pathlib
import os
import shutil
import argparse
import stat

from sys import argv

def list_files(startpath, testpath):
    errCount, repCount, cpCount = 0, 0, 0
    tocopy = []
    for root, dirs, files in os.walk(startpath):
        root = pathlib.Path(root)
        parts = list(root.parts)
        dir = "/".join(parts[1:])

        dstpth = testpath / "/".join(parts[1:])

        if not dstpth.exists():
            print(f"\n!!! Target folder does not exist {str(dstpth)}")
            print("\t Skipping Folder...\n")
            continue

            """print(f"\n!!! Target folder is read only {str(dstpth)}")
            print("\t Attempting Fix...\n")
            os.chmod(dstpth, stat.S_IWUSR)  # this probably wont work lmao """

        for f in files: 
            tocopy.append(dir + '/' + f)
            srcpath = root / f
            filepth = dstpth / f

            try:
                verbose_copy(srcpath, filepth)
            except Exception as e:
                print(f"\n\n \t ERROR")
                print(f"Failed to copy{str(srcpath)} to {str(filepth)}")
                print(f"\nException Type: {e}")
                print("\nMake sure folders are not read only")
                quit()

    # code that I probably wont ever need again
        """ for path in tocopy:
            if path[0] == '/':
                path = path[1:]

            srcpath = startpath / path
            dstpath = testpath / path
            verbose_copy(srcpath, dstpath) """

def verbose_copy(srcpath, dstpth):  # check if file exists, delete, replace
    if dstpth.exists():
        print('Replacing\n {!r}\n to {!r}'.format(str(srcpath), str(dstpth)))
        os.remove(dstpth)  # This will fail if project is read-only
        
    else:
        print('copying\n {!r}\n to {!r}'.format(str(srcpath), str(dstpth)))
        
    # make sure parent folders exist or else FileNotFoundError
    return shutil.copy2(srcpath, dstpth)

def check_target(target):
    target.exists()

def check_source(source):
    source.exists()

def main():
    """ parser = argparse.ArgumentParser(
        description='This programm should fix the unreal project by replacing the core files',
    )
    parser.add_argument('-f', action='store_false',
                    default=True,
                    dest='boolean_f',
                    help='Set a switch to false')
    
    opt = parser.parse_args()
    
    baseproject = pathlib.Path('BaseVRProject')
    targetproject = pathlib.Path('John/FacefinderAndData3') #targetproject = pathlib.Path('FacefinderAndDataFD') """


    if len(argv) <2 or len(argv) > 3:
        print("incorrect input")
        print("python fixtheproject.py {unrealfile\}")
        print("\n-or-")
        print("python fixtheproject.py {baseproject\} {unrealfile\}")
        quit()

    elif len(argv) == 2:
        baseproject = pathlib.Path('BaseVRProject')
        targetproject = pathlib.Path(argv[-1])

    elif len(argv) == 3:
        baseproject = pathlib.Path(argv[-2])
        targetproject = pathlib.Path(argv[-1])
    
    if not baseproject.exists() or not targetproject.exists():
        print("!!! Target or base project not detected\nBase:{}Target:\n{}".format(str(baseproject), str(targetproject)))
        exit()
        
    # !!! Add code to copy the main urealproject correctly
    list_files(baseproject, targetproject)
    
    # make sure filepaths are correct
    
    # replace and print results

    
if __name__ == '__main__':
    main()