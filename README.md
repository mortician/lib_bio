lib_bio
======

lib_bio is a python powered toolchain/library collection for the classic BIOHAZARD games, it's goal is to support every file format of the classic games.

It has I/O frontend modules that include the Blender import/export plugin for loading up and editing RDT files. 
I decided to focus on Blender for now, it's too much of a hassle to work on Blender and Maya at the same time.

lib_bio will offer extraction/rebuilding of a range of common modding relevant file formats. It's modules can be used as a base to write frontend programs that will handle the formats.


How to use the Blender RDT plugin?
======
Right now only the Blender I/O module is utilizing lib_bio

1. Download the linked archive
2. Copy/extract the "lib_bio" folder and the io_rdt_blender.py file from the archive to your Blender script addon folder (e.g. "C:\Users\YOUR_USER\AppData\Roaming\Blender Foundation\Blender\2.xx\scripts\addons") (!!! Note that this current version will only work with Blender 2.79, Blender 2.8 might be supported in the future...
3. Go to File>User preferences, go to "Addons" press the "Install addon from file..." button on the lower part of the User preferences window and select the "io_rdt_blender.py" in your script folder (see path example above)
4. Find the addon under "Supported Level" "Community" on the left upper side of the window, search for "Import-Export: BIOHAZARD RDT" and activate it by checking the checkbox
5. You can now use the RDT file import by using "File>Import>BIOHAZARD RDT (.RDT)"
