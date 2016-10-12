server_load_time = {{ server_load_time }}
client_load_time = new Date();
offset = server_load_time - client_load_time;

alarm_times = [
		{hour:8, min: 0, lable: "1st/2nd block start"},
		{hour:21, min: 2, lable: "1st/2nd block end"},
	]

function get_server_time() {
	client_time = new Date();
	server_time = new Date();
	server_time.setTime(client_time.getTime() + offset);
	return server_time;
}

function start_clock() {
	get_bell_times_from_server();
	clock_tick()
	setInterval('clock_tick();','1000');	
}

function clock_tick() {
	time = get_server_time();
	s = time.getSeconds();
	
	update_time("time"); // update clock every second
	debug = false
	if (s == 0) { // check if a bell is to be rung on each 0th second of each minute and if so ring it
		ring_alarms();
		
	} else if ( s == 10 ) { // reload the bell schedule each minute on the 10th second
		get_bell_times_from_server();
	} else if (debug && s == 12) {
		for (i=0; i<alarm_times.length; i++) {
			alert(alarm_times[i]['lable'])
		}
	}
	
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
	bell_list = xml_doc.getElementsByTagName("bell");
	for (i = 0; i <bell_list.length; i++) { 
		bell_data = {}
		bell_data['hour'] = bell_list[i].getElementsByTagName("hour")[0].childNodes[0].nodeValue
		bell_data['min'] = bell_list[i].getElementsByTagName("minute")[0].childNodes[0].nodeValue
		bell_data['lable'] = bell_list[i].getElementsByTagName("lable")[0].childNodes[0].nodeValue
		alarm_times.push(bell_data);
	}
	
}


function update_time(id) {
	time = get_server_time();
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
			audio = new Audio('media/bellschedule/School_Bell.mp3');
			audio.play();
		}
	} 
}
