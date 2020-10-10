#!/usr/bin/python
' Using the daily Bing Wallpaper as Desktop background in GNU/LINUX '

from requests import get, ConnectionError, ConnectTimeout

from os import system, path, mkdir, environ, popen

from colorama import Fore

from desktop import kde

from re import findall

import uuid



def get_url():
    ' This function is to get the image URL on the site bing '
    global Home
    Home = path.expanduser('~')
    try:
        print(f"\n [{Fore.GREEN}+{Fore.WHITE}]{Fore.GREEN} Starting to download wallpaper...{Fore.RESET}")
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'        
        source = get("https://www.bing.com/", params=user_agent).text
        #regex for split link image
        url_image = "https://www.bing.com" + "".join(findall(r"href=\"(\/th?.*jpg)", source))        
        return url_image
    
    except ConnectionError as error:
        print(Fore.RED , error , Fore.RESET)

    except ConnectTimeout as error:
        print(Fore.RED , error , Fore.RESET)

    except ConnectionResetError as error:
        print(Fore.RED , error , Fore.RESET)


def download_wallpaper(url):
    ''' This function is for downloading wallpaper '''
    try:
        isdir_0 = path.exists(f"{Home}/Pictures/bing_wallpaper")
        isdir_1 = path.exists(f"{Home}/Pictures/bing_wallpaper/save_wallpaper")

        if isdir_0 is False:
            mkdir(f"{Home}/Pictures/bing_wallpaper/")

        elif isdir_1 is False:
            mkdir(f"{Home}/Pictures/bing_wallpaper/save_wallpaper/")

        download_img = get(url)
        if download_img.status_code == 200:
            print(f"\n [{Fore.GREEN}+{Fore.WHITE}]{Fore.GREEN} Getting wallpaper please wait...{Fore.RESET}")
            with open(f"{Home}/Pictures/bing_wallpaper/wallpaper.jpg", 'wb') as walp:
                walp.write(download_img.content)
            print(f"\n [{Fore.GREEN}+{Fore.WHITE}]{Fore.GREEN} Wallpaper successfully downloaded.{Fore.RESET}")

    except ConnectionError as error:
        print(Fore.RED , error , Fore.RESET)

    except ConnectTimeout as error:
        print(Fore.RED , error , Fore.RESET)

        
def set_background():
    ''' Checking Desktop Environment at System '''

    #checking desktop environment at system
    desktop = environ.get('XDG_CURRENT_DESKTOP')
    wm = popen(" xprop -root _NET_SUPPORTING_WM_CHECK | grep -Po 'window id #.*\K\W.*'").read().strip()
    wm = popen(f"xprop -id {wm}  _NET_WM_NAME | cut -d '\"' -f2 ").read().strip()
    
    if  "i3" in wm:
        # set wallpaper in backgrounnd in i3 WM

        system("feh --bg-fill /backdrop/screen0/monitor0/workspace0/last-image -s ~/Pictures/bing_wallpaper/wallpaper.jpg")
        
    if desktop.lower() == "xfce":
        # set wallpaper in backgrounnd in XFCE desktop

        system("xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s ~/Pictures/bing_wallpaper/wallpaper.jpg")

    elif desktop.lower() == 'gnome':
        # set wallpaper in backgrounnd in GNOME desktop

        system('gsettings set org.gnome.desktop.background picture-uri file://~/Pictures/bing_wallpaper/wallpaper.jpg')

    elif desktop.lower() == 'mate':
        # set wallpaper in backgrounnd in MATE desktop

        system("gsettings set org.mate.background picture-filename ~/Pictures/bing_wallpaper/wallpaper.jpg")

    elif desktop.lower() == 'unity':
        # set wallpaper in backgrounnd in UNITY desktop

        system('gsettings set com.canonical.unity-greeter background ~/Pictures/bing_wallpaper/wallpaper.jpg')
    
    elif desktop.lower() == 'kde' or desktop.lower() == 'kde-plasma':
        # set wallpaper in backgrounnd in KDE.* desktop

        kde.address('~/Pictures/bing_wallpaper/wallpaper.jpg')

    elif 'cinnamon' in desktop.lower():
        # set wallpaper in backgrounnd in CINNAMON desktop

        system(' gsettings set org.cinnamon.desktop.background picture-uri file://~/Pictures/bing_wallpaper/wallpaper.jpg')

    elif 'lxde' in desktop.lower():
        # set wallpaper in backgrounnd in LXDE desktop

        system('pcmanfm --set-wallpaper=~/Pictures/bing_wallpaper/wallpaper.jpg')

    else:
        print(Fore.MAGENTA + " Please Report a Bug." + Fore.RESET)

    
    save=input(f"\n [{Fore.YELLOW}!{Fore.WHITE}]{Fore.YELLOW} Did you like this wallpaper to save? (Y,N): " + Fore.RESET)
    if save.lower() == 'y' or save.lower() == 'yes' or save == '':
        uniq_id = uuid.uuid1()
        system(f"cp ~/Pictures/bing_wallpaper/wallpaper.jpg ~/Pictures/bing_wallpaper/save_wallpaper/{uniq_id}.jpg")

        print(f"\n [{Fore.GREEN}+{Fore.WHITE}] Successfully saved to the following directory {Fore.MAGENTA} >> {Fore.MAGENTA} {Fore.GREEN}~/Pictures/bing_wallpaper/save_wallpaper{Fore.RESET}\n")
        
    else:
        system('clear')
        print(Fore.GREEN + "OK Thank you for choosing me!\n" + Fore.RESET)

def main():
    download_wallpaper(get_url())
    set_background()

if __name__ == "__main__":
    main()

