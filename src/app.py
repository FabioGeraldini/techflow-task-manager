import src.database as _db
from flask import Flask, request, jsonify

app = Flask(__name__)

# ── CREATE ──────────────────────────────────────────────
@app.route('/tasks', methods=['POST'])
def create_task():
    """Cadastra uma nova tarefa."""
    data     = request.get_json()
    title    = data.get('title', '').strip()
    status   = data.get('status', 'A Fazer')
    priority = data.get('priority', 'Média')

    if not title:
        return jsonify({'error': 'O título é obrigatório'}), 400

    conn    = _db.get_connection()
    cursor  = conn.execute(
        'INSERT INTO tasks (title, status, priority) VALUES (?, ?, ?)',
        (title, status, priority)
    )
    conn.commit()
    task_id = cursor.lastrowid

    return jsonify({'id': task_id, 'title': title, 'status': status, 'priority': priority}), 201

# ── READ ─────────────────────────────────────────────────
@app.route('/tasks', methods=['GET'])
def list_tasks():
    """Retorna todas as tarefas cadastradas."""
    conn  = _db.get_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    return jsonify([dict(t) for t in tasks])

# ── UPDATE ───────────────────────────────────────────────
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Atualiza título, status ou prioridade de uma tarefa."""
    data = request.get_json()
    conn = _db.get_connection()

    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404

    title    = data.get('title',    task['title'])
    status   = data.get('status',   task['status'])
    priority = data.get('priority', task['priority'])

    conn.execute(
        'UPDATE tasks SET title = ?, status = ?, priority = ? WHERE id = ?',
        (title, status, priority, task_id)
    )
    conn.commit()
    return jsonify({'id': task_id, 'title': title, 'status': status, 'priority': priority})

# ── DELETE ───────────────────────────────────────────────
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Remove uma tarefa pelo ID."""
    conn = _db.get_connection()

    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404

    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    return jsonify({'message': f'Tarefa {task_id} removida com sucesso'})

if __name__ == '__main__':
    _db.init_db()
    app.run(debug=True)

# ── FILTRO POR PRIORIDADE (mudança de escopo) ────────────
@app.route('/tasks/filter', methods=['GET'])
def filter_tasks():
    """Retorna tarefas filtradas por prioridade (Alta, Média ou Baixa)."""
    priority = request.args.get('priority', '').strip()

    if not priority:
        return jsonify({'error': 'Informe o parâmetro priority'}), 400

    conn  = _db.get_connection()
    tasks = conn.execute(
        'SELECT * FROM tasks WHERE priority = ?', (priority,)
    ).fetchall()

    return jsonify([dict(t) for t in tasks])
