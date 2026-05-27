// --- LÓGICA DE CLIENTE DEL DASHBOARD (JS VANILLA) ---

document.addEventListener('DOMContentLoaded', () => {
    // 1. SELECTOR DE TEMA CLARO/OSCURO
    const themeToggleBtn = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Obtener tema preferido guardado
    const savedTheme = localStorage.getItem('dashboard-theme') || 'light';
    body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('dashboard-theme', newTheme);
            updateThemeIcon(newTheme);
            
            // Actualizar colores de los gráficos si existen
            updateChartsTheme(newTheme);
        });
    }

    function updateThemeIcon(theme) {
        const iconSpan = themeToggleBtn ? themeToggleBtn.querySelector('span') : null;
        if (iconSpan) {
            iconSpan.textContent = theme === 'dark' ? 'light_mode' : 'dark_mode';
        }
    }

    // 2. NAVEGACIÓN POR PESTAÑAS (TABS)
    const navItems = document.querySelectorAll('.nav-item[data-tab]');
    const sections = document.querySelectorAll('.dashboard-section');

    // Comprobar si hay una pestaña en la URL (ej. ?tab=news)
    const urlParams = new URLSearchParams(window.location.search);
    const initialTab = urlParams.get('tab') || 'overview';
    switchTab(initialTab);

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabId = item.getAttribute('data-tab');
            switchTab(tabId);
            
            // Actualizar URL sin recargar
            const newUrl = window.location.pathname + '?tab=' + tabId;
            window.history.pushState({ path: newUrl }, '', newUrl);
        });
    });

    function switchTab(tabId) {
        // Desactivar todos los items y secciones
        navItems.forEach(nav => nav.classList.remove('active'));
        sections.forEach(sec => sec.classList.remove('active'));

        // Activar el correspondiente
        const targetNav = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
        const targetSection = document.getElementById(`section-${tabId}`);

        if (targetNav && targetSection) {
            targetNav.classList.add('active');
            targetSection.classList.add('active');
        } else {
            // Fallback al overview
            const overviewNav = document.querySelector('.nav-item[data-tab="overview"]');
            const overviewSection = document.getElementById('section-overview');
            if (overviewNav && overviewSection) {
                overviewNav.classList.add('active');
                overviewSection.classList.add('active');
            }
        }
    }

    // 3. TOAST NOTIFICATIONS SYSTEM
    window.showToast = function(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let icon = 'info';
        if (type === 'success') icon = 'check_circle';
        if (type === 'danger') icon = 'error';
        if (type === 'warning') icon = 'warning';

        toast.innerHTML = `
            <span class="material-icons" style="font-size: 1.25rem;">${icon}</span>
            <div class="toast-message">${message}</div>
        `;

        container.appendChild(toast);

        // Auto-eliminar después de 4 segundos
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s forwards';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 4000);
    };

    // Mostrar mensajes que vengan de Django en el toast
    const djangoMessages = document.querySelectorAll('.django-message');
    djangoMessages.forEach(msg => {
        const text = msg.textContent.trim();
        const tags = msg.getAttribute('data-tags');
        let type = 'info';
        if (tags.includes('success')) type = 'success';
        if (tags.includes('error') || tags.includes('danger')) type = 'danger';
        if (tags.includes('warning')) type = 'warning';
        showToast(text, type);
    });

    // 4. MODERACIÓN DE COMENTARIOS CON FETCH API
    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    const csrftoken = getCookie('csrftoken');

    const pendingCommentsList = document.getElementById('pending-comments-list');
    if (pendingCommentsList) {
        pendingCommentsList.addEventListener('click', async (e) => {
            const target = e.target.closest('.btn-comment-action');
            if (!target) return;

            const commentId = target.getAttribute('data-id');
            const action = target.getAttribute('data-action'); // 'approve' o 'delete'
            const row = document.getElementById(`comment-row-${commentId}`);

            if (!commentId || !row) return;

            if (action === 'delete') {
                if (!confirm('¿Estás seguro de que deseas rechazar y eliminar este comentario?')) {
                    return;
                }
            }

            const url = `/dashboard/api/comment/${commentId}/${action}/`;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    }
                });

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    // Animación de salida y remoción
                    row.style.transform = 'translateX(-30px)';
                    row.style.opacity = '0';
                    row.style.transition = 'all 0.3s ease';
                    setTimeout(() => {
                        row.remove();
                        // Actualizar contadores en la UI
                        updatePendingCount();
                        
                        // Si ya no quedan comentarios pendientes
                        if (pendingCommentsList.querySelectorAll('tr').length === 0) {
                            pendingCommentsList.innerHTML = `
                                <tr>
                                    <td colspan="5" style="text-align: center; color: var(--text-muted); padding: 2rem;">
                                        No hay comentarios pendientes de aprobación.
                                    </td>
                                </tr>
                            `;
                        }
                    }, 300);

                    showToast(data.message, action === 'approve' ? 'success' : 'warning');
                } else {
                    showToast(data.error || 'Ocurrió un error al procesar la solicitud.', 'danger');
                }
            } catch (err) {
                console.error(err);
                showToast('Error de conexión al servidor.', 'danger');
            }
        });
    }

    function updatePendingCount() {
        const counters = document.querySelectorAll('.stat-pending-val, .badge-pending-count');
        counters.forEach(c => {
            let current = parseInt(c.textContent) || 0;
            if (current > 0) {
                c.textContent = current - 1;
            }
        });
    }

    // 5. GESTIÓN DE CATEGORÍAS MODAL & AJAX
    const openModalBtn = document.getElementById('btn-new-category');
    const closeModalBtn = document.getElementById('close-category-modal');
    const cancelModalBtn = document.getElementById('btn-cancel-category');
    const modalOverlay = document.getElementById('category-modal');
    const categoryForm = document.getElementById('category-form-element');
    const categoriesTableBody = document.getElementById('categories-table-body');
    const selectCategoryDropdown = document.querySelector('select[name="category"]'); // Para formularios de noticias si hay

    if (openModalBtn && modalOverlay) {
        openModalBtn.addEventListener('click', () => modalOverlay.classList.add('active'));
    }

    const closeModal = () => {
        if (modalOverlay) {
            modalOverlay.classList.remove('active');
            if (categoryForm) categoryForm.reset();
        }
    };

    if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
    if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeModal);
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) closeModal();
        });
    }

    if (categoryForm) {
        categoryForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(categoryForm);

            try {
                const response = await fetch('/dashboard/api/category/create/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    body: formData
                });

                const data = await response.json();

                if (response.ok && data.status === 'ok') {
                    // Agregar categoría a la tabla
                    if (categoriesTableBody) {
                        const newRow = document.createElement('tr');
                        newRow.id = `category-row-${data.category.id}`;
                        newRow.innerHTML = `
                            <td><strong>${escapeHTML(data.category.name)}</strong></td>
                            <td style="color: var(--text-secondary);">${escapeHTML(data.category.description || 'Sin descripción')}</td>
                            <td><span class="badge-pill badge-info">0 artículos</span></td>
                            <td>${escapeHTML(data.category.slug)}</td>
                        `;
                        categoriesTableBody.appendChild(newRow);
                    }

                    // Actualizar el contador de categorías en stats
                    const catCounter = document.querySelector('.stat-categories-val');
                    if (catCounter) {
                        let current = parseInt(catCounter.textContent) || 0;
                        catCounter.textContent = current + 1;
                    }

                    // Cerrar el modal e informar
                    closeModal();
                    showToast(data.message, 'success');
                } else {
                    let errMsg = 'Revisa los campos e intenta de nuevo.';
                    if (data.errors && data.errors.name) {
                        errMsg = `Nombre: ${data.errors.name.join(' ')}`;
                    }
                    showToast(errMsg, 'danger');
                }
            } catch (err) {
                console.error(err);
                showToast('Error de conexión al servidor.', 'danger');
            }
        });
    }

    function escapeHTML(str) {
        if (!str) return '';
        return str.replace(/[&<>'"]/g, 
            tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
        );
    }

    // 6. FILTRO DE BÚSQUEDA DE NOTICIAS EN TIEMPO REAL
    const searchNewsInput = document.getElementById('search-news');
    const filterCategorySelect = document.getElementById('filter-category');
    const newsRows = document.querySelectorAll('.news-table-row');

    if (searchNewsInput || filterCategorySelect) {
        const filterNews = () => {
            const query = searchNewsInput ? searchNewsInput.value.toLowerCase().trim() : '';
            const cat = filterCategorySelect ? filterCategorySelect.value : '';

            newsRows.forEach(row => {
                const title = row.getAttribute('data-title').toLowerCase();
                const categoryId = row.getAttribute('data-category');
                
                const matchesSearch = title.includes(query);
                const matchesCategory = cat === '' || categoryId === cat;

                if (matchesSearch && matchesCategory) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        };

        if (searchNewsInput) searchNewsInput.addEventListener('input', filterNews);
        if (filterCategorySelect) filterCategorySelect.addEventListener('change', filterNews);
    }

    // 7. INICIALIZACIÓN DE GRÁFICOS CHART.JS
    let categoryChart = null;
    let commentActivityChart = null;

    window.initDashboardCharts = function(catData, commData) {
        const isDark = body.getAttribute('data-theme') === 'dark';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';
        const textColor = isDark ? '#94a3b8' : '#64748b';

        // Gráfico de Categorías (Bar/Doughnut)
        const ctxCat = document.getElementById('chart-categories');
        if (ctxCat) {
            categoryChart = new Chart(ctxCat, {
                type: 'doughnut',
                data: {
                    labels: catData.labels,
                    datasets: [{
                        label: 'Artículos por Categoría',
                        data: catData.values,
                        backgroundColor: [
                            'rgba(59, 130, 246, 0.75)',  // primary
                            'rgba(139, 92, 246, 0.75)',  // secondary
                            'rgba(16, 185, 129, 0.75)',  // success
                            'rgba(245, 158, 11, 0.75)',  // warning
                            'rgba(239, 68, 68, 0.75)',   // danger
                            'rgba(14, 165, 233, 0.75)',
                            'rgba(236, 72, 153, 0.75)'
                        ],
                        borderWidth: isDark ? 2 : 1,
                        borderColor: isDark ? '#111827' : '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: textColor,
                                font: { family: 'Outfit', size: 11 }
                            }
                        }
                    }
                }
            });
        }

        // Gráfico de Actividad de Comentarios (Line)
        const ctxComm = document.getElementById('chart-comments');
        if (ctxComm) {
            commentActivityChart = new Chart(ctxComm, {
                type: 'line',
                data: {
                    labels: commData.labels,
                    datasets: [{
                        label: 'Comentarios recibidos',
                        data: commData.values,
                        fill: true,
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        borderColor: 'rgba(139, 92, 246, 0.8)',
                        borderWidth: 2,
                        tension: 0.3,
                        pointBackgroundColor: 'rgba(139, 92, 246, 1)',
                        pointBorderColor: isDark ? '#111827' : '#ffffff',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            grid: { color: gridColor },
                            ticks: { color: textColor, font: { family: 'Outfit', size: 11 } }
                        },
                        y: {
                            grid: { color: gridColor },
                            ticks: { color: textColor, font: { family: 'Outfit', size: 11 } }
                        }
                    }
                }
            });
        }
    };

    function updateChartsTheme(theme) {
        const isDark = theme === 'dark';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';
        const textColor = isDark ? '#94a3b8' : '#64748b';

        if (categoryChart) {
            categoryChart.options.plugins.legend.labels.color = textColor;
            categoryChart.data.datasets[0].borderColor = isDark ? '#111827' : '#ffffff';
            categoryChart.data.datasets[0].borderWidth = isDark ? 2 : 1;
            categoryChart.update();
        }

        if (commentActivityChart) {
            commentActivityChart.options.scales.x.grid.color = gridColor;
            commentActivityChart.options.scales.x.ticks.color = textColor;
            commentActivityChart.options.scales.y.grid.color = gridColor;
            commentActivityChart.options.scales.y.ticks.color = textColor;
            commentActivityChart.data.datasets[0].pointBorderColor = isDark ? '#111827' : '#ffffff';
            commentActivityChart.update();
        }
    }
});
