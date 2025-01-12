import { dateToLocal } from '../../utility/helper';
import './device-table.css'

interface DeviceTableProps {
    lastQueryTime: Date;
    devices: any[];
    isDetailTable: boolean;
}

function DeviceTable({ lastQueryTime, devices, isDetailTable }: DeviceTableProps) {
    function showModal(macAddress: string) {
        alert('show modal for device ' + macAddress)
    }

    if (isDetailTable) {
        return (
            <table className="striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Device Name</th>
                        <th>Manufacturer</th>
                        <th>IP Address</th>
                        <th>MAC Address</th>
                        <th>Last Connected UTC</th>
                        <th>Device Type</th>
                        <th>Notify</th>
                    </tr>

                </thead>
                <tbody>
                    {devices.map((device) =>
                        <tr onClick={() => showModal(device.id)}>
                            <td>{device.id}</td>
                            <td>{device.friendly_name}</td>
                            <td>{device.device_name}</td>
                            <td>{device.vendor_name}</td>
                            <td>{device.ip_address}</td>
                            <td>{device.mac_address}</td>
                            <td>{device.last_connected_date}</td>
                            <td>{device.device_type}</td>
                            <td>{device.notify_on_connect}</td>
                        </tr>
                    )}

                </tbody>
            </table>
        )
    }
    else {
        return (
            <table className="striped">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Device Name</th>
                        <th>Connected</th>
                        <th>Device Type</th>
                        <th>Notify</th>
                    </tr>
                </thead>
                <tbody>
                    {devices.map((device) =>
                        <tr onClick={() => showModal(device.id)}>
                            <td>{device.friendly_name}</td>
                            <td>{device.device_name}</td>
                            <td>
                                {(device.last_connected_date == lastQueryTime) ? <span>🟢</span> : <span>{dateToLocal(device.last_connected_date, true)}</span>}
                            </td>
                            <td>{device.device_type}</td>
                            <td>{(device.notify_on_connect) ? <span>✔</span> : <span>❌</span>}</td>
                        </tr>
                    )}
                </tbody>
            </table>
        )
    }
}

export default DeviceTable
