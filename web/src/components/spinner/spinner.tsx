import { useEffect, useState } from 'react';
import './spinner.css'

function Spinner() {
    const [tickValue, setTickValue] = useState('◓');

    useEffect(() => {
        const interval = setInterval(() => {
            setTickValue(getNext(tickValue))
        }, 1000);

        return () => clearInterval(interval);
    }, [tickValue]);

    function getNext(symbol: string): string {
        //◓◑◒◐
        switch (symbol) {
            case '◓':
                return '◑'
            case '◑':
                return '◒'
            case '◒':
                return '◐'
            case '◐':
            default:
                return '◓'
        }
    }

    return (
        <span id='ticker'>{`${tickValue}`}</span>
    )
}

export default Spinner


