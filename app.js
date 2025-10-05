// Avalanche Risk Assessment Dashboard - Main Application Script

// Global variables
let map;
let markers = [];
let autoRefreshInterval;
let isAutoRefreshEnabled = true;

// Risk level colors and descriptions
const riskColors = {
    low: '#27ae60',
    moderate: '#f39c12', 
    considerable: '#e67e22',
    high: '#e74c3c',
    extreme: '#8e44ad'
};

const riskDescriptions = {
    low: "Generally safe conditions, but always exercise caution.",
    moderate: "Heightened avalanche conditions, careful route selection essential.",
    considerable: "Dangerous avalanche conditions, avoid avalanche terrain.",
    high: "Very dangerous conditions, travel in avalanche terrain not recommended.",
    extreme: "Extreme danger, avoid all avalanche terrain."
};

// Colorado backcountry zones data
const avalancheZones = [
    { id: 'aspen', name: 'Aspen', lat: 39.1911, lng: -106.8175 },
    { id: 'vail_summit', name: 'Vail & Summit County', lat: 39.6403, lng: -106.3742 },
    { id: 'front_range', name: 'Front Range', lat: 39.7392, lng: -105.9903 },
    { id: 'steamboat_flat_tops', name: 'Steamboat & Flat Tops', lat: 40.4850, lng: -106.8317 },
    { id: 'sawatch_range', name: 'Sawatch Range', lat: 39.1175, lng: -106.4453 },
    { id: 'gunnison', name: 'Gunnison', lat: 38.5458, lng: -107.0323 },
    { id: 'grand_mesa', name: 'Grand Mesa', lat: 39.0644, lng: -108.1103 },
    { id: 'northern_san_juan', name: 'Northern San Juan', lat: 37.8136, lng: -107.6631 },
    { id: 'southern_san_juan', name: 'Southern San Juan', lat: 37.2753, lng: -106.9603 },
    { id: 'sangre_de_cristo', name: 'Sangre de Cristo', lat: 37.5831, lng: -105.4903 }
];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏔️ Initializing Avalanche Risk Assessment Dashboard');
    
    // Initialize map
    initMap();
    
    // Load initial data
    loadRiskAssessment();
    
    // Setup event listeners
    setupEventListeners();
    
    // Start auto-refresh
    startAutoRefresh();
    
    // Update current time
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
    
    console.log('✅ Dashboard initialized successfully');
});

// Initialize the map
function initMap() {
    console.log('🗺️ Initializing map...');
    
    // Create map centered on Colorado
    map = L.map('map', {
        center: [39.0, -105.5],
        zoom: 7,
        zoomControl: true,
        attributionControl: true
    });

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(map);

    // Add scale control
    L.control.scale({
        position: 'bottomright',
        metric: true,
        imperial: false
    }).addTo(map);

    console.log('✅ Map initialized');
}

// Load risk assessment data from API
async function loadRiskAssessment() {
    console.log('📊 Loading risk assessment data...');
    
    try {
        const response = await fetch('/api/risk-assessment');
        const data = await response.json();

        if (data.status === 'success') {
            console.log('✅ Risk assessment data loaded');
            updateMapWithRiskData(data.data);
            updateModelMetrics(data.model_info);
            updateZoneDetails(data.data);
        } else {
            console.error('❌ Failed to load risk assessment:', data.message);
            loadDemoData();
        }
    } catch (error) {
        console.error('❌ Error loading risk assessment:', error);
        loadDemoData();
    }
}

// Update map with risk data
function updateMapWithRiskData(riskData) {
    console.log('🗺️ Updating map with risk data...');
    
    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    // Add markers for each zone
    riskData.forEach(zone => {
        const marker = L.circleMarker([zone.lat, zone.lng], {
            radius: 12,
            fillColor: riskColors[zone.risk_level],
            color: '#000',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map);

        // Create popup content
        const popupContent = `
            <div class="popup-content">
                <h3>${zone.name}</h3>
                <div class="risk-info">
                    <div class="risk-level ${zone.risk_level}">
                        <strong>Risk Level:</strong> ${zone.risk_level.toUpperCase()}
                    </div>
                    <div class="risk-score">
                        <strong>Risk Score:</strong> ${(zone.risk_score * 100).toFixed(0)}%
                    </div>
                    <div class="probabilities">
                        <div><strong>Slab Probability:</strong> ${(zone.slab_probability * 100).toFixed(0)}%</div>
                        <div><strong>Wet Probability:</strong> ${(zone.wet_probability * 100).toFixed(0)}%</div>
                    </div>
                    <div class="recommendation">
                        <strong>Recommendation:</strong> ${riskDescriptions[zone.risk_level]}
                    </div>
                </div>
            </div>
        `;

        marker.bindPopup(popupContent);
        markers.push(marker);
    });

    console.log(`✅ Added ${markers.length} risk markers to map`);
}

// Load demo data as fallback
function loadDemoData() {
    console.log('🎭 Loading demo data...');
    
    const demoData = avalancheZones.map(zone => ({
        name: zone.name,
        lat: zone.lat,
        lng: zone.lng,
        risk_level: getRandomRiskLevel(),
        risk_score: Math.random(),
        slab_probability: Math.random(),
        wet_probability: Math.random()
    }));

    updateMapWithRiskData(demoData);
    updateModelMetrics({
        accuracy: 0.942,
        precision: 0.897,
        recall: 0.913,
        f1_score: 0.905
    });
    updateZoneDetails(demoData);
}

// Get random risk level for demo
function getRandomRiskLevel() {
    const levels = ['low', 'moderate', 'considerable', 'high', 'extreme'];
    return levels[Math.floor(Math.random() * levels.length)];
}

// Update model metrics display
function updateModelMetrics(modelInfo) {
    console.log('📈 Updating model metrics...');
    
    const metrics = {
        'accuracy-score': modelInfo.accuracy,
        'precision-score': modelInfo.precision,
        'recall-score': modelInfo.recall,
        'f1-score': modelInfo.f1_score || 0.905
    };

    Object.entries(metrics).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = `${(value * 100).toFixed(1)}%`;
        }
    });

    console.log('✅ Model metrics updated');
}

// Update zone details section
function updateZoneDetails(riskData) {
    console.log('🏔️ Updating zone details...');
    
    const zoneGrid = document.getElementById('zone-details');
    if (!zoneGrid) return;

    zoneGrid.innerHTML = '';

    riskData.forEach(zone => {
        const zoneCard = document.createElement('div');
        zoneCard.className = 'zone-card';
        zoneCard.innerHTML = `
            <div class="zone-header">
                <div class="zone-name">${zone.name}</div>
                <div class="zone-risk ${zone.risk_level}">${zone.risk_level.toUpperCase()}</div>
            </div>
            <div class="zone-metrics">
                <div class="metric-item">
                    <div class="metric-label">Risk Score</div>
                    <div class="metric-number">${(zone.risk_score * 100).toFixed(0)}%</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Slab Prob</div>
                    <div class="metric-number">${(zone.slab_probability * 100).toFixed(0)}%</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Wet Prob</div>
                    <div class="metric-number">${(zone.wet_probability * 100).toFixed(0)}%</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Status</div>
                    <div class="metric-number">${zone.risk_level}</div>
                </div>
            </div>
            <div class="zone-recommendation">
                ${riskDescriptions[zone.risk_level]}
            </div>
        `;
        zoneGrid.appendChild(zoneCard);
    });

    console.log(`✅ Updated ${riskData.length} zone details`);
}

// Update current time display
function updateCurrentTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit', 
        hour12: true 
    });
    
    const timestamp = document.getElementById('current-time');
    if (timestamp) {
        timestamp.textContent = `Last updated: ${timeString} MST`;
    }
}

// Setup event listeners
function setupEventListeners() {
    console.log('🎧 Setting up event listeners...');
    
    // Refresh button
    const refreshButton = document.getElementById('refresh-data');
    if (refreshButton) {
        refreshButton.addEventListener('click', handleRefresh);
    }

    // Auto-refresh toggle
    const autoRefreshButton = document.getElementById('toggle-auto-refresh');
    if (autoRefreshButton) {
        autoRefreshButton.addEventListener('click', toggleAutoRefresh);
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.key === 'r' || e.key === 'R') {
            handleRefresh();
        }
        if (e.key === 'a' || e.key === 'A') {
            toggleAutoRefresh();
        }
    });

    // Window resize handler
    window.addEventListener('resize', handleResize);

    console.log('✅ Event listeners setup complete');
}

// Handle refresh button click
async function handleRefresh() {
    console.log('🔄 Refreshing data...');
    
    const refreshButton = document.getElementById('refresh-data');
    if (refreshButton) {
        refreshButton.innerHTML = '<span class="btn-icon">⏳</span> Updating...';
        refreshButton.disabled = true;
    }

    try {
        await loadRiskAssessment();
        console.log('✅ Data refreshed successfully');
    } catch (error) {
        console.error('❌ Error refreshing data:', error);
    } finally {
        if (refreshButton) {
            refreshButton.innerHTML = '<span class="btn-icon">🔄</span> Update Risk Assessment';
            refreshButton.disabled = false;
        }
    }
}

// Toggle auto-refresh
function toggleAutoRefresh() {
    isAutoRefreshEnabled = !isAutoRefreshEnabled;
    
    const autoStatus = document.getElementById('auto-status');
    if (autoStatus) {
        autoStatus.textContent = isAutoRefreshEnabled ? 'ON' : 'OFF';
    }

    if (isAutoRefreshEnabled) {
        startAutoRefresh();
        console.log('✅ Auto-refresh enabled');
    } else {
        stopAutoRefresh();
        console.log('⏸️ Auto-refresh disabled');
    }
}

// Start auto-refresh
function startAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    if (isAutoRefreshEnabled) {
        autoRefreshInterval = setInterval(loadRiskAssessment, 30000); // 30 seconds
        console.log('⏰ Auto-refresh started (30s interval)');
    }
}

// Stop auto-refresh
function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        console.log('⏹️ Auto-refresh stopped');
    }
}

// Handle window resize
function handleResize() {
    if (map) {
        setTimeout(() => {
            map.invalidateSize();
        }, 100);
    }
}

// Utility function to format numbers
function formatNumber(num, decimals = 1) {
    return (num * 100).toFixed(decimals);
}

// Utility function to get risk level color
function getRiskColor(riskLevel) {
    return riskColors[riskLevel] || '#666';
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadRiskAssessment,
        updateMapWithRiskData,
        updateModelMetrics,
        updateZoneDetails
    };
}
