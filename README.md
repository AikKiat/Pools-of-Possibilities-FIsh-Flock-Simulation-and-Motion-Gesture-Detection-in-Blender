A fun project utilising Motion Gesture Detection, to control the behaviour of virtual fishes in a fully custom-built Blender scene, initialised via code using Blender's python .bpy python scripting library. 

Access the main files in the folder <<fish-flock-simulation>>
Inside:
1. Our trained Tensorflowlife models are found in <<model>>
2. Blender files containing the .blend files of our custom made Fish models, and rigs are in <<Blender Scene Files>>, the ojects of each .blend imported into a new Blender scene via our script
3. <<Miscelleanous>> Contains old random test files

4. Try everything out in <<Run Simulation>>
Requirements:
Blender Development addon for VSCode. Used to create a new Blender Scene and run our Blender python scripts. https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development
Run Motion_Gesture_Detect.py first to start the motion detection service.
Open Blender_Scene_Initialiser.py, CRTL+P to access Blender Python's START SCENE command, and then RUN SCRIPT. The scene should be set up automatically. Feel free to adjust any of the meshes such as the floor plane.
Press the Animation Play Button in Blender, or simply tap the space bar, and let the simulation begin.

Enjoy!

Use a dedicated Webcam / Video Capture device such as an XBOX Kinect for the best experience --> mount it above you so that it can detect the gestures, and project the scene to the floor for a more grand interaction. 

Inspiration: https://vanschneider.com/blog/sensory-surreal-worlds-teamlab/

Our website:
https://titustsang2000.wixsite.com/sc05-grp-8-dti



