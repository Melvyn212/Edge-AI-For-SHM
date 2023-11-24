function yield_power() {
    let timestamp = Shelly.getComponentStatus("sys").unixtime;
    let switch_status = Shelly.getComponentStatus("switch", 0);
    let result = {
        switch_ts: switch_status.aenergy.minute_ts,
        sys_ts: timestamp,
        current: switch_status.current,
        apower: switch_status.voltage 
    };

    return JSON.stringify(result);
}