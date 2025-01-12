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

// Função para exibir o formulário de edição com animação
function editarTarefa(id) {
    const form = document.getElementById(`editar-form-${id}`);
    form.style.display = 'block';
    form.style.opacity = '0';
    form.style.transition = 'opacity 0.3s ease';

    setTimeout(() => {
        form.style.opacity = '1';
    }, 10);
}

// Função para salvar a edição da tarefa
async function salvarEdicao(event, id) {
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

    const formData = new FormData(form);
    const response = await fetch(`/tarefa/${id}/editar`, {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        window.location.reload();
    } else {
        submitButton.disabled = false;
        submitButton.textContent = 'Salvar';
        alert('Erro ao salvar a tarefa. Tente novamente.');
    }
}

// Função para ocultar o formulário de edição com animação
function cancelarEdicao(id) {
    const form = document.getElementById(`editar-form-${id}`);
    form.style.opacity = '0';
    form.style.transition = 'opacity 0.3s ease';

    setTimeout(() => {
        form.style.display = 'none';
    }, 300);
}

// Carregar tarefas ao iniciar
loadTodos();