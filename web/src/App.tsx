import { useEffect, useState } from 'react'
import './App.css'
import Accordian from './components/accordian/accordian'
import Header from './components/header/header'
import { BackendService } from './services/backendservice'
import DeviceTable from './components/device-table/device-table'
import { dateToLocal } from './utility/helper'
import EditDeviceModal from './components/edit-device-modal/edit-device-modal'

function App() {
  const [devices, setDevices] = useState([])
  const [lastQueryTime, setLastQueryTime] = useState(new Date())
  const [sleepTime, setSleepTime] = useState(0)
  const backendService = new BackendService();

  useEffect(() => {
    const getDevices = async () => {
      const apiResult = await backendService.get<[]>('device');
      if (apiResult) {
        setDevices(apiResult);
      }
    };

    getDevices();
  }, []);

  useEffect(() => {
    const getLastQueryTime = async () => {
      const apiResult = await backendService.get<Date>('monitor/lastquerytime');
      if (apiResult) {
        setLastQueryTime(apiResult);
      }
    };

    getLastQueryTime();
  }, []);

  useEffect(() => {
    const getSleepTime = async () => {
      const apiResult = await backendService.get<number>('monitor/sleeptime');
      if (apiResult) {
        setSleepTime(apiResult);
      }
    };

    getSleepTime();
  }, []);



  return (
    <>
      <Header lastQueryTime={lastQueryTime} />
      <main className='container'>
        <article>
          <p><b>Last Query Time:</b> {dateToLocal(lastQueryTime)}</p>
          <p><b>Query Delay (s):</b> {sleepTime}</p>
        </article>
        <Accordian title='Quick View' isOpen={true}  >
          <DeviceTable devices={devices} lastQueryTime={lastQueryTime} isDetailTable={false} />
        </Accordian>
        <Accordian title='Detailed View' isOpen={false}>
          <DeviceTable devices={devices} lastQueryTime={lastQueryTime} isDetailTable={true} />
        </Accordian>
      </main>
      <EditDeviceModal/>
    </>
  )
}

export default App
