/**
 * Monitor Dashboard - Clean and organized JavaScript
 */

class MonitorDashboard {
    constructor() {
        this.refreshInterval = null;
        this.init();
    }

    init() {
        this.loadInstanceInfo();
        this.loadServices();
        this.setupEventListeners();
        this.startAutoRefresh();
        
        // Load system overview
        const overviewContainer = document.getElementById('system-overview');
        if (overviewContainer) {
            this.loadInstanceInfo();
        }
    }

    setupEventListeners() {
        // Enter key support for service checker
        const hostInput = document.getElementById('check-host');
        const portInput = document.getElementById('check-port');
        const commonPorts = document.getElementById('common-ports');
        
        [hostInput, portInput].forEach(input => {
            input?.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.checkCustomService();
                }
            });
        });
        
        // Common ports dropdown handler
        commonPorts?.addEventListener('change', (e) => {
            if (e.target.value) {
                portInput.value = e.target.value;
            }
        });
    }

    startAutoRefresh() {
        // Auto-refresh services every 30 seconds
        this.refreshInterval = setInterval(() => {
            this.loadServices();
            this.showRefreshIndicator();
        }, 30000);
    }

    showRefreshIndicator() {
        const indicator = document.getElementById('refresh-indicator');
        if (indicator) {
            indicator.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i>';
            setTimeout(() => {
                indicator.innerHTML = '<i class="fas fa-hourglass-half"></i>';
            }, 600);
        }
    }

    // API Helper Methods
    async makeApiCall(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    }

    // Instance Information
    async loadInstanceInfo() {
        const container = document.getElementById('instance-info');
        const overviewContainer = document.getElementById('system-overview');
        if (!container && !overviewContainer) return;

        try {
            const data = await this.makeApiCall('/api/instance-info');
            if (container) {
                container.innerHTML = this.renderInstanceInfo(data);
            }
            if (overviewContainer) {
                overviewContainer.innerHTML = this.renderSystemOverview(data);
            }
        } catch (error) {
            const errorMsg = `<div class="error">Failed to load instance info: ${error.message}</div>`;
            if (container) container.innerHTML = errorMsg;
            if (overviewContainer) overviewContainer.innerHTML = errorMsg;
        }
    }

    renderSystemOverview(data) {
        const metrics = [
            { label: 'CPU Usage', value: data.cpu_usage || '0%', key: 'cpu_usage' },
            { label: 'Memory Usage', value: data.memory_usage || '0%', key: 'memory_usage' },
            { label: 'Disk Usage', value: data.disk_usage || '0%', key: 'disk_usage' },
            { label: 'Uptime', value: data.uptime || 'Unknown', key: 'uptime' }
        ];
        
        return metrics.map(metric => {
            const numValue = parseFloat(metric.value);
            const isPercentage = metric.value.includes('%');
            let progressClass = '';
            let progressWidth = '0%';
            
            if (isPercentage) {
                progressWidth = metric.value;
                if (numValue > 80) progressClass = 'error';
                else if (numValue > 60) progressClass = 'warning';
            }
            
            return `
                <div class="metric-card">
                    <div class="metric-value">${metric.value}</div>
                    <div class="metric-label">${metric.label}</div>
                    ${isPercentage ? `
                        <div class="progress-bar">
                            <div class="progress-fill ${progressClass}" style="width: ${progressWidth}"></div>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
    }
    
    renderInstanceInfo(data) {
        // Organize information into categories for tabs
        const sections = {
            'system': {
                title: 'System Information',
                fields: ['hostname', 'platform', 'platform_release', 'architecture', 'processor', 'container_type', 'cloud_provider']
            },
            'resources': {
                title: 'Resource Usage',
                fields: ['cpu_cores', 'cpu_threads', 'cpu_usage', 'cpu_frequency', 'memory_total', 'memory_used', 'memory_usage', 'memory_available']
            },
            'network': {
                title: 'Network Configuration',
                fields: ['private_ip', 'public_ip', 'network_interfaces']
            },
            'runtime': {
                title: 'Runtime Information',
                fields: ['uptime', 'boot_time', 'disk_total', 'disk_used', 'disk_free', 'disk_usage']
            }
        };

        let html = '';
        
        for (const [sectionId, section] of Object.entries(sections)) {
            const sectionItems = section.fields
                .filter(field => data[field] !== undefined && data[field] !== 'Unknown' && data[field] !== null)
                .map(field => {
                    let value = data[field];
                    let displayName = field.replace(/_/g, ' ');
                    
                    // Special formatting for certain fields
                    if (field === 'network_interfaces' && Array.isArray(value)) {
                        value = value.join('<br>');
                    }
                    if (field === 'processor' && value.length > 50) {
                        value = value.substring(0, 47) + '...';
                    }
                    
                    // Add icons for better visual hierarchy
                    const icons = {
                        'hostname': '<i class="fas fa-tag"></i>',
                        'platform': '<i class="fas fa-desktop"></i>',
                        'cpu_cores': '<i class="fas fa-microchip"></i>',
                        'cpu_usage': '<i class="fas fa-chart-line"></i>',
                        'memory_usage': '<i class="fas fa-memory"></i>',
                        'disk_usage': '<i class="fas fa-hdd"></i>',
                        'uptime': '<i class="fas fa-clock"></i>',
                        'private_ip': '<i class="fas fa-network-wired"></i>',
                        'public_ip': '<i class="fas fa-globe"></i>',
                        'container_type': '<i class="fas fa-box"></i>',
                        'cloud_provider': '<i class="fas fa-cloud"></i>',
                        'memory_total': '<i class="fas fa-memory"></i>',
                        'memory_used': '<i class="fas fa-memory"></i>',
                        'memory_available': '<i class="fas fa-memory"></i>',
                        'cpu_threads': '<i class="fas fa-microchip"></i>',
                        'cpu_frequency': '<i class="fas fa-microchip"></i>',
                        'disk_total': '<i class="fas fa-hdd"></i>',
                        'disk_used': '<i class="fas fa-hdd"></i>',
                        'disk_free': '<i class="fas fa-hdd"></i>',
                        'boot_time': '<i class="fas fa-power-off"></i>',
                        'architecture': '<i class="fas fa-cog"></i>',
                        'processor': '<i class="fas fa-microchip"></i>'
                    };
                    
                    const icon = icons[field] || '';
                    return `<tr><td>${icon} ${displayName}</td><td>${value}</td></tr>`;
                });
            
            const isActive = sectionId === 'system' ? 'active' : '';
            if (sectionItems.length > 0) {
                html += `
                    <div class="tab-section ${isActive}" id="tab-${sectionId}">
                        <table class="info-table">${sectionItems.join('')}</table>
                    </div>
                `;
            }
        }
        
        return html || '<div class="no-data">No system information available</div>';
    }

    // Services Management
    async loadServices() {
        const container = document.getElementById('services-list');
        if (!container) return;

        try {
            const data = await this.makeApiCall('/api/services');
            
            if (data.services && data.services.length > 0) {
                container.innerHTML = this.renderServices(data.services);
                
                // Check all services
                data.services.forEach(service => {
                    this.checkService(service.host, service.port, service.name);
                });
            } else {
                container.innerHTML = '<div class="no-data">No services configured</div>';
            }
        } catch (error) {
            container.innerHTML = `<div class="error">Failed to load services: ${error.message}</div>`;
        }
    }

    renderServices(services) {
        return services.map(service => `
            <div class="service-item" id="service-${service.name}">
                <span class="service-name">${service.name}</span>
                <span class="status checking">Checking</span>
                <button onclick="dashboard.recheckService('${service.host}', ${service.port}, '${service.name}')" 
                        class="small-button"><i class="fas fa-redo-alt"></i></button>
            </div>
        `).join('');
    }

    async checkService(host, port, name = null) {
        try {
            const data = await this.makeApiCall('/api/check-service', {
                method: 'POST',
                body: JSON.stringify({ host, port })
            });

            if (name) {
                this.updateServiceStatus(name, data);
            }

            return data;
        } catch (error) {
            console.error('Service check failed:', error);
            if (name) {
                this.updateServiceStatus(name, { status: 'error', message: error.message });
            }
            return { status: 'error', message: error.message };
        }
    }

    updateServiceStatus(name, data) {
        const statusElement = document.querySelector(`#service-${name} .status`);
        if (statusElement) {
            statusElement.className = `status ${data.status}`;
            statusElement.textContent = data.status.toUpperCase();
            statusElement.title = data.message;
        }
    }

    recheckService(host, port, name) {
        this.checkService(host, port, name);
    }

    // Custom Service Checker
    async checkCustomService() {
        const hostInput = document.getElementById('check-host');
        const portInput = document.getElementById('check-port');
        const resultDiv = document.getElementById('custom-check-result');

        if (!hostInput || !portInput || !resultDiv) return;

        const host = hostInput.value.trim();
        const port = portInput.value.trim();

        if (!host || !port) {
            this.showResult(resultDiv, 'error', 'Please enter both host and port');
            return;
        }

        this.showResult(resultDiv, 'checking', 'Checking connection...');

        try {
            const data = await this.checkService(host, port);
            this.showResult(resultDiv, data.status, `${data.status.toUpperCase()}: ${data.message}`);
        } catch (error) {
            this.showResult(resultDiv, 'error', `Error: ${error.message}`);
        }
    }

    showResult(container, status, message) {
        container.innerHTML = `<div class="result ${status}">${message}</div>`;
    }

    // Network Tools
    async getSystemInfo() {
        const resultDiv = document.getElementById('network-results');
        if (!resultDiv) return;

        resultDiv.innerHTML = '<div class="checking">Gathering system information...</div>';

        try {
            const data = await this.makeApiCall('/api/system-info');
            resultDiv.innerHTML = `<pre>${data.output || data.error || 'No output'}</pre>`;
        } catch (error) {
            resultDiv.innerHTML = `<div class="error">Failed to get system info: ${error.message}</div>`;
        }
    }

    async scanNetwork() {
        const resultDiv = document.getElementById('network-results');
        if (!resultDiv) return;

        resultDiv.innerHTML = '<div class="checking">Scanning network... (this may take a moment)</div>';

        try {
            const data = await this.makeApiCall('/api/network-scan', {
                method: 'POST',
                body: JSON.stringify({ target: 'localhost' })
            });
            resultDiv.innerHTML = `<pre>${data.output || data.error || 'No scan results'}</pre>`;
        } catch (error) {
            resultDiv.innerHTML = `<div class="error">Network scan failed: ${error.message}</div>`;
        }
    }

    // Utility Methods
    updateGlancesLink(event) {
        event.preventDefault();
        const currentHost = window.location.hostname;
        const port = window.location.port ? `:${window.location.port.replace('8080', '61208')}` : ':61208';
        window.open(`http://${currentHost}${port}`, '_blank');
    }

    cleanup() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
    }
}

// Tab switching functionality
function switchTab(tabName) {
    // Remove active class from all tabs and sections
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-section').forEach(section => section.classList.remove('active'));
    
    // Add active class to clicked tab and corresponding section
    event.target.classList.add('active');
    const section = document.getElementById(`tab-${tabName}`);
    if (section) {
        section.classList.add('active');
    }
}

// Global functions for HTML onclick handlers
let dashboard;

function loadInstanceInfo() {
    dashboard?.loadInstanceInfo();
}

function loadServices() {
    dashboard?.loadServices();
}

function checkCustomService() {
    dashboard?.checkCustomService();
}

function getSystemInfo() {
    dashboard?.getSystemInfo();
}

function scanNetwork() {
    dashboard?.scanNetwork();
}

function updateGlancesLink(event) {
    dashboard?.updateGlancesLink(event);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new MonitorDashboard();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    dashboard?.cleanup();
});