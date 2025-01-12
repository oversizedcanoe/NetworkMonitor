import './expansion.css'

interface ExpansionProps {
    isOpen: boolean;
    title: string;
}

function Expansion({isOpen, title}: ExpansionProps) {

  return (
    <article>
        <details {...(isOpen? { open: true} : {})}>
            <summary>{title}</summary>
            <slot/>
        </details>
    </article>
  )
}

export default Expansion
