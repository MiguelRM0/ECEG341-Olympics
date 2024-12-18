ECEG 341 Robot Olympics
Miguel Romero Muniz
Mike Merola
12/19/2024

Description: Our robot competes in four events in the ECEG 341 Robot Olympics; these events are the meter dash, curling, breaking, and marathon. Each events tests how well the robot
can perform in several areas including speed, sensing distance, following a line, a unique design, and overall ability to adapt to different circumstances. 

Relevant Files:
bot.py: The code to move the bot and the pin configuration is in this file. This file allows the robot to move forward, left, right, stop, and get the distance.
breaking.py: This file contains the code for the breaking event. The robot does a unique routine for 30 seconds while staying within a 75cm diameter circle.
curling.pt: This file contains the code for the curling event. The robot follows a line that ends halfway through the track then attempts to get within a target 45cm from the wall and 
light up when it reaches the target.
lineFollow.py: This file allows the robot to follow a line using a sensor that detects whether the group is white or black under it.
marathon.py: This file contains the code for the marathon event. The robot follows a track and must not get off course, this code primarily uses line follow to achieve this task.
meterDash.py: This file contains the code for the meter dash event. The robot must not move until the starting gate is moved then it must follow a 1m track as fast as it can and 
stop when it reaches the wall.

How to Run: To run the desired event you must open the terminal and type in:
python3 -m mpremote run "filename"
We have a script that sets up the code on the board which makes it so the board doesn't need to download the code each time.

Robot Features: Our robot was built using the CamJam EduKit #3. Our chassy is the kit's box with all of our sensors, motors, and microprosessor attached to it. Our distance sensor is
on the front of the bot with the trig pin connected to GP5 and the echo pin connected to GP4. Our neopixels are connected to GP18 and our buzzer was connected to GP22, both the lights
and buzzer are directly on the microprocessor. Our line sensor is on the bottom of the chassy held up by popsicle sticks that are glued together, the left line sensor is connected to GP2
and the right is connected to GP3. Our motors to turn the wheels are also on the underside of the chassy towards the back and we have a ball that rotates with the direction of the bot
stabilizing it in the front.
