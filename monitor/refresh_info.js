url = "http://35.89.30.6/all_server_status"
async function updateData() {
    response = await fetch(url);
    data = await response.json();
    console.log(data);
    table = document.getElementById("info");
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
setInterval(() => updateData(), 1000);