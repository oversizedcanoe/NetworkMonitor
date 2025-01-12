import './device-table.css'

interface DeviceTableProps {
    lastQueryTime: Date;
    devices: any[]
}

function DeviceTable({lastQueryTime, devices}: DeviceTableProps) {

  return (
    <table className="striped">
    <thead>
        <th>Name</th>
        <th>Device Name</th>
        <th>Connected</th>
        <th>Device Type</th>
        <th>Notify</th>
    </thead>
    <tbody>
        {devices.map((device) => 
            <tr>
            <td>{device.friendly_name}</td>
            <td>{device.device_name}</td>
            <td>
                {(device.last_connected_date == lastQueryTime) ? <span>🟢</span> : <span>{device.last_connected_date}</span>}
            </td>
            <td>{device.device_type}</td>
            <td>{(device.notify_on_connect) ? <span>✔</span> : <span>❌</span>}</td>
        </tr>
        )}
    </tbody>
</table>

  )
}

export default DeviceTable
