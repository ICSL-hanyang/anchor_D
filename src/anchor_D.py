#! /usr/bin/env python
import serial
import rospy
from geometry_msgs.msg import PoseStamped
#from anchor_D.msg import TagLocation

ser =  serial.Serial('/dev/ttyACM0',115200) #serial open
#######################ros######################################
rospy.init_node("anchor_D_node")
pub_xyz = rospy.Publisher('/anchorD', PoseStamped, queue_size=50)

send_xyz = PoseStamped()

rate = rospy.Rate(15)
################################################################

buff_1 = []
buff_2 = []
buff_3 = []
buff_4 = []

	
def Average_buff(buff) :
	if len(buff) == 0 : 
		return 1
	else :
		avg = sum(buff)/len(buff)
		return avg

while not rospy.is_shutdown():

	try : 
		##serial split
		data = ser.read(46)
		data_split = data.split('`')
		ser.flushInput()
		ser.flushOutput()
		send_xyz.pose.orientation.x = float(data_split[1])
		send_xyz.pose.orientation.y = float(data_split[3])
		send_xyz.pose.orientation.z = float(data_split[5])
		send_xyz.pose.orientation.w = float(data_split[7])
		if float(data_split[1]) == 0 :
			print("drop 0")
			send_xyz.pose.orientation.x = Average_buff(buff_1)

		if float(data_split[3]) == 0 :
			print("drop 1")
			send_xyz.pose.orientation.y = Average_buff(buff_2)

		if float(data_split[5]) == 0 :
			print("drop 2")
			send_xyz.pose.orientation.z = Average_buff(buff_3)

		if float(data_split[7]) == 0 :
			print("drop 3")
			send_xyz.pose.orientation.w = Average_buff(buff_4)

		print 'A0:',int(send_xyz.pose.orientation.x),'  A1:',int(send_xyz.pose.orientation.y),'  A2:',int(send_xyz.pose.orientation.z), '  A3:',int(send_xyz.pose.orientation.w)
		
		if float(data_split[1]) != 0 :
			buff_1.append(send_xyz.pose.orientation.x)

		if float(data_split[3]) != 0 :
			buff_2.append(send_xyz.pose.orientation.y)

		if float(data_split[5]) != 0 :
			buff_3.append(send_xyz.pose.orientation.z)

		if float(data_split[7]) != 0 :
			buff_4.append(send_xyz.pose.orientation.w)
		
		if len(buff_1) == 11 :
			buff_1.pop(0)
		if len(buff_2) == 11 :
			buff_2.pop(0)
		if len(buff_3) == 11 :
			buff_3.pop(0)
		if len(buff_4) == 11 :
			buff_4.pop(0)

		pub_xyz.publish(send_xyz)

		rate.sleep()
	except ValueError,e :
		print "error",e
		ser.flushInput()
		ser.flushOutput()




