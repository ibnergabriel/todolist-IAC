// Função para carregar tarefas
const loadTodos = async () => {
    const response = await fetch('/');
    const data = await response.text();
    document.getElementById('todo-list').innerHTML = new DOMParser()
        .parseFromString(data, 'text/html')
        .getElementById('todo-list').innerHTML;
};

// Adicionar nova tarefa
document.getElementById('todo-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch('/tarefa', {
        method: 'POST',
        body: formData
    });
    if (response.ok) {
        window.location.reload(); // Recarregar a página após adicionar a tarefa
    }
});

// Atualizar status de tarefa
document.querySelectorAll('.finish-todo').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const response = await fetch(e.target.action, {
            method: 'POST',
            body: new FormData(e.target)
        });
        if (response.ok) {
            window.location.reload(); // Recarregar a página após atualizar o status
        }
    });
});

// Excluir tarefa
document.querySelectorAll('.remove-todo').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const response = await fetch(e.target.action, {
            method: 'POST'
        });
        if (response.ok) {
            window.location.reload(); // Recarregar a página após excluir a tarefa
        }
    });
});

// Carregar tarefas ao iniciar
loadTodos();