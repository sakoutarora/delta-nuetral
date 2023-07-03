from datetime import datetime
from dependencies.generic import init, init_position, TrackPos, CheckInitalPostion
from dependencies.constants import INIT_DELTA

def EventLoop():
    init()
    done_init = CheckInitalPostion()
    if not done_init:
        init_position(INIT_DELTA)
    else:
        TrackPos()

if __name__ == "__main__":
    starttime = datetime.now()
    print('--------------------------------- Start ----------------------------- ')
    EventLoop()
    endtime = datetime.now()
    print(f'--DONE-- time taken {endtime - starttime}')