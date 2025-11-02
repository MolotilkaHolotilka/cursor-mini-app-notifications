// Telegram WebApp API initialization
let tg = window.Telegram?.WebApp;

if (tg) {
    tg.ready();
    tg.expand();
    
    // Set theme colors
    if (tg.themeParams) {
        document.documentElement.style.setProperty('--primary-color', tg.themeParams.button_color || '#2481cc');
    }
}

// API Configuration
// Автоматическое определение API URL
const API_BASE_URL = window.API_BASE_URL || (() => {
    // Локальная разработка
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'http://localhost:8000/api';
    }
    
    // Если фронтенд на GitHub Pages - используем отдельный API домен
    // Если фронтенд и API на одном домене (Coolify) - используем относительный путь
    const hostname = window.location.hostname;
    
    // GitHub Pages (статический хостинг) - нужен отдельный API сервер
    if (hostname.includes('github.io')) {
        // TODO: Замените на реальный URL вашего API сервера на Coolify
        return 'https://your-coolify-api-domain.com/api';
    }
    
    // Если фронтенд и API на одном домене (Coolify) - используем относительный путь
    // Это работает когда фронтенд обслуживается через FastAPI
    return '/api';
})();

// State
let notifications = [];
let filters = {
    type: 'all',
    manager: 'all'
};

// DOM Elements
const filterBtn = document.getElementById('filterBtn');
const refreshBtn = document.getElementById('refreshBtn');
const filterPanel = document.getElementById('filterPanel');
const notificationsContainer = document.getElementById('notificationsContainer');
const emptyState = document.getElementById('emptyState');
const loadingState = document.getElementById('loadingState');
const notificationTemplate = document.getElementById('notificationTemplate');
const managerFilter = document.getElementById('managerFilter');
const clearFiltersBtn = document.getElementById('clearFilters');
const applyFiltersBtn = document.getElementById('applyFilters');

// Stats elements
const totalCountEl = document.getElementById('totalCount');
const unreadCountEl = document.getElementById('unreadCount');
const todayCountEl = document.getElementById('todayCount');

// Event Listeners
filterBtn?.addEventListener('click', toggleFilterPanel);
refreshBtn?.addEventListener('click', loadNotifications);
clearFiltersBtn?.addEventListener('click', clearFilters);
applyFiltersBtn?.addEventListener('click', applyFilters);

// Filter chips
document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', function() {
        document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        filters.type = this.dataset.filter;
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadNotifications();
    await loadManagers(); // Загружаем менеджеров из API
});

// Toggle filter panel
function toggleFilterPanel() {
    filterPanel.classList.toggle('active');
}

// Load notifications - загрузка с API
async function loadNotifications() {
    showLoading();
    
    try {
        // Формируем query параметры
        const params = new URLSearchParams();
        if (filters.type !== 'all') {
            params.append('type', filters.type);
        }
        if (filters.manager !== 'all') {
            params.append('user_id', filters.manager);
        }
        params.append('limit', '100');
        params.append('offset', '0');
        
        const url = `${API_BASE_URL}/notifications?${params.toString()}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Преобразуем данные API в формат для фронтенда
        notifications = data.notifications.map(n => ({
            id: n.id,
            type: n.type,
            title: n.title,
            description: n.description,
            user: n.user_name,
            userId: n.user_id,
            timestamp: new Date(n.timestamp).getTime(),
            read: n.status === 'read',
            details: n.details ? Object.values(n.details) : []
        }));
        
        renderNotifications();
        await loadStats();
        hideLoading();
    } catch (error) {
        console.error('Ошибка загрузки уведомлений:', error);
        showError('Не удалось загрузить уведомления. Проверьте подключение к API.');
        // Fallback на моки в случае ошибки
        notifications = getMockNotifications();
        renderNotifications();
        updateStats();
        hideLoading();
    }
}

// Render notifications
function renderNotifications() {
    notificationsContainer.innerHTML = '';
    
    const filteredNotifications = applyFiltersToNotifications();
    
    if (filteredNotifications.length === 0) {
        emptyState.classList.add('active');
        return;
    }
    
    emptyState.classList.remove('active');
    
    // Group by time
    const grouped = groupNotificationsByTime(filteredNotifications);
    
    Object.keys(grouped).forEach(timeGroup => {
        if (timeGroup !== 'other') {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'time-group';
            groupDiv.innerHTML = `<div class="time-group-title">${timeGroup}</div>`;
            notificationsContainer.appendChild(groupDiv);
        }
        
        grouped[timeGroup].forEach(notification => {
            const notificationEl = createNotificationElement(notification);
            notificationsContainer.appendChild(notificationEl);
        });
    });
}

// Create notification element
function createNotificationElement(notification) {
    const el = notificationTemplate.cloneNode(true);
    el.id = '';
    el.style.display = '';
    el.classList.remove('template');
    
    if (notification.read === false) {
        el.classList.add('unread');
        el.querySelector('.notification-badge').style.display = 'block';
    }
    
    // Set icon based on type
    const iconEl = el.querySelector('.notification-icon');
    iconEl.className = `notification-icon ${notification.type}`;
    iconEl.querySelector('.icon').textContent = getIconForType(notification.type);
    
    // Set content
    el.querySelector('.notification-title').textContent = notification.title;
    el.querySelector('.notification-user').textContent = notification.user;
    el.querySelector('.notification-time').textContent = formatTime(notification.timestamp);
    el.querySelector('.notification-description').textContent = notification.description;
    
    // Add details
    const detailsEl = el.querySelector('.notification-details');
    if (notification.details) {
        notification.details.forEach(detail => {
            const tag = document.createElement('span');
            tag.className = 'notification-tag';
            tag.textContent = detail;
            detailsEl.appendChild(tag);
        });
    }
    
    // Click handler
    el.addEventListener('click', async () => {
        await markAsRead(notification.id);
        el.classList.remove('unread');
        el.querySelector('.notification-badge').style.display = 'none';
    });
    
    return el;
}

// Apply filters
function applyFiltersToNotifications() {
    return notifications.filter(notification => {
        if (filters.type !== 'all' && notification.type !== filters.type) {
            return false;
        }
        if (filters.manager !== 'all' && notification.userId !== filters.manager) {
            return false;
        }
        return true;
    });
}

// Group notifications by time
function groupNotificationsByTime(notifications) {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const thisWeek = new Date(today);
    thisWeek.setDate(thisWeek.getDate() - 7);
    
    const groups = {
        'Сегодня': [],
        'Вчера': [],
        'На этой неделе': [],
        'Ранее': []
    };
    
    notifications.forEach(notification => {
        const date = new Date(notification.timestamp);
        
        if (date >= today) {
            groups['Сегодня'].push(notification);
        } else if (date >= yesterday) {
            groups['Вчера'].push(notification);
        } else if (date >= thisWeek) {
            groups['На этой неделе'].push(notification);
        } else {
            groups['Ранее'].push(notification);
        }
    });
    
    // Remove empty groups
    Object.keys(groups).forEach(key => {
        if (groups[key].length === 0) {
            delete groups[key];
        }
    });
    
    return groups;
}

// Load stats from API
async function loadStats() {
    try {
        const params = new URLSearchParams();
        if (filters.manager !== 'all') {
            params.append('user_id', filters.manager);
        }
        
        const url = `${API_BASE_URL}/stats${params.toString() ? '?' + params.toString() : ''}`;
        const response = await fetch(url);
        
        if (response.ok) {
            const stats = await response.json();
            totalCountEl.textContent = stats.total;
            unreadCountEl.textContent = stats.unread;
            todayCountEl.textContent = stats.today;
            
            // Обновляем список менеджеров из статистики
            if (stats.by_user && Object.keys(stats.by_user).length > 0) {
                updateManagerFilter(Object.keys(stats.by_user));
            }
        } else {
            updateStats(); // Fallback на локальный расчет
        }
    } catch (error) {
        console.error('Ошибка загрузки статистики:', error);
        updateStats(); // Fallback на локальный расчет
    }
}

// Update stats - локальный расчет (fallback)
function updateStats() {
    const filtered = applyFiltersToNotifications();
    const unread = filtered.filter(n => !n.read).length;
    const today = filtered.filter(n => {
        const date = new Date(n.timestamp);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return date >= today;
    }).length;
    
    totalCountEl.textContent = filtered.length;
    unreadCountEl.textContent = unread;
    todayCountEl.textContent = today;
}

// Clear filters
function clearFilters() {
    filters = { type: 'all', manager: 'all' };
    document.querySelectorAll('.chip').forEach(c => {
        c.classList.toggle('active', c.dataset.filter === 'all');
    });
    managerFilter.value = 'all';
    renderNotifications();
    updateStats();
}

// Apply filters
function applyFilters() {
    filters.manager = managerFilter.value;
    renderNotifications();
    updateStats();
    toggleFilterPanel();
}

// Mark notification as read - обновление через API
async function markAsRead(id) {
    const notification = notifications.find(n => n.id === id);
    if (!notification) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/notifications/${id}/read`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            notification.read = true;
            await loadStats();
        } else {
            // Если API не работает, обновляем локально
            notification.read = true;
            updateStats();
        }
    } catch (error) {
        console.error('Ошибка обновления статуса:', error);
        // Fallback на локальное обновление
        notification.read = true;
        updateStats();
    }
}

// Helper functions
function getIconForType(type) {
    const icons = {
        'file_upload': '📤',
        'record_create': '➕',
        'record_update': '✏️',
        'user_action': '👤'
    };
    return icons[type] || '🔔';
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return 'только что';
    if (minutes < 60) return `${minutes} мин назад`;
    if (hours < 24) return `${hours} ч назад`;
    if (days < 7) return `${days} дн назад`;
    
    return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
}

function showLoading() {
    loadingState.classList.add('active');
    emptyState.classList.remove('active');
}

function hideLoading() {
    loadingState.classList.remove('active');
}

function showError(message) {
    console.error(message);
    // Показываем уведомление пользователю (можно улучшить UI)
    if (tg?.showAlert) {
        tg.showAlert(message);
    } else {
        alert(message);
    }
}

// Mock data (remove in production)
function getMockNotifications() {
    const now = Date.now();
    const managers = ['Менеджер А', 'Менеджер Б', 'Менеджер В'];
    
    return [
        {
            id: 1,
            type: 'file_upload',
            title: 'Загрузка файла',
            description: 'Загружен файл "Отчет_2024.xlsx" в таблицу "Документы"',
            user: managers[0],
            userId: 'manager_a',
            timestamp: now - 300000, // 5 min ago
            read: false,
            details: ['Airtable', 'Документы', 'Excel']
        },
        {
            id: 2,
            type: 'record_create',
            title: 'Создание записи',
            description: 'Создана новая запись в таблице "Проекты": "Проект Альфа"',
            user: managers[1],
            userId: 'manager_b',
            timestamp: now - 1800000, // 30 min ago
            read: false,
            details: ['Airtable', 'Проекты']
        },
        {
            id: 3,
            type: 'record_update',
            title: 'Обновление записи',
            description: 'Обновлена запись "Клиент XYZ" в таблице "Клиенты"',
            user: managers[0],
            userId: 'manager_a',
            timestamp: now - 3600000, // 1 hour ago
            read: true,
            details: ['Airtable', 'Клиенты']
        },
        {
            id: 4,
            type: 'file_upload',
            title: 'Загрузка файла',
            description: 'Загружен файл "Презентация.pdf" в таблицу "Материалы"',
            user: managers[2],
            userId: 'manager_c',
            timestamp: now - 7200000, // 2 hours ago
            read: false,
            details: ['Airtable', 'Материалы', 'PDF']
        },
        {
            id: 5,
            type: 'user_action',
            title: 'Действие пользователя',
            description: 'Выполнен экспорт данных из таблицы "Заказы"',
            user: managers[1],
            userId: 'manager_b',
            timestamp: now - 86400000, // 1 day ago
            read: true,
            details: ['Airtable', 'Заказы', 'Экспорт']
        }
    ];
}

// Load managers from API stats
async function loadManagers() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        if (response.ok) {
            const stats = await response.json();
            if (stats.by_user && Object.keys(stats.by_user).length > 0) {
                updateManagerFilter(Object.keys(stats.by_user));
                return;
            }
        }
    } catch (error) {
        console.error('Ошибка загрузки менеджеров:', error);
    }
    
    // Fallback на моки если API недоступен
    setupMockManagers();
}

function updateManagerFilter(managerNames) {
    // Очищаем существующие опции (кроме "Все менеджеры")
    while (managerFilter.children.length > 1) {
        managerFilter.removeChild(managerFilter.lastChild);
    }
    
    // Добавляем менеджеров из статистики
    // Нужно получить user_id для каждого менеджера из уведомлений
    const managerMap = new Map();
    notifications.forEach(n => {
        if (!managerMap.has(n.userId)) {
            managerMap.set(n.userId, n.user);
        }
    });
    
    managerMap.forEach((name, userId) => {
        const option = document.createElement('option');
        option.value = userId;
        option.textContent = name;
        managerFilter.appendChild(option);
    });
}

function setupMockManagers() {
    // Populate manager filter (fallback)
    const managers = [
        { id: 'manager_a', name: 'Менеджер А' },
        { id: 'manager_b', name: 'Менеджер Б' },
        { id: 'manager_c', name: 'Менеджер В' }
    ];
    
    managers.forEach(manager => {
        const option = document.createElement('option');
        option.value = manager.id;
        option.textContent = manager.name;
        managerFilter.appendChild(option);
    });
}
