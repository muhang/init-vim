import os
import sys
import urllib.request
import shutil
import zipfile
import distutils.dir_util

TMP_FOLDER_NAME = ".vimtmp"
TMP_ZIP_NAME = "temp.zip"
TMP_VIMRC_NAME = "vimrc.txt"

PATH = os.getcwd()
PATH_TO_TMP = PATH + "/" + TMP_FOLDER_NAME
PATH_TO_ZIP = PATH + "/" + TMP_ZIP_NAME
PATH_TO_VIMTMP = PATH + "/" + TMP_VIMRC_NAME

PATH_TO_VIMRC = os.path.expanduser("~") + "/.vimrc"
PATH_TO_PATHOGEN = os.path.expanduser("~") + "/.vim/bundle"

PATHOGEN_PLUGINS = {
    "ag.vim" : "https://github.com/rking/ag.vim/archive/master.zip",
    "emmet-vim" : "https://github.com/mattn/emmet-vim/archive/master.zip",
    "nerdcommenter" : "https://github.com/scrooloose/nerdcommenter/archive/master.zip",
    "nerdtree" : "https://github.com/scrooloose/nerdtree/archive/master.zip",
    "supertab" : "https://github.com/ervandew/supertab/archive/master.zip",
    "tabular" : "https://github.com/godlygeek/tabular/archive/master.zip",
    "vim-fugitive" : "https://github.com/tpope/vim-fugitive/archive/master.zip",
    "vim-gitgutter" : "https://github.com/airblade/vim-gitgutter/archive/master.zip",
    "vim-indent-guides" : "https://github.com/nathanaelkane/vim-indent-guides/archive/master.zip",
    "vim-pad" : "https://github.com/fmoralesc/vim-pad/archive/master.zip",
    "vim-surround" : "https://github.com/tpope/vim-surround/archive/master.zip",
    "vim-windowswap" : "https://github.com/wesQ3/vim-windowswap/archive/master.zip"
}

PATHOGEN_THEMES = {
    "vim-monokai" : "https://github.com/sickill/vim-monokai/archive/master.zip",
    "base16-vim" : "https://github.com/chriskempson/base16-vim/archive/master.zip",
    "vim-colors-solarized" : "https://github.com/altercation/vim-colors-solarized/archive/master.zip",
    "vim-distinguished" : "https://github.com/Lokaltog/vim-distinguished/archive/master.zip"
}

PATHOGEN_SYNTAX = {
    "yajs.vim" : "https://github.com/othree/yajs.vim/archive/master.zip",
    "scss-syntax.vim" : "https://github.com/cakebaker/scss-syntax.vim/archive/master.zip",
    "javascript-libraries-syntax.vim" : "https://github.com/othree/javascript-libraries-syntax.vim/archive/master.zip",
    "mustache.vim" : "https://github.com/juvenn/mustache.vim/archive/master.zip",
    "vim-go" : "https://github.com/fatih/vim-go/archive/master.zip",
    "vim-cpp-enhanced-highlight" : "https://github.com/octol/vim-cpp-enhanced-highlight/archive/master.zip",
    "vim-jade" : "https://github.com/digitaltoad/vim-jade/archive/master.zip"
}

def process_pathogen():
    # if .vim/bundle exists
    if os.path.isdir(PATH_TO_PATHOGEN):
        if check_override("~/.vim/bundle already exisits, continuing will replace contents. Continue? (yes/no)") != True:
            return

    # Set up .vim/bundle structure in tmp directory
    print("=======================")
    print("Downloading plugins...")
    print("=======================")
    for plugin in PATHOGEN_PLUGINS:
        fetch_single_plugin(plugin, PATHOGEN_PLUGINS[plugin])
    
    print("=======================")
    print("Downloading themes...")
    print("=======================")
    for theme in PATHOGEN_THEMES:
        fetch_single_plugin(theme, PATHOGEN_THEMES[theme])

    print("=======================")
    print("Downloading syntax...")
    print("=======================")
    for syntax in PATHOGEN_SYNTAX:
        fetch_single_plugin(syntax, PATHOGEN_SYNTAX[syntax])

    # Delete existing pathogen downloads
    if os.path.isdir(PATH_TO_PATHOGEN):
        shutil.rmtree(PATH_TO_PATHOGEN)


    print("=======================")
    print("Copying to ~/.vim/bundle...")
    print("=======================")
    # Copy downloaded plugins to .vim/bundle
    os.makedirs(PATH_TO_PATHOGEN)
    distutils.dir_util.copy_tree(PATH_TO_TMP, PATH_TO_PATHOGEN)
    print("Finished processing pathogen")

def process_vimrc():
    # if .vimrc exists
    #if os.path.isdir(PATH_TO_PATHOGEN):
        #shutil.rmtree(PATH_TO_PATHOGEN)

    ## Copy downloaded plugins to .vim/bundle
    #os.makedirs(PATH_TO_PATHOGEN)
    #distutils.dir_util.copy_tree(PATH_TO_TMP, PATH_TO_PATHOGEN)
    if os.path.isfile(PATH_TO_VIMRC):
        if check_override(".vimrc already exists in home directory, continuing will overwrite this file. Continue? (yes/no)") != True:
            return

    # Delete existing vimrc
    print("=======================")
    print("Copying new vimrc to ~/.vimrc...")
    if os.path.isfile(PATH_TO_VIMRC):
        os.remove(PATH_TO_VIMRC)

    shutil.copyfile(PATH_TO_VIMTMP, PATH_TO_VIMRC)

    print("Finished processing vimrc")

def fetch_single_plugin(name, url):
    print("Fetching %s..." % name)

    # Download zip of repo
    try:
        urllib.request.urlretrieve(url, TMP_ZIP_NAME)
    except err:
        print("Couldn't get %s" % name)
        return

    # Extract zip to temp folder
    zip_ref = zipfile.ZipFile(PATH_TO_ZIP, "r")
    zip_ref.extractall(PATH_TO_TMP)
    zip_ref.close()
    
    # Rename folder
    raw_name = PATH_TO_TMP + "/" + name + "-master"
    os.rename(raw_name, remove_github_suffix(raw_name))

    print("Done!")
        
def remove_github_suffix(string):
    if string.endswith("-master"):
        return string[:-len("-master")]
    return string

def check_override(prompt):
    print("=======================")
    override = input(prompt)
    return override == "yes"

def cleanup():
    print("=======================")
    print("Cleaning up...")

    if os.path.isdir(PATH_TO_TMP):
        shutil.rmtree(PATH_TO_TMP)

    if os.path.isfile(PATH_TO_ZIP):
        os.remove(PATH_TO_ZIP)

def main():

    # Remove temp directory if it exists
    if os.path.isdir(PATH_TO_TMP):
        shutil.rmtree(PATH_TO_TMP)

    # Create temp directory
    os.mkdir(TMP_FOLDER_NAME) 

    # Process pathogen plugins
    process_pathogen()

    # Copy over .vimrc
    process_vimrc()

    cleanup()

    print("All done!")

if __name__ == "__main__":
    main()
