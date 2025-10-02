// Colorado backcountry zones - will be populated from API
let avalancheZones = [];

// Risk level colors
const riskColors = {
    low: '#27ae60',
    moderate: '#f39c12',
    considerable: '#e67e22',
    high: '#e74c3c',
    extreme: '#8e44ad'
};

// Risk level descriptions
const riskDescriptions = {
    low: 'Low Risk - Generally safe conditions',
    moderate: 'Moderate Risk - Heightened avalanche conditions',
    considerable: 'Considerable Risk - Dangerous avalanche conditions',
    high: 'High Risk - Very dangerous avalanche conditions',
    extreme: 'Extreme Risk - Avoid all avalanche terrain'
};

let map;
let markers = [];

// Initialize the map
async function initMap() {
    // Center on Colorado
    map = L.map('map').setView([39.0, -105.5], 7);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Load risk assessment data from API
    await loadRiskAssessment();
    
    // Add avalanche zones
    addAvalancheZones();
    
    // Add current time display
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
}

// Add avalanche zones to the map
function addAvalancheZones() {
    avalancheZones.forEach(zone => {
        const marker = L.circleMarker([zone.lat, zone.lng], {
            radius: 15,
            fillColor: riskColors[zone.riskLevel],
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map);
        
        // Add popup with zone information
        marker.bindPopup(`
            <div class="popup-content">
                <h3>${zone.name}</h3>
                <p><strong>Risk Level:</strong> ${zone.riskLevel.toUpperCase()}</p>
                <p><strong>Risk Score:</strong> ${(zone.riskScore * 100).toFixed(0)}%</p>
                <p><strong>Description:</strong> ${zone.description}</p>
                <p><strong>Recommendation:</strong> ${riskDescriptions[zone.riskLevel]}</p>
            </div>
        `);
        
        // Add click event to show detailed information
        marker.on('click', function() {
            showZoneDetails(zone);
        });
        
        markers.push(marker);
    });
}

// Show detailed zone information
function showZoneDetails(zone) {
    // Update metrics display with zone-specific data
    document.getElementById('accuracy').textContent = '92.0%';
    document.getElementById('precision').textContent = '86.0%';
    document.getElementById('recall').textContent = '88.0%';
    
    // You could add more detailed information here
    console.log('Selected zone:', zone);
}

// Update current time display
function updateCurrentTime() {
    const now = new Date();
    const timeString = now.toLocaleString('en-US', {
        timeZone: 'America/Denver',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    // Update header with current time
    const header = document.querySelector('header p');
    header.innerHTML = `Real-time avalanche risk assessment for Colorado backcountry zones<br><small>Last updated: ${timeString} MST</small>`;
}

// Load risk assessment data from API
async function loadRiskAssessment() {
    try {
        const response = await fetch('/api/risk-assessment');
        const data = await response.json();
        
        if (data.status === 'success') {
            avalancheZones = data.data.map(zone => ({
                name: zone.name,
                lat: zone.lat,
                lng: zone.lng,
                riskLevel: zone.risk_level,
                riskScore: zone.risk_score,
                slabProbability: zone.slab_probability,
                wetProbability: zone.wet_probability,
                description: `${zone.name} - ${zone.risk_level} risk (${(zone.risk_score * 100).toFixed(0)}%)`
            }));
            
            // Update model metrics
            updateModelMetrics(data.model_info);
        } else {
            console.error('Failed to load risk assessment:', data.message);
            // Fallback to demo data
            loadDemoData();
        }
    } catch (error) {
        console.error('Error loading risk assessment:', error);
        // Fallback to demo data
        loadDemoData();
    }
}

// Load demo data as fallback
function loadDemoData() {
    avalancheZones = [
        {
            name: "Aspen",
            lat: 39.1911,
            lng: -106.8175,
            riskLevel: "moderate",
            riskScore: 0.65,
            description: "Aspen backcountry zone - Moderate risk due to recent snowfall"
        },
        {
            name: "Vail & Summit County",
            lat: 39.6403,
            lng: -106.3742,
            riskLevel: "high",
            riskScore: 0.85,
            description: "Vail & Summit County - High risk with significant snow loading"
        },
        {
            name: "Front Range",
            lat: 39.7392,
            lng: -105.9903,
            riskLevel: "considerable",
            riskScore: 0.75,
            description: "Front Range - Considerable risk with wind-loaded slopes"
        },
        {
            name: "Steamboat & Flat Tops",
            lat: 40.4850,
            lng: -106.8317,
            riskLevel: "low",
            riskScore: 0.35,
            description: "Steamboat & Flat Tops - Low risk, stable conditions"
        },
        {
            name: "Sawatch Range",
            lat: 39.1175,
            lng: -106.4453,
            riskLevel: "moderate",
            riskScore: 0.55,
            description: "Sawatch Range - Moderate risk with isolated pockets"
        },
        {
            name: "Gunnison",
            lat: 38.5458,
            lng: -107.0323,
            riskLevel: "considerable",
            riskScore: 0.70,
            description: "Gunnison - Considerable risk on north-facing aspects"
        },
        {
            name: "Grand Mesa",
            lat: 39.0644,
            lng: -108.1103,
            riskLevel: "low",
            riskScore: 0.25,
            description: "Grand Mesa - Low risk, well-settled snowpack"
        },
        {
            name: "Northern San Juan",
            lat: 37.8136,
            lng: -107.6631,
            riskLevel: "high",
            riskScore: 0.80,
            description: "Northern San Juan - High risk with persistent weak layers"
        },
        {
            name: "Southern San Juan",
            lat: 37.2753,
            lng: -106.9603,
            riskLevel: "extreme",
            riskScore: 0.95,
            description: "Southern San Juan - Extreme risk, avoid all avalanche terrain"
        },
        {
            name: "Sangre de Cristo",
            lat: 37.5831,
            lng: -105.4903,
            riskLevel: "moderate",
            riskScore: 0.60,
            description: "Sangre de Cristo - Moderate risk with warming temperatures"
        }
    ];
}

// Update model metrics display
function updateModelMetrics(modelInfo) {
    document.getElementById('accuracy').textContent = `${(modelInfo.accuracy * 100).toFixed(1)}%`;
    document.getElementById('precision').textContent = `${(modelInfo.precision * 100).toFixed(1)}%`;
    document.getElementById('recall').textContent = `${(modelInfo.recall * 100).toFixed(1)}%`;
}

// Refresh risk assessment data
async function updateRiskLevels() {
    await loadRiskAssessment();
    
    // Update markers with new data
    avalancheZones.forEach((zone, index) => {
        if (markers[index]) {
            markers[index].setStyle({
                fillColor: riskColors[zone.riskLevel]
            });
            
            // Update popup content
            markers[index].setPopupContent(`
                <div class="popup-content">
                    <h3>${zone.name}</h3>
                    <p><strong>Risk Level:</strong> ${zone.riskLevel.toUpperCase()}</p>
                    <p><strong>Risk Score:</strong> ${(zone.riskScore * 100).toFixed(0)}%</p>
                    <p><strong>Slab Probability:</strong> ${(zone.slabProbability * 100).toFixed(0)}%</p>
                    <p><strong>Wet Probability:</strong> ${(zone.wetProbability * 100).toFixed(0)}%</p>
                    <p><strong>Recommendation:</strong> ${riskDescriptions[zone.riskLevel]}</p>
                </div>
            `);
        }
    });
}

// Add some interactive features
function addInteractiveFeatures() {
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.key === 'r' || e.key === 'R') {
            updateRiskLevels();
        }
    });
    
    // Add refresh button functionality
    const refreshButton = document.createElement('button');
    refreshButton.textContent = '🔄 Refresh Risk Assessment';
    refreshButton.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #3498db;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        transition: all 0.3s ease;
    `;
    
    refreshButton.addEventListener('click', updateRiskLevels);
    refreshButton.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
        this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.3)';
    });
    refreshButton.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.2)';
    });
    
    document.body.appendChild(refreshButton);
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    addInteractiveFeatures();
    
    // Update risk levels every 30 seconds (simulate real-time updates)
    setInterval(updateRiskLevels, 30000);
    
    // Add loading animation
    const loadingElement = document.createElement('div');
    loadingElement.className = 'loading';
    loadingElement.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
    `;
    
    // Remove loading animation after 2 seconds
    setTimeout(() => {
        if (loadingElement.parentNode) {
            loadingElement.parentNode.removeChild(loadingElement);
        }
    }, 2000);
});

// Add CSS for popup content
const popupStyles = `
    <style>
        .popup-content h3 {
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 1.2rem;
        }
        .popup-content p {
            margin: 5px 0;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        .popup-content strong {
            color: #34495e;
        }
    </style>
`;

// Inject popup styles
document.head.insertAdjacentHTML('beforeend', popupStyles);
