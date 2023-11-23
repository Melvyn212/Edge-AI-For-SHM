let CONFIG = {
    timespan: 1000, // 1 second
    keep_last: 1000
};

function status() {
    let switch_status = Shelly.getComponentStatus("switch", 0);
    let timestamps = Shelly.getComponentStatus("sys").unixtime;
    let result = {
        switch_ts: switch_status.aenergy.minute_ts,
        sys_ts: timestamps,
        current: switch_status.current,
        apower: switch_status.voltage 
    };

    return JSON.stringify(result);
}


