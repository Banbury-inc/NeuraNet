


const devicesTab = document.querySelector('.devices-tab');
const filesTab = document.querySelector('.files-tab');
const devicesSection = document.querySelector('.devices-section');
const filesSection = document.querySelector('.files-section');

devicesTab.addEventListener('click', () => {
    devicesSection.classList.add('active');
    filesSection.classList.remove('active');
});

filesTab.addEventListener('click', () => {
    filesSection.classList.add('active');
    devicesSection.classList.remove('active');
});

const addDeviceButton = document.querySelector('.add-device-button');


addDeviceButton.addEventListener('click', () => {
    // Implement your logic here to add a device or show a form
    // For now, let's just toggle the visibility of the devices section
    devicesSection.classList.toggle('active');
    filesSection.classList.remove('active');
});

// Function to show the devices section and activate the devices tab
function openDevicesTab() {
    devicesSection.classList.add('active');
    filesSection.classList.remove('active');
    devicesTab.classList.add('active'); // Add 'active' class to indicate it's selected
    filesTab.classList.remove('active');
}

// Function to show the files section and activate the files tab
function openFilesTab() {
    filesSection.classList.add('active');
    devicesSection.classList.remove('active');
    filesTab.classList.add('active'); // Add 'active' class to indicate it's selected
    devicesTab.classList.remove('active');
}

// Automatically open the devices tab when the page loads
window.addEventListener('load', () => {
    openDevicesTab();
});

// Add click event listeners to the tabs
devicesTab.addEventListener('click', openDevicesTab);
filesTab.addEventListener('click', openFilesTab);