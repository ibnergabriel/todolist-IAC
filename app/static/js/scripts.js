// Função para carregar tarefas com base nos filtros
const loadTodos = async () => {
    try {
        // Obter os valores atuais dos filtros
        const filtroStatus = document.getElementById('filtro-status').value;
        const filtroPrioridade = document.getElementById('filtro-prioridade').value;

        // Construir a URL com os filtros
        const url = `/tarefas?filtro_status=${filtroStatus}&filtro_prioridade=${filtroPrioridade}`;

        // Fazer a requisição ao servidor
        const response = await fetch(url);
        if (!response.ok) throw new Error('Erro ao carregar tarefas');

        // Atualizar a lista de tarefas
        const data = await response.text();
        const todoList = new DOMParser()
            .parseFromString(data, 'text/html')
            .getElementById('todo-list').innerHTML;
        document.getElementById('todo-list').innerHTML = todoList;

        // Reanexar listeners após carregar as tarefas
        attachEventListeners();
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
        alert('Erro ao carregar tarefas. Tente novamente.');
    }
};

// Função para adicionar uma nova tarefa
const addTodo = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        const response = await fetch('/tarefa', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) throw new Error('Erro ao adicionar tarefa');
        window.location.reload(); // Recarregar a página após adicionar a tarefa
    } catch (error) {
        console.error('Erro ao adicionar tarefa:', error);
        alert('Erro ao adicionar tarefa. Tente novamente.');
    }
};

// Função para atualizar o status de uma tarefa
const updateTodoStatus = async (e) => {
    e.preventDefault();
    try {
        const response = await fetch(e.target.action, {
            method: 'POST',
            body: new FormData(e.target)
        });
        if (!response.ok) throw new Error('Erro ao atualizar status');
        window.location.reload(); // Recarregar a página após atualizar o status
    } catch (error) {
        console.error('Erro ao atualizar status:', error);
        alert('Erro ao atualizar status. Tente novamente.');
    }
};

// Função para excluir uma tarefa
const deleteTodo = async (e) => {
    e.preventDefault();
    try {
        const response = await fetch(e.target.action, {
            method: 'POST'
        });
        if (!response.ok) throw new Error('Erro ao excluir tarefa');
        window.location.reload(); // Recarregar a página após excluir a tarefa
    } catch (error) {
        console.error('Erro ao excluir tarefa:', error);
        alert('Erro ao excluir tarefa. Tente novamente.');
    }
};

// Função para exibir o formulário de edição com animação
const showEditForm = (id) => {
    const form = document.getElementById(`editar-form-${id}`);
    form.style.display = 'block';
    form.style.opacity = '0';
    form.style.transition = 'opacity 0.3s ease';

    setTimeout(() => {
        form.style.opacity = '1';
    }, 10);
};

// Função para salvar a edição da tarefa
const saveEdit = async (event, id) => {
    event.preventDefault();
    const form = event.target;
    const titulo = form.querySelector('input[name="titulo"]').value;

    if (!titulo.trim()) {
        alert('O título da tarefa é obrigatório.');
        return;
    }

    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.textContent = 'Salvando...';

    try {
        const formData = new FormData(form);
        const response = await fetch(`/tarefa/${id}/editar`, {
            method: 'POST',
            body: formData
        });
        if (!response.ok) throw new Error('Erro ao salvar edição');
        window.location.reload();
    } catch (error) {
        console.error('Erro ao salvar edição:', error);
        alert('Erro ao salvar edição. Tente novamente.');
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Salvar';
    }
};

// Função para ocultar o formulário de edição com animação
const hideEditForm = (id) => {
    const form = document.getElementById(`editar-form-${id}`);
    form.style.opacity = '0';
    form.style.transition = 'opacity 0.3s ease';

    setTimeout(() => {
        form.style.display = 'none';
    }, 300);
};

// Função para aplicar filtros sem recarregar a página
const aplicarFiltros = () => {
    // Obter os valores dos filtros
    const filtroStatus = document.getElementById('filtro-status').value;
    const filtroPrioridade = document.getElementById('filtro-prioridade').value;

    // Atualizar a URL sem recarregar a página
    const url = `/tarefas?filtro_status=${filtroStatus}&filtro_prioridade=${filtroPrioridade}`;
    window.history.pushState({}, '', url);

    // Carregar as tarefas com os novos filtros
    loadTodos();
};

// Função para anexar listeners aos elementos
const attachEventListeners = () => {
    // Adicionar nova tarefa
    document.getElementById('todo-form').addEventListener('submit', addTodo);

    // Atualizar status de tarefa
    document.querySelectorAll('.finish-todo').forEach(form => {
        form.addEventListener('submit', updateTodoStatus);
    });

    // Excluir tarefa
    document.querySelectorAll('.remove-todo').forEach(form => {
        form.addEventListener('submit', deleteTodo);
    });

    // Botões de edição
    document.querySelectorAll('[onclick^="editarTarefa"]').forEach(button => {
        const id = button.getAttribute('onclick').match(/\d+/)[0];
        button.addEventListener('click', () => showEditForm(id));
    });

    // Botões de cancelar edição
    document.querySelectorAll('[onclick^="cancelarEdicao"]').forEach(button => {
        const id = button.getAttribute('onclick').match(/\d+/)[0];
        button.addEventListener('click', () => hideEditForm(id));
    });

    // Formulários de edição
    document.querySelectorAll('[onsubmit^="salvarEdicao"]').forEach(form => {
        const id = form.getAttribute('onsubmit').match(/\d+/)[0];
        form.addEventListener('submit', (e) => saveEdit(e, id));
    });

    // Filtros
    document.getElementById('filtro-status').addEventListener('change', aplicarFiltros);
    document.getElementById('filtro-prioridade').addEventListener('change', aplicarFiltros);
};

// Carregar tarefas ao iniciar e anexar listeners
document.addEventListener('DOMContentLoaded', () => {
    // Restaurar os valores dos filtros da URL
    const urlParams = new URLSearchParams(window.location.search);
    document.getElementById('filtro-status').value = urlParams.get('filtro_status') || 'Todas';
    document.getElementById('filtro-prioridade').value = urlParams.get('filtro_prioridade') || 'Todas';

    // Carregar as tarefas com os filtros atuais
    loadTodos();
});