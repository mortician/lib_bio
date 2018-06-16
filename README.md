bh_tools
======

Extract RDT files
-----------------
The plugin will extract a RDT that was selected by using the Blender/Maya file selection dialog, to a temporary "work folder".
E.g: You select "C:\ROOM1000.RDT" that will result in the plugin extracting all of the files contents to a folder called "ROOM1000" that will be created in the same directory where the selected RDT is located.

Rebuild RDT files
-----------------
After using the Blender/Maya folder selection dialog and selecting the "work folder" of an extracted RDT the plugin will rebuild it again.

- Import/Export BLK data (Data can be imported, edited and exported)
- Import/Export FLR data (Data can be imported, edited and exported)
- Import/Export LIT data (Data can be imported, edited and exported)
- Import/Export RID data (Data can be imported, edited and exported)
- Import/Export RVD data (Data can be imported, edited and exported)
- Import/Export SCA data (Data can be imported, edited and exported)
- Import/Export SCD data (Data can be imported, edited and exported. Note only AOTs of the main script are utilized atm.)
- Import/Export MD1 data (Item models will be imported and positioned according to references found in the main SCD)
