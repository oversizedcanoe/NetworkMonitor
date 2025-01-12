import './App.css'
import Expansion from './components/expansion/expansion'
import Header from './components/header/header'

function App() {

  return (
    <>
      <Header />
      <main className='container'>
        <article>
          <p>Last Query Time:</p>
        </article>		
        <Expansion title='Quick View' isOpen={true}>
          {/* <DeviceTable/> */}
        </Expansion>
        <Expansion title='Detailed View' isOpen={false}>
          {/* <DeviceTable/> */}
        </Expansion>
      </main>
    </>
  )
}

export default App
