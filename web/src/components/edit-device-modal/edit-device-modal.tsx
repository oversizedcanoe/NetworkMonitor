import { useEffect, useState } from 'react';
import './edit-device-modal.css'

function EditDeviceModal() {

    return (
        <dialog open>
            <article>
                <h2>Confirm Your Membership</h2>
                <p>
                    Thank you for signing up for a membership!
                    Please review the membership details below:
                </p>
                <ul>
                    <li>Membership: Individual</li>
                    <li>Price: $10</li>
                </ul>
                <footer>
                    <button className="secondary">
                        Cancel
                    </button>
                    <button>Confirm</button>
                </footer>
            </article>
        </dialog>
    )
}

export default EditDeviceModal


