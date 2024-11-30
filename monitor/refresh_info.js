url_1 = "http://34.213.136.51/all_server_status"
async function updateData_1() {
    response = await fetch(url_1);
    data = await response.json();
    console.log(data);
    table = document.getElementById("info-1");
    table.innerHTML = "";
    headerRow = table.insertRow();
    headerRow.insertCell().innerText  = "Server Name";
    headerRow.insertCell().innerText  = "Active Requests";
    headerRow.insertCell().innerText  = "CPU Usage";
    headerRow.insertCell().innerText  = "Last Updated";
    headerRow.insertCell().innerText  = "Requests in Last 5 Seconds";
    for (server in data) {
        row = table.insertRow();
        serverData = data[server];
        serverName = Object.keys(serverData)[0];
        serverData = serverData[serverName]
        console.log(serverData)
        row.insertCell().innerText = serverName;
        row.insertCell().innerText = serverData.active_requests;
        row.insertCell().innerText = serverData.cpu_usage;
        row.insertCell().innerText = serverData.last_updated;
        row.insertCell().innerText = serverData.req_last_5;
    }
}
url_2 = "http://34.82.218.52/all_server_status"
async function updateData_2() {
    response = await fetch(url_2);
    data = await response.json();
    console.log(data);
    table = document.getElementById("info-2");
    table.innerHTML = "";
    headerRow = table.insertRow();
    headerRow.insertCell().innerText  = "Server Name";
    headerRow.insertCell().innerText  = "Active Requests";
    headerRow.insertCell().innerText  = "CPU Usage";
    headerRow.insertCell().innerText  = "Last Updated";
    headerRow.insertCell().innerText  = "Requests in Last 5 Seconds";
    for (server in data) {
        row = table.insertRow();
        serverData = data[server];
        serverName = Object.keys(serverData)[0];
        serverData = serverData[serverName]
        console.log(serverData)
        row.insertCell().innerText = serverName;
        row.insertCell().innerText = serverData.active_requests;
        row.insertCell().innerText = serverData.cpu_usage;
        row.insertCell().innerText = serverData.last_updated;
        row.insertCell().innerText = serverData.req_last_5;
    }
}
setInterval(() => updateData_1(), 1000);
setInterval(() => updateData_2(), 1000);