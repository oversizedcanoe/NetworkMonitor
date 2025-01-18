import { useEffect, useState } from 'react';
import './edit-device-modal.css'
import { ModalService } from '../../services/modal.service';
import { BackendService } from '../../services/backendservice';

function EditDeviceModal() {
    const [friendlyName, setFriendlyName] = useState('');
    const [deviceName, setDeviceName] = useState('');
    const [deviceType, setDeviceType] = useState(0);
    const [notifyOnConnect, setNotifyOnConnect] = useState(false);
    const [deviceId, setDeviceId] = useState(0);
    const [isOpen, setIsOpen] = useState(false);

    let devices: any[] = [];
    let selectedDevice: any = null;

    function setModalData(isOpen: boolean, modalData: any) {
        setDeviceId(modalData.id);
        devices = modalData.devices;
        selectedDevice = devices.filter(d => d.id == modalData.id)[0];
        setFriendlyName(selectedDevice.friendly_name ?? "");
        setDeviceName(selectedDevice.device_name ?? "");
        setDeviceType(selectedDevice.device_type);
        setNotifyOnConnect(Boolean(selectedDevice.notify_on_connect));
        setIsOpen(isOpen);
    }

    useEffect(() => {
        ModalService.setOpenFunction(setModalData);
        return () => {
            ModalService.setOpenFunction(() => { });
        };
    }, [isOpen]);

    useEffect(() => {
        function handleKeyDown(e: KeyboardEvent) {
            if (e.key == 'Escape') {
                close();
            }
        }

        document.addEventListener('keydown', handleKeyDown);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        }
    }, []);


    async function updateDevice() {
        const backendService = new BackendService();
        const result = await backendService.post('device/' + deviceId.toString(), { friendlyName: friendlyName, deviceType: deviceType, notify: notifyOnConnect });
        if (result == '') {
            location.reload();
        }
    }

    function close() {
        setFriendlyName('');
        setDeviceName('');
        setDeviceType(0);
        setNotifyOnConnect(false);
        setIsOpen(false);
    }

    return (
        <dialog {...(isOpen ? { open: true } : {})}>
            <article>
                <header>
                    <button aria-label="Close" rel="prev" onClick={close}></button>
                    <p><b>Edit Device {`${deviceId}`}</b></p>
                </header>
                <form>
                    <fieldset>
                        <label>
                            Friendly Name
                            <input name="friendlyName" placeholder="Friendly name" value={friendlyName} onChange={(e) => setFriendlyName(e.target.value)} />
                        </label>
                        <label>
                            Device Name
                            <input name="deviceName" placeholder="Device name" value={deviceName} disabled />
                        </label>
                        <label>
                            Device Type
                            <select name="deviceType" required defaultValue={""} value={deviceType} onChange={(e) => setDeviceType(parseInt(e.target.value))}>
                                <option value={""} disabled></option>
                                <option value={0}>Unknown</option>
                                <option value={1}>Network Monitor Server</option>
                                <option value={2}>Router</option>
                                <option value={3}>Computer</option>
                                <option value={4}>Cell Phone</option>
                                <option value={5}>Smart Home Device</option>
                                <option value={6}>TV</option>
                                <option value={7}>Game Console</option>
                            </select>
                        </label>
                        <label>
                            <input type="checkbox" name="notify" checked={notifyOnConnect} onChange={() => setNotifyOnConnect(!notifyOnConnect)} />
                            Notify on Connect
                        </label>
                    </fieldset>
                </form>
                <footer>
                    <button className="secondary" onClick={close}>Cancel</button>
                    <button onClick={updateDevice}>Confirm</button>
                </footer>
            </article>
        </dialog>
    )
}

export default EditDeviceModal