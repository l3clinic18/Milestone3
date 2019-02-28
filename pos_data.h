//Header guard 
#ifndef pos_data
#define pos_data
#include <stdio.h>
//CSV data from the camera
void camera_data(FILE *fp, double& cam_pos_data);
//
void GPS_data(FILE *fp, double& GPS_pos_data);
//CSV data from decawave device
void UWB_data(FILE *fp, double& UWB_pos_data);

#endif