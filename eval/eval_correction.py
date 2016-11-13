#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Some manual evaluation correction.
"""

correct_temp_pairs = [
    (
        "Print the list of files from the \"/zu/durchsuchender/Ordner\" directory tree whose "
        "names begin with \"beispieldatei\" and which contain string \"Beispielinhalt\"\n",
        "find -exec grep -l Pattern {} \; -name Pattern File"
    )]

error_temp_pairs = [
    (
        "display all the regular files in the current folder which dont not have the permission 777\n",
        "find -perm Permission -type f File"
    ),
    (
        "find any files in the current directory that begin with a number\n",
        "find -name Pattern File"
    ),
    (
        "find file which case-insensitive name is foo in current directory.\n",
        "find -name Pattern File"
    ),
    (
        "Remove all \"work\" directories residing in /usr/ports and below\n",
        "find -exec rm {} \; -name Pattern -type d File"
    ),
    (
        "List root's regular files with permissions 4000\n",
        "find -exec ls -l {} \; -perm Permission -print -type f File"
    ),
    (
        "display all sqlite files in the current directory along with their timestamp\n",
        "find -printf Pattern File"
    ),
    (
        "Find .gif and .png image files in ~/Desktop and move them to the ~/Pictures directory.\n",
        "find -exec mv File {} \; -name Pattern File"
    ),
    (
        "display all the files in the current directory excluding the paths \"targert\", \"tools\", \"git\"\n",
        "find \( -path File -prune -or -print \) File"
    ),
    (
        "Delete all .svn files/directories under current directory\n",
        "find -exec rm {} \; -name Pattern File"
    ),
    (
        "Copy file header.shtml to directories dir1, dir2, dir3, and dir4\n",
        "find -exec cp File {} \; -name Pattern File"
    ),
    (
        "Count the number of files/directories named file1 under current directory\n",
        "find -exec wc -l {} \; -name Pattern File"
    ),
    (
        "search for all the directories ending with \".mp3\" in the file system and move them to "
                                                         "the folder /mnt/mp3\n",
        "find -iname Pattern -print0 -type f File | xargs -0 -I {} mv File {}"
    ),
    (
        "Find files with 002 permission in entire file system and print them with the string 'has world write "
        "permissions' appended after every path\n",
        "find -exec ls -l {} \; -perm Permission -type f File"
    )]

correct_str_pairs = [
    (
        "List all empty files in the current directory tree\n",
        "find . -empty"
    )]

error_str_pairs = [
    (
        "find  file which case-insensitive name is too in currect directory\n",
        "find . -iname \"filename\""
    ),
    (
        "search for files with the name \"temp\" in the /usr folder\n",
        "find /usr -name '*.sh'"
    ),
    (
        "Find all the files called FindCommandExamples.txt of owner root\n",
        "find / -user root -name tecmint.txt"
    ),
    (
        "Find all .c and .h files in the current directory tree and search them for \"expr\"\n",
        "find . -name '*.[ch]' | xargs grep -E 'expr'"
    ),
    (
        "Find all *.py files under and below the current directory and search them for \"xrange\"\n",
        "find . -name *.py | xargs grep some_function"
    ),
    (
        "Find all .c and .h files in the current directory tree and search them for \"expr\"\n",
        "find . -name \"*.c\" | xargs grep -E 'expr'"
    ),
    (
        "find all the swap files (files ending with ~) in the current folder and delete them\n",
        "find . -name \"*.sh\" -exec rm -r -f {} \;"
    ),
    (
        "display all files in the current directory excluding those that are present in the directories whose name starts with \"efence\" and do not search in the sub directories\n",
        "find \( -name Pattern -prune -or -name Pattern \) -print File"
    )]
