let CONFIG = {
  timespan: 1000, // 1 second (under 1s timestamp is not precise enough)
  list_size: 100, // Max stored measurements 
  url_segment: "api", // script api endpoint
  actions: {},
  registerActionHandler: function (actionParamValue, handler) {
    this.actions[actionParamValue] = handler;
  },
};


function Measurement(current, voltage, power, timestamp) {
  return {
    current: current,
    voltage: voltage,
    power: power,
    timestamp: timestamp,
  };
}
// List class using prototypes
function List() {
  return {
    head: null,
    tail: null,
    size: 0,
    toJSON: function() {
      let items = [];
      let current = this.head;
    
      while (current) {
        items.push(current.item);
        current = current.next;
      }
    
      return items;
    },
    append: function(item) {
      let newNode = {
        item: item,
        prev: null,
        next: null,
      };
      
      if (!this.head) { // this is the first element
        this.head = newNode;
        this.tail = newNode;
      } else {
        newNode.prev = this.tail;
        this.tail.next = newNode;
        this.tail = newNode;
      }
    
      if (this.size < CONFIG.list_size) {
        this.size++;
      } else { // delete earliest item if the list is full
        this.head = this.head.next;
        this.head.prev = null;
      }
    }
  };
}




let measurements = List();

let yield_power = function() {
  let switch_status = Shelly.getComponentStatus("switch", 0);
  let measurement = Measurement(
    switch_status.current,
    switch_status.voltage,
    switch_status.apower,
    switch_status.aenergy.minute_ts
  );
  measurements.append(measurement);
};

Timer.set(CONFIG.timespan, true, yield_power);


// API definition
function yield_handler(response) {
  response.code = 200;
  response.body = JSON.stringify(measurements.toJSON());
}
CONFIG.registerActionHandler("yield", yield_handler);

// Passing from the HTTP server to the API appropriate handler
function httpServerHandler(request, response) {
  console.log("Request", JSON.stringify(request));
  let param = request.query;
  if (
    typeof param === "undefined" ||
    typeof CONFIG.actions[param] === "undefined" ||
    CONFIG.actions[param] === null
  ) {
    response.code = 400;
    response.body =
      "No " +
      CONFIG.action_param +
      " parameter in query string or no action defined";
    response.send();
  } else {
    CONFIG.actions[param](response);
    response.send();
    console.log("Handler called");
  }
}
HTTPServer.registerEndpoint(CONFIG.url_segment, httpServerHandler)