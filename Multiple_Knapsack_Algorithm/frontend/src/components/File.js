import React, { useState, useEffect } from 'react';

const File = () => {
    const [files, setFiles] = useState([]);

    useEffect(() => {
        // Fetch files from the backend API
        fetch('/files')
            .then(response => response.json())
            .then(data => setFiles(data))
            .catch(error => console.error('Error fetching files:', error));
    }, []);

    return (
        <div>
            <h2>Files</h2>
            <ul>
                {files.map(file => (
                    <li key={file.id}>{file.name} (Size: {file.size} MB)</li>
                ))}
            </ul>
        </div>
    );
};

export default File;
