// In a React component, e.g., OutputDisplay.tsx
import React, { useEffect, useState } from 'react';

const OutputDisplay: React.FC = () => {
    const [scriptOutput, setScriptOutput] = useState<string>('');

    useEffect(() => {
        // Listen for the Python script's output
        window.electronAPI.onPythonOutput((output: string) => {
            setScriptOutput(output);
        });
    }, []);

    return (
        <div>
            <p>Python Script Output:</p>
            <pre>{scriptOutput}</pre>
        </div>
    );
};

export default OutputDisplay;

