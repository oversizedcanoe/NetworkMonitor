import Spinner from '../spinner/spinner'
import './header.css'

interface HeaderProps {
  lastQueryTime: Date
}

function Header({ lastQueryTime }: HeaderProps) {

  return (
    <header>
        <div className="container">
          <hgroup>
            <h1 className='inline'>Netw<Spinner/>rk M<Spinner/>nit<Spinner/>r</h1>
            <p>Monitor your local network </p>
          </hgroup>
        </div>
    </header>
  )
}

export default Header
