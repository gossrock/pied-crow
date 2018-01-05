offset = 0;

sched_name = ""
alarm_times = []

// the function that kicks everything off
function start_clock() {
	get_server_time_from_server(); // initial set up to syncronize time with server
	get_bell_times_from_server(); // initial list of times for bell schedule
	clock_tick() // run worker once
	setInterval('clock_tick();','1000'); // run the worker function once every second
}

// this function runs once a second and does various things based on the time
function clock_tick() {
	time = get_server_time();
	s = time.getSeconds();
	
	update_time("time"); // update clock every second
	debug = false
	if (s == 0) { // check if a bell is to be rung on each 0th second of each minute and if so ring it
		ring_alarms();
		
	} else if ( s == 10 ) { // reload the bell schedule each minute on the 10th second
		get_bell_times_from_server();
	} else if ( s == 15 ) { // reload the bell schedule each minute on the 10th second
		get_server_time_from_server();
	} else if (debug && s == 12) {
		for (i=0; i<alarm_times.length; i++) {
			alert(alarm_times[i]['lable'])
		}
	}
	
}

function get_server_time() {
	client_time = new Date();
	server_time = new Date();
	server_time.setTime(client_time.getTime() + offset);
	document.getElementById("debug").innerHTML = offset
	return server_time;
}

function get_server_time_from_server() {
	
	xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() { if (this.readyState == 4 && this.status == 200) {parse_server_time(this.responseText);} };
	xhttp.open("GET", "data/server_time", true);
	xhttp.send();
}


function parse_server_time(text) {
	server_load_time = text
	client_load_time = new Date();
	offset = server_load_time - client_load_time;
}



function get_bell_times_from_server() {
	
	xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() { if (this.readyState == 4 && this.status == 200) {parse_bell_xml(this);} };
	xhttp.open("GET", "data/bell_times.xml", true);
	xhttp.send();
	
}


function parse_bell_xml(xml) {
	alarm_times = []
	xml_doc = xml.responseXML;
	sched_name = xml_doc.getElementsByTagName("sched_name")[0].childNodes[0].nodeValue
	bell_list = xml_doc.getElementsByTagName("bell");
	for (i = 0; i <bell_list.length; i++) { 
		bell_data = {}
		bell_data['hour'] = bell_list[i].getElementsByTagName("hour")[0].childNodes[0].nodeValue
		bell_data['min'] = bell_list[i].getElementsByTagName("minute")[0].childNodes[0].nodeValue
		bell_data['lable'] = bell_list[i].getElementsByTagName("lable")[0].childNodes[0].nodeValue
		alarm_times.push(bell_data);
	}
	display_schedule()
}

function display_schedule() {
	document.getElementById("sched_name").innerHTML = sched_name
	innerhtml = "<table class='w3-table w3-striped'>"
	for (i = 0; i < alarm_times.length; i++) {
		alarm_data = alarm_times[i]
		hour = alarm_data['hour']
		if (hour<10) { hour= "0"+hour}
		minute = alarm_data['min']
		if (minute<10) { minute= "0"+minute}
		lable = alarm_data['lable']
		innerhtml += "<tr><td>"+hour+":"+minute+"</td><td>"+lable+"</td></tr>"
	}
	innerhtml += "</table>"
	document.getElementById("schedule_table").innerHTML = innerhtml
}

WEEK_DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH_NAMES = ["January", "Febuary", "March", "Apirl", "May", "June", "July", "August", "September", "October", "November", "December"]

function update_time(id) {
	time = get_server_time();
	
	day_of_week = WEEK_DAY_NAMES[time.getDay()];
	month = MONTH_NAMES[time.getMonth()]; 
	day = time.getDate();
	year = time.getFullYear()
	
	date_str = day_of_week+", "+month+" "+day+", "+year
	
	document.getElementById("date").innerHTML = date_str
	
	
	h = time.getHours();
	m = time.getMinutes();
	s = time.getSeconds();
	
	if(h<10) { h = "0"+h; }
	if(m<10) { m = "0"+m; }
	if(s<10) { s = "0"+s; }
	
	formated_time = h+':'+m+':'+s;
	document.getElementById(id).innerHTML = formated_time;
}

function ring_alarms() {
	date = get_server_time();
	h = date.getHours();
	m = date.getMinutes();
	for (i=0; i<alarm_times.length; i++) {
		a = alarm_times[i];
		hour = a['hour'];
		min = a['min'];
		lable = a['lable']
		if ((hour == h) && (min == m)) {
			document.getElementById("last_alarm").innerHTML = lable;
			audio = new Audio('media/bells/School_Bell_4s.mp3');
			audio.play();
		}
	} 
}
