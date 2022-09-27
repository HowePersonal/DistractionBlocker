# DistractionBlocker
GUI application that disables access to selected websites and installed desktop applications. 

UPDATE 8/31/2022:
Created base functionality with application blocking and website blocking. Application blocking specifically required the implementation of multi-threading, enabled by a module from PyQt5.
User interaction is maintained through a GUI created with PyQt5, allowing users to add websites or installed applications to be blocked. 

UPDATE 9/02/2022: 
Refactored program to block websites through browser extension, therefore no longer requiring modification of the hostname. 

UPDATE 9/06/2022:
Added scheduling feature to allow users to create periods of time in which the blocker would be activated. Created a visualization of these scheduled blocks within the UI.

UPDATE 9/10/2022:
Refactored full Qt GUI by using one single window as the UI, created custom title bar for better style and frames to allow for resizing

UPDATE 9/20/2022:
Implemented proper scheduling display blocks, allowing program to correctly visualize periods scheduled to be blocked by users
