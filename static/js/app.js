// Automated Diagnostic System - Main JavaScript

// Theme management
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme();
        this.bindEventListeners();
    }

    applyTheme() {
        const html = document.documentElement;
        if (this.theme === 'dark') {
            html.classList.add('dark');
        } else {
            html.classList.remove('dark');
        }
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', this.theme);
        this.applyTheme();
    }

    bindEventListeners() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
    }
}

// Form enhancement
class FormEnhancer {
    constructor() {
        this.init();
    }

    init() {
        this.enhanceSymptomForm();
        this.enhanceExampleBundles();
        this.addFormValidation();
        this.addAccessibilityFeatures();
    }

    enhanceSymptomForm() {
        const symptomCheckboxes = document.querySelectorAll('input[name="symptoms"]');
        const symptomText = document.getElementById('symptoms_text');
        
        if (symptomCheckboxes.length > 0) {
            // Add counter for selected symptoms
            this.addSymptomCounter(symptomCheckboxes);
            
            // Add search functionality
            this.addSymptomSearch(symptomCheckboxes);
            
            // Add clear all functionality
            this.addClearAllButton(symptomCheckboxes);
        }

        // Auto-resize textarea
        if (symptomText) {
            this.autoResizeTextarea(symptomText);
        }
    }

    addSymptomCounter(checkboxes) {
        const counterContainer = document.createElement('div');
        counterContainer.className = 'mb-4 text-sm text-winter-600 dark:text-winter-400';
        counterContainer.innerHTML = `
            <span id="symptom-counter">0 symptoms selected</span>
            <button type="button" id="clear-all-symptoms" class="ml-4 text-red-600 dark:text-red-400 hover:underline hidden">
                Clear all
            </button>
        `;
        
        const symptomContainer = checkboxes[0].closest('.grid').parentNode;
        symptomContainer.insertBefore(counterContainer, symptomContainer.querySelector('.grid'));
        
        const counter = document.getElementById('symptom-counter');
        const clearButton = document.getElementById('clear-all-symptoms');
        
        const updateCounter = () => {
            const checked = Array.from(checkboxes).filter(cb => cb.checked).length;
            counter.textContent = `${checked} symptom${checked !== 1 ? 's' : ''} selected`;
            
            if (checked > 0) {
                clearButton.classList.remove('hidden');
            } else {
                clearButton.classList.add('hidden');
            }
        };
        
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateCounter);
        });
        
        clearButton.addEventListener('click', () => {
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
            updateCounter();
        });
        
        updateCounter();
    }

    addSymptomSearch(checkboxes) {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'mb-4';
        searchContainer.innerHTML = `
            <div class="relative">
                <input type="text" id="symptom-search" placeholder="Search symptoms..." 
                       class="w-full px-4 py-2 pl-10 rounded-lg border border-winter-300 dark:border-winter-600 bg-white dark:bg-winter-700 text-winter-900 dark:text-winter-100 focus:ring-2 focus:ring-ice-500 focus:border-ice-500 transition-colors">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i data-feather="search" class="w-5 h-5 text-winter-400"></i>
                </div>
            </div>
        `;
        
        const symptomContainer = checkboxes[0].closest('.grid').parentNode;
        symptomContainer.insertBefore(searchContainer, symptomContainer.querySelector('.grid'));
        
        // Re-render feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
        
        const searchInput = document.getElementById('symptom-search');
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            
            checkboxes.forEach(checkbox => {
                const label = checkbox.closest('label');
                const text = label.textContent.toLowerCase();
                
                if (text.includes(searchTerm)) {
                    label.style.display = '';
                } else {
                    label.style.display = 'none';
                }
            });
        });
    }

    addClearAllButton(checkboxes) {
        // This is handled in addSymptomCounter method
    }

    enhanceExampleBundles() {
        const exampleBundles = document.querySelectorAll('.example-bundle');
        
        exampleBundles.forEach(bundle => {
            bundle.addEventListener('click', () => {
                const symptoms = bundle.dataset.symptoms.split(',');
                const checkboxes = document.querySelectorAll('input[name="symptoms"]');
                
                // Clear all checkboxes first
                checkboxes.forEach(checkbox => {
                    checkbox.checked = false;
                });
                
                // Check the relevant symptoms
                symptoms.forEach(symptom => {
                    const checkbox = document.querySelector(`input[name="symptoms"][value="${symptom}"]`);
                    if (checkbox) {
                        checkbox.checked = true;
                    }
                });
                
                // Trigger change event to update counter
                const firstCheckbox = document.querySelector('input[name="symptoms"]');
                if (firstCheckbox) {
                    firstCheckbox.dispatchEvent(new Event('change'));
                }
                
                // Show visual feedback
                bundle.classList.add('bg-ice-100', 'dark:bg-ice-900/40');
                setTimeout(() => {
                    bundle.classList.remove('bg-ice-100', 'dark:bg-ice-900/40');
                }, 500);
                
                // Scroll to symptom section
                const symptomSection = document.querySelector('input[name="symptoms"]').closest('.bg-white\\/60, .dark\\:bg-winter-800\\/60');
                if (symptomSection) {
                    symptomSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }

    autoResizeTextarea(textarea) {
        const resize = () => {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        };
        
        textarea.addEventListener('input', resize);
        
        // Initial resize
        setTimeout(resize, 100);
    }

    addFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    validateForm(form) {
        const symptomCheckboxes = form.querySelectorAll('input[name="symptoms"]');
        const symptomText = form.querySelector('input[name="symptoms_text"], textarea[name="symptoms_text"]');
        
        // Check if this is the main diagnosis form
        if (symptomCheckboxes.length > 0) {
            const hasSelectedSymptoms = Array.from(symptomCheckboxes).some(cb => cb.checked);
            const hasTextSymptoms = symptomText && symptomText.value.trim().length > 0;
            
            if (!hasSelectedSymptoms && !hasTextSymptoms) {
                this.showError('Please select symptoms or describe how you feel.');
                return false;
            }
        }
        
        // Validate required radio buttons
        const requiredRadios = form.querySelectorAll('input[type="radio"][required]');
        const radioGroups = new Set();
        
        requiredRadios.forEach(radio => {
            radioGroups.add(radio.name);
        });
        
        for (const groupName of radioGroups) {
            const groupRadios = form.querySelectorAll(`input[name="${groupName}"]`);
            const isChecked = Array.from(groupRadios).some(radio => radio.checked);
            
            if (!isChecked) {
                this.showError('Please answer all required questions.');
                return false;
            }
        }
        
        return true;
    }

    addAccessibilityFeatures() {
        // Add keyboard navigation for custom elements
        const interactiveElements = document.querySelectorAll('.example-bundle, button, [role="button"]');
        
        interactiveElements.forEach(element => {
            element.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    element.click();
                }
            });
            
            // Ensure elements are focusable
            if (!element.hasAttribute('tabindex')) {
                element.setAttribute('tabindex', '0');
            }
        });
        
        // Add ARIA labels where needed
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            const label = checkbox.closest('label');
            if (label && !checkbox.hasAttribute('aria-label')) {
                const labelText = label.textContent.trim();
                checkbox.setAttribute('aria-label', labelText);
            }
        });
    }

    showError(message) {
        // Create or update error message
        let errorDiv = document.getElementById('form-error');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'form-error';
            errorDiv.className = 'fixed top-4 left-1/2 transform -translate-x-1/2 bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg shadow-lg z-50 max-w-md';
            document.body.appendChild(errorDiv);
        }
        
        errorDiv.innerHTML = `
            <div class="flex items-center">
                <i data-feather="alert-circle" class="w-5 h-5 mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Re-render feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (errorDiv && errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

// Loading states manager
class LoadingManager {
    constructor() {
        this.init();
    }

    init() {
        this.addLoadingStates();
    }

    addLoadingStates() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitButton = form.querySelector('button[type="submit"]');
                if (submitButton) {
                    this.showLoading(submitButton);
                }
            });
        });
    }

    showLoading(button) {
        const originalText = button.innerHTML;
        button.disabled = true;
        button.innerHTML = `
            <div class="flex items-center justify-center">
                <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                Processing...
            </div>
        `;
        
        // Store original text for potential restoration
        button.dataset.originalText = originalText;
    }

    hideLoading(button) {
        if (button.dataset.originalText) {
            button.innerHTML = button.dataset.originalText;
            button.disabled = false;
            delete button.dataset.originalText;
        }
    }
}

// Performance monitoring
class PerformanceMonitor {
    constructor() {
        this.init();
    }

    init() {
        // Monitor page load performance
        window.addEventListener('load', () => {
            if ('performance' in window) {
                const perfData = performance.timing;
                const loadTime = perfData.loadEventEnd - perfData.navigationStart;
                console.log(`Page load time: ${loadTime}ms`);
                
                // Log slow loads (> 3 seconds)
                if (loadTime > 3000) {
                    console.warn('Slow page load detected');
                }
            }
        });
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all managers
    new ThemeManager();
    new FormEnhancer();
    new LoadingManager();
    new PerformanceMonitor();
    
    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add focus management for accessibility
    const focusableElements = document.querySelectorAll(
        'a[href], area[href], input:not([disabled]), select:not([disabled]), ' +
        'textarea:not([disabled]), button:not([disabled]), iframe, object, embed, ' +
        '[tabindex="0"], [contenteditable]'
    );
    
    // Handle focus indicators
    focusableElements.forEach(element => {
        element.addEventListener('focus', () => {
            element.classList.add('focus-visible');
        });
        
        element.addEventListener('blur', () => {
            element.classList.remove('focus-visible');
        });
    });
    
    // Auto-dismiss flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 300);
        }, 5000);
    });
    
    console.log('Automated Diagnostic System initialized successfully');
});

// Service worker registration (if available)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Error handling
window.addEventListener('error', (e) => {
    console.error('Application error:', e.error);
    
    // Show user-friendly error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'fixed bottom-4 right-4 bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg shadow-lg z-50 max-w-sm';
    errorDiv.innerHTML = `
        <div class="flex items-start">
            <i data-feather="alert-triangle" class="w-5 h-5 mr-2 mt-0.5 flex-shrink-0"></i>
            <div>
                <div class="font-medium">Something went wrong</div>
                <div class="text-sm">Please refresh the page and try again.</div>
            </div>
        </div>
    `;
    
    document.body.appendChild(errorDiv);
    
    // Re-render feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Auto-hide after 10 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 10000);
});

// Unhandled promise rejection handling
window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    e.preventDefault();
});
