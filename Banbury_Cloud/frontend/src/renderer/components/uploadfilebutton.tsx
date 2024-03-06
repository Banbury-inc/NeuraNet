import * as React from 'react';
import { exec } from "child_process";
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const InputFileUploadButton: React.FC = () => {
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;
    if (!file) {
      console.log("No file selected.");
      return;
    }

    console.log("File:", file);
    // Log the file name for debugging purposes
    console.log("Selected file:", file.name);

    // Run the Python script with the selected file
    runPythonScript(file);
  };

  const runPythonScript = async (file: File) => {

      const scriptPath = 'src/main/upload.py'; // Update this to the path of your Python script
       
      exec(`python "${scriptPath}" "${file.path}"`, (error, stdout, stderr) => {
      console.log(File)
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          return
        }
        if (stdout) {
          console.log(`Python Script Message: ${stdout}`);
          return
        }
        console.log(`Python Script Message: ${stdout}`);

      });
 
    } 



  return (
    <Button component="label" variant="outlined" size="small">
      Upload file
      <VisuallyHiddenInput
        type="file"
        onChange={handleFileChange}
        // If you want to handle multiple files, you might consider adding the "multiple" attribute
      />
    </Button>
  );
};

export default InputFileUploadButton;

