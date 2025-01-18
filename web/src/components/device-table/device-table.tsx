import { ModalService } from '../../services/modal.service';
import { dateToLocal } from '../../utility/helper';
import DeviceIcon from '../device-icon/device-icon';
import './device-table.css'

interface DeviceTableProps {
    lastQueryTime: Date;
    devices: any[];
    isDetailTable: boolean;
}

function DeviceTable({ lastQueryTime, devices, isDetailTable }: DeviceTableProps) {
    function showModal(id: number) {
        ModalService.setOpen(true, {id: id, devices: devices})
    }

    function getDeviceSymbol(deviceType: number){
        switch(deviceType){
            case 0:
                // Unknown
                return '❓'                
            case 1:
                // Network Monitor Server
                
            case 2:
                // Router
            case 3:
                // Computer
            case 4:
                // Cell Phone
            case 5:
                // Smart Home Device
            case 6:
                // TV
            case 7:
                // Game Console
        }
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
                        <tr onClick={() => showModal(device.id)} key={device.id + '-b'}>
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
                        <tr onClick={() => showModal(device.id)} key={device.id + '-a'}>
                            <td>{device.friendly_name}</td>
                            <td>{device.device_name}</td>
                            <td>
                                {(device.last_connected_date == lastQueryTime) ? <span>🟢</span> : <span>{dateToLocal(device.last_connected_date, true)}</span>}
                            </td>
                            <td><DeviceIcon deviceType={device.device_type} /></td>
                            <td>{(device.notify_on_connect) ? <span>✔</span> : <span></span>}</td>
                        </tr>
                    )}
                </tbody>
            </table>
        )
    }
}

export default DeviceTable
