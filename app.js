/**
 * ProjectFlow - Logic & State Management
 */

// State
let projects = JSON.parse(localStorage.getItem('projectflow_data')) || [];
let activeProjectId = null;
let draggedTask = null;

// DOM Elements
const projectListEl = document.getElementById('project-list');
const addProjectBtn = document.getElementById('add-project-btn');
const addTaskBtn = document.getElementById('add-task-btn');
const deleteProjectBtn = document.getElementById('delete-project-btn');
const currentProjectTitle = document.getElementById('current-project-title');
const currentProjectDesc = document.getElementById('current-project-desc');
const progressBarFill = document.getElementById('progress-bar-fill');
const progressPercentageText = document.getElementById('progress-percentage');

// Modals
const projectModal = document.getElementById('project-modal');
const taskModal = document.getElementById('task-modal');
const closeBtns = document.querySelectorAll('.close-modal, .cancel-modal');

// Inputs
const projectNameInput = document.getElementById('project-name');
const taskTitleInput = document.getElementById('task-title');
const taskDescInput = document.getElementById('task-desc');
const saveProjectBtn = document.getElementById('save-project-btn');
const saveTaskBtn = document.getElementById('save-task-btn');

// Board
const dropzones = document.querySelectorAll('.dropzone');
const kanbanColumns = {
    'todo': document.querySelector('#col-todo .task-list'),
    'inprogress': document.querySelector('#col-inprogress .task-list'),
    'done': document.querySelector('#col-done .task-list')
};

/* ==========================================================================
   Initialization
   ========================================================================== */
function init() {
    setupEventListeners();
    renderProjects();
    
    if (projects.length > 0) {
        selectProject(projects[0].id);
    } else {
        renderEmptyState();
    }
}

function saveData() {
    localStorage.setItem('projectflow_data', JSON.stringify(projects));
}

function generateId() {
    return Math.random().toString(36).substr(2, 9);
}

/* ==========================================================================
   Event Listeners Setup
   ========================================================================== */
function setupEventListeners() {
    // Modals
    addProjectBtn.addEventListener('click', () => openModal(projectModal));
    addTaskBtn.addEventListener('click', () => openModal(taskModal));
    
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            closeModal(projectModal);
            closeModal(taskModal);
        });
    });

    // Submits
    saveProjectBtn.addEventListener('click', handleAddProject);
    projectNameInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleAddProject();
    });

    saveTaskBtn.addEventListener('click', handleAddTask);
    taskTitleInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleAddTask();
    });

    deleteProjectBtn.addEventListener('click', handleDeleteProject);

    // Drag and Drop
    setupDragAndDrop();
}

/* ==========================================================================
   Projects Management
   ========================================================================== */
function renderProjects() {
    projectListEl.innerHTML = '';
    
    projects.forEach(project => {
        const li = document.createElement('li');
        li.className = `project-item ${project.id === activeProjectId ? 'active' : ''}`;
        li.innerHTML = `
            <div class="dot"></div>
            <span>${project.name}</span>
        `;
        li.addEventListener('click', () => selectProject(project.id));
        projectListEl.appendChild(li);
    });
}

function handleAddProject() {
    const name = projectNameInput.value.trim();
    if (!name) return;

    const newProject = {
        id: generateId(),
        name: name,
        tasks: []
    };

    projects.push(newProject);
    saveData();
    renderProjects();
    closeModal(projectModal);
    projectNameInput.value = '';
    
    selectProject(newProject.id);
}

function handleDeleteProject() {
    if (!activeProjectId) return;
    
    if (confirm('Are you sure you want to delete this project? All tasks will be lost.')) {
        projects = projects.filter(p => p.id !== activeProjectId);
        saveData();
        activeProjectId = null;
        renderProjects();
        if (projects.length > 0) {
            selectProject(projects[0].id);
        } else {
            renderEmptyState();
        }
    }
}

function selectProject(id) {
    activeProjectId = id;
    renderProjects();
    
    const project = projects.find(p => p.id === id);
    if (!project) return;

    currentProjectTitle.textContent = project.name;
    currentProjectDesc.textContent = `${project.tasks.length} Total Tasks`;
    
    addTaskBtn.disabled = false;
    deleteProjectBtn.disabled = false;

    renderTasks();
}

function renderEmptyState() {
    currentProjectTitle.textContent = "No Project Selected";
    currentProjectDesc.textContent = "Create a project to get started";
    addTaskBtn.disabled = true;
    deleteProjectBtn.disabled = true;
    
    Object.values(kanbanColumns).forEach(col => {
        col.innerHTML = `
            <div class="empty-state">
                <i class="fa-solid fa-clipboard-list"></i>
                <p>No tasks yet</p>
            </div>
        `;
    });
    
    updateProgress();
    updateCounts();
}

/* ==========================================================================
   Tasks Management
   ========================================================================== */
function renderTasks() {
    const project = projects.find(p => p.id === activeProjectId);
    if (!project) return;

    // Clear columns
    Object.values(kanbanColumns).forEach(col => col.innerHTML = '');

    let hasTasks = false;

    project.tasks.forEach(task => {
        hasTasks = true;
        const card = createTaskCard(task);
        if(kanbanColumns[task.status]) {
            kanbanColumns[task.status].appendChild(card);
        }
    });

    if (!hasTasks) {
        Object.values(kanbanColumns).forEach(col => {
            col.innerHTML = `
                <div class="empty-state">
                    <i class="fa-regular fa-folder-open"></i>
                    <p>Drop tasks here</p>
                </div>
            `;
        });
    }

    updateProgress();
    updateCounts();
}

function createTaskCard(task) {
    const div = document.createElement('div');
    div.className = 'task-card';
    div.draggable = true;
    div.dataset.id = task.id;

    div.innerHTML = `
        <div class="task-header">
            <span class="task-title">${task.title}</span>
            <button class="task-delete" onclick="deleteTask(event, '${task.id}')">
                <i class="fa-solid fa-trash-can"></i>
            </button>
        </div>
        ${task.desc ? `<p class="task-desc">${task.desc}</p>` : ''}
    `;

    // Drag Events
    div.addEventListener('dragstart', (e) => {
        draggedTask = div;
        setTimeout(() => div.classList.add('dragging'), 0);
    });

    div.addEventListener('dragend', () => {
        draggedTask.classList.remove('dragging');
        draggedTask = null;
    });

    return div;
}

function handleAddTask() {
    if (!activeProjectId) return;
    
    const title = taskTitleInput.value.trim();
    const desc = taskDescInput.value.trim();
    
    if (!title) return;

    const project = projects.find(p => p.id === activeProjectId);
    
    const newTask = {
        id: generateId(),
        title,
        desc,
        status: 'todo'
    };

    project.tasks.push(newTask);
    saveData();
    renderTasks();
    
    closeModal(taskModal);
    taskTitleInput.value = '';
    taskDescInput.value = '';
}

// Attach to window to allow inline onclick call
window.deleteTask = function(e, taskId) {
    e.stopPropagation(); // prevent drag
    if (!activeProjectId) return;
    
    const project = projects.find(p => p.id === activeProjectId);
    project.tasks = project.tasks.filter(t => t.id !== taskId);
    
    saveData();
    renderTasks();
};

/* ==========================================================================
   Drag and Drop
   ========================================================================== */
function setupDragAndDrop() {
    const columns = document.querySelectorAll('.kanban-column');

    columns.forEach(col => {
        col.addEventListener('dragover', e => {
            e.preventDefault();
            col.classList.add('drag-over');
            
            const dropzone = col.querySelector('.dropzone');
            const afterElement = getDragAfterElement(dropzone, e.clientY);
            
            if (draggedTask) {
                // Remove empty state if present
                const emptyState = dropzone.querySelector('.empty-state');
                if (emptyState) emptyState.remove();

                if (afterElement == null) {
                    dropzone.appendChild(draggedTask);
                } else {
                    dropzone.insertBefore(draggedTask, afterElement);
                }
            }
        });

        col.addEventListener('dragleave', () => {
            col.classList.remove('drag-over');
        });

        col.addEventListener('drop', e => {
            e.preventDefault();
            col.classList.remove('drag-over');
            
            if (!draggedTask || !activeProjectId) return;
            
            const taskId = draggedTask.dataset.id;
            const newStatus = col.dataset.status;
            
            // Update state
            const project = projects.find(p => p.id === activeProjectId);
            const task = project.tasks.find(t => t.id === taskId);
            
            if (task && task.status !== newStatus) {
                task.status = newStatus;
                saveData();
                updateProgress();
                updateCounts();
            }
            
            // Cleanup visually empty columns
            Object.values(kanbanColumns).forEach(lz => {
                if(lz.children.length === 0) {
                    lz.innerHTML = `
                        <div class="empty-state">
                            <i class="fa-regular fa-folder-open"></i>
                            <p>Drop tasks here</p>
                        </div>
                    `;
                }
            });
        });
    });
}

// Utility to find drop position
function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.task-card:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

/* ==========================================================================
   Helpers
   ========================================================================== */
function openModal(modal) {
    modal.classList.add('active');
    const input = modal.querySelector('input');
    if (input) setTimeout(() => input.focus(), 100);
}

function closeModal(modal) {
    modal.classList.remove('active');
}

function updateProgress() {
    if (!activeProjectId) {
        progressBarFill.style.width = '0%';
        progressPercentageText.textContent = '0%';
        return;
    }

    const project = projects.find(p => p.id === activeProjectId);
    const total = project.tasks.length;
    
    if (total === 0) {
        progressBarFill.style.width = '0%';
        progressPercentageText.textContent = '0%';
        return;
    }

    const done = project.tasks.filter(t => t.status === 'done').length;
    // We can value inprogress as half done, or just count 'done'
    const percentage = Math.round((done / total) * 100);
    
    progressBarFill.style.width = `${percentage}%`;
    progressPercentageText.textContent = `${percentage}%`;
}

function updateCounts() {
    if (!activeProjectId) return;
    const project = projects.find(p => p.id === activeProjectId);
    
    document.querySelector('#col-todo .task-count').textContent = project.tasks.filter(t => t.status === 'todo').length;
    document.querySelector('#col-inprogress .task-count').textContent = project.tasks.filter(t => t.status === 'inprogress').length;
    document.querySelector('#col-done .task-count').textContent = project.tasks.filter(t => t.status === 'done').length;
    
    currentProjectDesc.textContent = `${project.tasks.length} Total Tasks`;
}

// Start app
init();
