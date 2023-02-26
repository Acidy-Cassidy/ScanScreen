# ScanScreen

This current version is listed as 0. At time of created 2/26/23 there has only been one day of development so far.
===========================================================================================================
What I plan to add:

- Improve looks and 'flow' of the application
- Better outline of 'motion' detected in Screenshot Overlay window. As well as longer persistant rectangles.
- Notication counter that can count 'events'
- Menu with toggleable features.

- More as well. Likely a .net based version for windows users so they wont have to install a bunch of python reqs..







To install the required modules (cv2, keyboard, numpy) run this command: 
    
    
    
    -> May need to run as root
      -> pip install -r requirements.txt
      
    -> Alternatively if you are using Visual Studio 2019
      -> Open the .py file in VS2019 then in the top center section, next to the python environment version, there is a small icon shaped like a present.
            Click that button. From there a new window should appear and you will be able to search and add the requirements listed in the .txt file manually. 
            
            
 TO RUN
------------------------------------
* Start the program - An overlay will appear.
* With your mouse draw a rectangle around the area you want to monitor.
* After you draw the shape, release your mouse button.
* Hit the 'S' Key and a new window will appear. This contains the area you are monitoring for new changes. A console will also output when new changes happen with a time stamp.
* OPTIONALLY You can hit B to increase the brightness of the pop-out window.
* To Quit press 'Q' in the console
