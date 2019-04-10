import decawave
#import sss_triangle_angles
distance = 59.294
test = decawave.regression_correction(distance)
print("final value = " + str(test))
print("error = " + str(test - 59.546))

#dist = sss_triangle_angles.decawave_offset_correction(90,5)
#print(dist)