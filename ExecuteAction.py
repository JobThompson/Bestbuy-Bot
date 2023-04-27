from ProgramState import programState
from Classes.Actions.BuyScript import buy_script
from Classes.Actions.MonitorScript import monitor_script

def execute_action():
    match programState.Action:
        case "BuyScript":
            buy_script()
        case "MonitorScript":
            monitor_script()