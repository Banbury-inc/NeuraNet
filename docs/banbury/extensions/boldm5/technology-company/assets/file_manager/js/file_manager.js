const devicesTab = document.querySelector('.devices-tab');
const filesTab = document.querySelector('.files-tab');
const mapTab = document.querySelector('.map-tab'); // New tab
const devicesSection = document.querySelector('.devices-section');
const filesSection = document.querySelector('.files-section');
const mapSection = document.querySelector('.map-section'); // New section

devicesTab.addEventListener('click', () => {
    devicesSection.classList.add('active');
    filesSection.classList.remove('active');
    mapSection.classList.remove('active'); // Remove 'active' from map section
});

filesTab.addEventListener('click', () => {
    filesSection.classList.add('active');
    devicesSection.classList.remove('active');
    mapSection.classList.remove('active'); // Remove 'active' from map section
});

mapTab.addEventListener('click', () => { // New event listener for the map tab
    mapSection.classList.add('active'); // Add 'active' to map section
    devicesSection.classList.remove('active');
    filesSection.classList.remove('active');
});

const addDeviceButton = document.querySelector('.add-device-button');

addDeviceButton.addEventListener('click', () => {
    // Implement your logic here to add a device or show a form
    // For now, let's just toggle the visibility of the devices section
    devicesSection.classList.toggle('active');
    filesSection.classList.remove('active');
    mapSection.classList.remove('active'); // Remove 'active' from map section
});

// Function to show the devices section and activate the devices tab
function openDevicesTab() {
    devicesSection.classList.add('active');
    filesSection.classList.remove('active');
    mapSection.classList.remove('active'); // Remove 'active' from map section
    devicesTab.classList.add('active'); // Add 'active' class to indicate it's selected
    filesTab.classList.remove('active');
    mapTab.classList.remove('active'); // Remove 'active' class from map tab
}

// Function to show the files section and activate the files tab
function openFilesTab() {
    filesSection.classList.add('active');
    devicesSection.classList.remove('active');
    mapSection.classList.remove('active'); // Remove 'active' from map section
    filesTab.classList.add('active'); // Add 'active' class to indicate it's selected
    devicesTab.classList.remove('active');
    mapTab.classList.remove('active'); // Remove 'active' class from map tab
}

// Function to show the map section and activate the map tab
function openMapTab() {
    mapSection.classList.add('active'); // Add 'active' to map section
    devicesSection.classList.remove('active');
    filesSection.classList.remove('active');
    mapTab.classList.add('active'); // Add 'active' class to indicate it's selected
    devicesTab.classList.remove('active');
    filesTab.classList.remove('active');
}

// Automatically open the devices tab when the page loads
window.addEventListener('load', () => {
    openDevicesTab();
});

// Add click event listeners to the tabs
devicesTab.addEventListener('click', openDevicesTab);
filesTab.addEventListener('click', openFilesTab);
mapTab.addEventListener('click', openMapTab); // New event listener for the map tab
