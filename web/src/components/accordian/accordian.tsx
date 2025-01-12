import { ReactNode } from 'react';
import './accordian.css'

interface AccordianProps {
    isOpen: boolean;
    title: string;
    children: ReactNode;
}

function Accordian({isOpen, title, children}: AccordianProps) {

  return (
    <article>
        <details {...(isOpen? { open: true} : {})}>
            <summary>{title}</summary>
            {children}
        </details>
    </article>
  )
}

export default Accordian
