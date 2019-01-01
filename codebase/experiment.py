import os, utility, time


isNix = False
if os.name == 'posix':
    isNix = True

if isNix:
    # Start the clock
    start = time.time()

    # Begin Searching/Indexing File System
    os.system('ls /etc >> etc.txt')
    os.system('ls /tmp >> tmp.txt')
    os.system('ls /bin >> bin.txt')
    os.system('ls /usr/lib >> usrlib.txt')
    os.system('ls /usr/bin >> usrbin.txt')
    os.system('ls /usr/include >> inc.txt')
    etc_folder_contents = utility.swap('etc.txt', True)
    tmp_folder_contents = utility.swap('tmp.txt', True)
    bin_folder_contents = utility.swap('bin.txt', True)
    usr_lib_contents = utility.swap('usrlib.txt', True)
    usr_bin_contents = utility.swap('usrbin.txt', True)
    inc_folder_contents = utility.swap('inc.txt', True)

    # Stop the Clock
    stop = time.time()

    # Organize print statements
    line0 = "Finished Searching FileSystem in " + str(stop-start)+" seconds"
    line1 = " Folders/Files Found in /etc folder"
    line2 = " Folders/Files Found in /tmp folder"
    line3 = " Folders/Binaries Found in /bin folder"
    line4 = ' Folders/Files Found in /usr/lib'
    line5 = ' Folders/Binaries Found in /usr/bin'
    line6 = ' Folders/Files found in /usr/include'

    # Print the results
    print utility.console_color_printing(line0, 'purple', True, False)
    print str(len(etc_folder_contents))+utility.console_color_printing(line1, 'blue', True, False)
    print str(len(tmp_folder_contents))+utility.console_color_printing(line2, 'red', True, False)
    print str(len(etc_folder_contents))+utility.console_color_printing(line3, 'green', True, False)
    print str(len(usr_lib_contents)) + utility.console_color_printing(line4, 'red', True, False)
    print str(len(usr_bin_contents)) + utility.console_color_printing(line5, 'blue', True, False)
    print str(len(inc_folder_contents)) + utility.console_color_printing(line6, 'green', True, False)

