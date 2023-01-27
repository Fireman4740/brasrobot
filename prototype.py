from logging import config
import yaml
"""
# xArm-Python-SDK: https://github.com/xArm-Developer/xArm-Python-SDK
# git clone git@github.com:xArm-Developer/xArm-Python-SDK.git
# cd xArm-Python-SDK
# python setup.py install
"""
try:
    from xarm.tools import utils
except:
    pass
from xarm import version
from xarm.wrapper import XArmAPI


import logging
from logging import config
import json 
with open("config.yaml","r") as f:
        data= yaml.safe_load(f)

with open(data["logConfigfile"],'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)
################ Logger #################
logger = logging.getLogger("__main__")
logger.debug("Inside Addition Function")
# 
    # logger.warning("Warning : Parameter A is passed as String. Future versions won't support it.")
    # logger.info("Addition Function Completed Successfully")
    

if __name__ == "__main__":
    params = {'events': {}, 'callback_in_thread': True, 'quit': False}
    
    
    
    try:
        arm = XArmAPI(data["ip_robots"], baud_checkset=False)
        arm.clean_warn()
        arm.clean_error()
        arm.motion_enable(True)
        arm.set_mode(0)
        arm.set_state(0)
    except Exception as e:
        logger.exception("Exception in ".format(e))
    
    def error_warn_change_callback(data):
        if data and data['error_code'] != 0:
            params['quit'] = True
            logger.error('err={}, quit'.format(data['error_code']))
            arm.release_error_warn_changed_callback(error_warn_change_callback)
            arm.register_error_warn_changed_callback(error_warn_change_callback)
        
    def state_changed_callback(data):
        if data and data['state'] == 4:
            if arm.version_number[0] > 1 or (arm.version_number[0] == 1 and arm.version_number[1] > 1):
                params['quit'] = True
                logger.error('state=4, quit')
                arm.release_state_changed_callback(state_changed_callback)
    arm.register_state_changed_callback(state_changed_callback)


    # Register counter value changed callback
    if hasattr(arm, 'register_count_changed_callback'):
        def count_changed_callback(data):
            if not params['quit']:
                logger.error('counter val: {}'.format(data['count']))
        arm.register_count_changed_callback(count_changed_callback)

    # Register connect changed callback
    def connect_changed_callback(data):
        if data and not data['connected']:
            params['quit'] = True
            logger.error('disconnect, connected={}, reported={}, quit'.format(data['connected'], data['reported']))
            arm.release_connect_changed_callback(error_warn_change_callback)
    arm.register_connect_changed_callback(connect_changed_callback)
    
    def move_robot(data):
        
        if arm.error_code == 0 and not params['quit']:
            code =  arm.set_position(x=data["position_1"]["x"], y=data["position_1"]["y"], z=data["position_1"]["z"]+100, roll=data["position_1"]["roll"], pitch=data["position_1"]["pitch"], yaw=data["position_1"]["yaw"], speed=data["speed_move"], mvacc=data["mvacc"], wait=False)
            if code != 0:
                params['quit'] = True
                logger.error('set_position, code={}'.format(code))
        
        
        if arm.error_code == 0 and not params['quit']:
            code =  arm.set_gripper_position(data["gripper_position_2"], wait=False, speed=data["speed_gripper"], auto_enable=True)
            if code != 0:
                params['quit'] = True
                logger.error('set_gripper_position, code={}'.format(e))
        
        if arm.error_code == 0 and not params['quit']:
            code =  arm.set_position(x=data["position_1"]["x"], y=data["position_1"]["y"], z=data["position_1"]["z"], roll=data["position_1"]["roll"], pitch=data["position_1"]["pitch"], yaw=data["position_1"]["yaw"], speed=data["speed_move"], mvacc=data["mvacc"], wait=False)
            if code != 0:
                params['quit'] = True
                logger.error('set_position, code={}'.format(code))
        
        if arm.error_code == 0 and not params['quit']:
            code =  arm.set_gripper_position(data["gripper_position_1"], wait=False, speed=data["speed_gripper"], auto_enable=True)
            if code != 0:
                params['quit'] = True
                logger.error('set_gripper_position, code={}'.format(e))
                
        if arm.error_code == 0 and not params['quit']:
            code =  arm.set_position(x=data["position_1"]["x"], y=data["position_1"]["y"], z=data["position_1"]["z"]+100, roll=data["position_1"]["roll"], pitch=data["position_1"]["pitch"], yaw=data["position_1"]["yaw"], speed=data["speed_move"], mvacc=data["mvacc"], wait=False)
            if code != 0:
                params['quit'] = True
                logger.error('set_position, code={}'.format(code))
        
        if arm.error_code == 0 and not params['quit']:
            code =  arm.set_position(x=data["position_2"]["x"], y=data["position_2"]["y"], z=data["position_2"]["z"]+100, roll=data["position_2"]["roll"], pitch=data["position_2"]["pitch"], yaw=data["position_2"]["yaw"], speed=data["speed_move"], mvacc=data["mvacc"], wait=False)
            if code != 0:
                params['quit'] = True
                logger.error('set_position, code={}'.format(code))
                
                
        if arm.error_code == 0 and not params['quit']:
            code =  arm.set_gripper_position(data["gripper_position_2"], wait=False, speed=data["speed_gripper"], auto_enable=True)
            if code != 0:
                params['quit'] = True
                logger.error('set_gripper_position, code={}'.format(e))
    
            
    for i in range(3):
        move_robot(data)
            
    
