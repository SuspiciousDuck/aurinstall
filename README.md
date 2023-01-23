# aurinstall
This is a program to automate installing things on an Arch system. I was frustrated having to manually install things that were not on pacman when installing things like ffmpeg-full. With this, it is completely automated! There are likely plenty bugs with this, as it's just a small side project and I have only tested this on my machine.

# Usage
To install, just download the zip folder and unzip it with a program of your choice. <br>
Next, run the `main.py` file in the folder with arguments. <br>
The available options are `--uninstall` and `--install` <br>
For example, you'd run `python main.py --install ffmpeg` <br>
Hopefully, if all goes well, it should properly install <br>
Although this was made with the intent to automate, you may have to enter the root password, or choose to remove a conflicting package. <br>