#!/usr/bin/env python3
# encoding: utf-8

"""\
Copy relevant files between your firefox profile and a remote destination.

Usage:
    firefox_profile backup <rsync_url> [<profile_dir>] [options]
    firefox_profile restore <rsync_url>

Arguments:
    <rsync_url>
        The remote destination to sync with.  Any URL that ``rsync'' can 
        understand will be accepted.

    <profile_dir>
        The profile to backup.  If not specified, your default profile 
        ``~/.mozilla/*.default'' will be used.

Options:
    -A, --no-autocomplete
        The ``formhistory.sqlite'' file remembers what you have searched for 
        in the Firefox search bar and what information you've entered into 
        forms on websites.

    -B, --no-bookmarks
        The ``places.sqlite'' file contains all your Firefox bookmarks and 
        lists of all the files you've downloaded and websites you've visited.  
        The ``bookmarkbackups'' folder stores bookmark backup files, which can 
        be used to restore your bookmarks.

    -C, --no-certificates
        The ``cert8.db'' file stores all your security certificate settings 
        and any SSL certificates you have imported into Firefox.

    -K, --no-cookies
        A cookie is a bit of information stored on your computer by a website 
        you've visited.  Usually this is something like your site preferences 
        or login status.  Cookies are all stored in the ``cookies.sqlite'' 
        file. 

    -D, --no-dictionary
        The ``persdict.dat'' file stores any custom words you have added to 
        Firefox's dictionary.

    -W, --no-download-actions
        The ``mimeTypes.rdf'' file stores your preferences that tell Firefox 
        what to do when it comes across a particular type of file.  For 
        example, these are the settings that tell Firefox to open a PDF file 
        with Acrobat Reader when you click on it.

    -P, --no-passwords
        Your passwords are stored in the ``key3.db'' and ``logins.json'' 
        files.

    -R, --no-preferences
        The ``prefs.js'' file stores customized user preference settings, such 
        as changes you make in Firefox Preferences dialogs. The optional 
        ``user.js'' file, if one exists, will override any modified 
        preferences.

    -S, --no-search-engines
        The ``search.sqlite'' file and ``searchplugins'' folder store the 
        search engines that are available in the Firefox Search bar.

    -I, --no-site-settings
        The ``permissions.sqlite'' and ``content-prefs.sqlite'' files store 
        many of your Firefox permissions (for instance, which sites are 
        allowed to display popups) or zoom levels that are set on a 
        site-by-site basis.

    -Y, --no-styles
        The ``chrome/userChrome.css'' and ``chrome/userContent.css'' files 
        store user-defined changes to either how Firefox looks, or how certain 
        websites or HTML elements look or act. 

Descriptions of the files that comprise your firefox profile were taken from:
https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data
"""

from pprint import pprint
from pathlib import Path

__version__ = '0.0.0'

def main():
    import docopt

    args = docopt.docopt(__doc__)
    url = args['<rsync_url>']
    profile = Path(args['<profile_dir>'] or firefox_profile_dir())
    kwargs = {
            key[len('--no-'):].replace('-', '_').lower(): not value
            for key, value in args.items()
            if key.startswith('--no-')
    }

    if args['backup']:
        files = pick_files(profile, **kwargs)
        backup_files(url, files)

    if args['restore']:
        restore_files(profile, url)
            
def pick_files(profile_dir, **kwargs):
    """
    Return paths to the files from the profile that should be backed up.

    There are 17 files that can be backed up.  They have been organized into 11 
    categories for your convenience:
        
    - autocomplete
    - bookmarks
    - certificates
    - cookies
    - dictionary
    - download_actions
    - passwords
    - preferences
    - search_engines
    - site_settings
    - styles

    By default all 17 files will be backed up, but you can prune any of the 
    above categories by passing it as a keyword argument set to False, i.e. 
    ``cookies=False''.
    """
    profile_files = {   # (no fold)
        'autocomplete': [
            'formhistory.sqlite',
        ],
        'bookmarks': [
            'places.sqlite',
            'bookmarkbackups',
        ],
        'certificates': [
            'cert8.db',
        ],
        'cookies': [
            'cookies.sqlite',
        ],
        'dictionary': [
            'persdict.dat',
        ],
        'download_actions': [
            'mimeTypes.rdf',
        ],
        'passwords': [
            'key3.db',
            'logins.json',
        ],
        'preferences': [
            'prefs.js',
            'user.js',
        ],
        'search_engines': [
            'search.json',
            'searchplugins',
        ],
        'site_settings': [
            'permissions.sqlite',
            'content-prefs.sqlite',
        ],
        'styles': [
            'chrome/userChrome.css',
            'chrome/userContent.css',
        ],
    }
    picked_files = []

    for key in profile_files:
        if kwargs.get(key, True):
            picked_files += [profile_dir / x for x in profile_files[key]]

    return [x for x in picked_files if x.exists()]

def backup_files(url, files):
    """
    Use ``rsync'' to copy the given files to the given URL.
    """
    import subprocess
    rsync = ['rsync', '-r'] + [str(x) for x in files] + [url]
    subprocess.call(rsync)

def restore_files(profile_dir, url):
    """
    Use ``rsync'' to copy files from a remote destination into your firefox 
    profile.
    """
    import subprocess
    rsync = ['rsync', '-r', url.rstrip('/'), str(profile_dir)]
    subprocess.call(rsync)

def firefox_profile_dir():
    """
    Return the path to the default firefox profile.  This is surprisingly 
    nontrivial because there are usually several profiles and each is named by 
    a string of random characters.  Finding the default profile requires 
    parsing ``~/.mozilla/firefox/profiles.ini''.
    """
    import configparser

    firefox_dir = Path(os.path.expanduser('~/.mozilla/firefox'))
    ini = configparser.ConfigParser()
    ini.read(str(firefox_dir / 'profiles.ini'))

    for section in ini.sections():
        if ini[section].get('Default') == '1':
            return firefox_dir / ini[section]['Path']


if __name__ == '__main__':
    main()

