import { useEffect, useState } from 'react';
import './edit-device-modal.css'
import { ModalService } from '../../services/modal.service';

function EditDeviceModal() {
    const [deviceName, setDeviceName] = useState('');
    const [deviceType, setDeviceType] = useState(0);
    const [isOpen, setIsOpen] = useState(false);

    let devices: any[] = [];
    let id: number = 0;
    let selectedDevice: any = null;

    function setModalData(isOpen: boolean, modalData: any) {
        console.warn(modalData);
        devices = modalData.devices;
        id = modalData.id;
        selectedDevice = devices.filter(d => d.id == id)[0];
        setIsOpen(isOpen);
    }

    useEffect(() => {
        ModalService.setOpenFunction(setModalData);
        return () => {
            ModalService.setOpenFunction(() => { });
        };
    }, [isOpen]);

    function updateDevice() {
        alert(deviceName + ' ' + deviceType);
        close();
    }

    function close(){
        setDeviceName('');
        setDeviceType(0);
        setIsOpen(false);
    }

    return (
        <dialog {...(isOpen ? { open: true } : {})}>
            <article>
                <header>
                    <button aria-label="Close" rel="prev" onClick={close}></button>
                    <p><b>Edit Device {`${id}`}</b></p>
                </header>
                <form>
                    <fieldset>
                        <label>
                            Device Name
                            <input name="deviceName" placeholder="Device name" value={deviceName} onChange={(e) => setDeviceName(e.target.value)} />
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


