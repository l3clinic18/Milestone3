# Milestone3
Source writen in Python 3.5 
Branch(s):
	master -> Robot A,
	RobotB -> Robot B,
	RobotC -> Robot C (This branch will be added soon).

		/\
                  /  \
           base  /    \  rover
                /      \
               /________\
                   rtk
L3Clinic Project 2018-2019, University of Utah, ECE College of Engineering
Project Members: Joe, Andrew & Trevor. L3 Liason: Scott Lyon.
ECE Advisors: Jon Davies, Angela Rassmusen & Alex Orange

Goal of the project was to acheive an azimuth no more than 3 sigma from the true bearing, at a distance of 100 meters. To achieve this, we used Ubox GPS modules for the base and rover to get the rtk distance as seen above.
Decawave Ultrawide band modules (3) to get Rover and Base distances to the target and a Pixy camera (first revsion) to correct for any error.
