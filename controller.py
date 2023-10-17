import math
import main
# import queue              ....

# angle_queue = queue.Queue()       ....
#
# def getAngle():
#     global angle_queue
#     return angle_queue


def controller(queue):
    #ser = serial.Serial('COM10', 9600, timeout=1)

    # global angle_queue                        ....

    print('controller_thread_started')
    is_first_val = False
    IVL = []
    sj0_x, sj0_y, lj0_x, lj0_y, hj0_x, hj0_y = 0, 0, 0, 0, 0, 0
    l0_h = 0.0

    # define each gradients
    mh0, mu0, mh, mu = 0.0, 0.0, 0.0, 0.0


    while True:
        value = queue.get()
        if value is None:
            continue
        else:
            # print(value)
            if not is_first_val:
                is_first_val = True
                IVL = value

                print(value)
                sj0_x, sj0_y, lj0_x, lj0_y, hj0_x, hj0_y = IVL[0][1], IVL[0][2], IVL[1][1], IVL[1][2], IVL[2][1], \
                IVL[2][2]  # Each joint coordinates initially
                l0_h = math.sqrt((sj0_x - lj0_x) ** 2 + (sj0_y - lj0_y) ** 2)  # initial_lengths of humerus part

                # take initial coordinates
                # initial shoulder coordinates are //sj0_x, sj0_y//
                # initial elbow coordinates are //lj0_x, lj0_y//
                # initial hand coordinates are //hj0_x, hj0_y//

                # now let's calculate initial gradients of lines each Humerus and Ulna parts
                if (sj0_x != lj0_x) or (lj0_x != hj0_x):
                    mh0 = (sj0_y - lj0_y)/(sj0_x - lj0_x) # m- gradient h-humerus 0 - initial
                    mu0 = (lj0_y - hj0_y)/(lj0_x - hj0_x)
                    print(mh0, mu0)
                elif (sj0_x == lj0_x) or (lj0_x == hj0_x):
                    mh0, mu0 = 0.0,0.0
            # set current values
            else:
                sj_x, sj_y, lj_x, lj_y, hj_x, hj_y = value[0][1], value[0][2], value[1][1], value[1][2], value[2][1], \
                value[2][2]
                l_h = round(math.sqrt((sj_x - lj_x) ** 2 + (sj_y - lj_y) ** 2), 1)

                # now let's calculate current gradients of lines each Humerus and Ulna parts
                if (sj_x == lj_x) or (lj_x == hj_x):
                    pass
                else:
                    mh = (sj_y - lj_y) / (sj_x - lj_x)  # m- gradient h-humerus 0 - initial
                    mu = (lj_y - hj_y) / (lj_x - hj_x)

                # shoulder flexion angle
                shoulder_angle = round(math.atan((math.fabs((mh - mh0)))/(1 + mh*mh0)), 2)
                shoulder_angle = math.fabs(round(math.degrees(shoulder_angle), 0))
                if sj0_x == lj0_x:
                    shoulder_angle = 90.0 - shoulder_angle

                # elbow angle
                elbow_angle = round(math.atan((math.fabs((mu - mu0))) / (1 + mu * mu0)), 2)
                elbow_angle = math.fabs(round(math.degrees(elbow_angle), 0))
                if lj0_x == hj0_x:
                    elbow_angle = 90.0 - elbow_angle



                if (elbow_angle <= shoulder_angle + 1):
                    print('Shoulder flexion Angle : \t', shoulder_angle)
                else :
                    rel_el_ang = elbow_angle - shoulder_angle
                    print('Shoulder flexion Angle : ', shoulder_angle)
                    print('Elbow flexion Angle : \t', rel_el_ang)

                if l0_h > l_h:
                    j1_angle = math.acos(round(l_h / l0_h, 4))
                    j1_angle_degrees = math.degrees(j1_angle)
                    print('Shoulder abduction Angle : \t', round(j1_angle_degrees))
                    #ser.write(int(j1_angle_degrees))
                    # angle_queue.put(j1_angle_degrees)                                     ....


        if main.req == 'stop':
            break
    return
