import React, { useState, useEffect } from 'react';

const Device = () => {
    const [devices, setDevices] = useState([]);

    useEffect(() => {
        // Fetch devices from the backend API
        fetch('/devices')
            .then(response => response.json())
            .then(data => setDevices(data))
            .catch(error => console.error('Error fetching devices:', error));
    }, []);

    return (
        <div>
            <h2>Devices</h2>
            <ul>
                {devices.map(device => (
                    <li key={device.id}>{device.name} (Storage Capacity: {device.storage_capacity} GB)</li>
                ))}
            </ul>
        </div>
    );
};

export default Device;
