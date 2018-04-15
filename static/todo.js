// TODO API
// 获取所有 todo
var apiTodoAll = function(callback) {
    var path = '/api/todo/all'
    ajax('GET', path, '', callback)
}

// 增加一个 todo
var apiTodoAdd = function(form, callback) {
    var path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

var apiTodoDelete = function(id, callback) {
    var path = `/api/todo/delete?id=${id}`
    ajax('GET', path, '', callback)
}

var apiTodoUpdate = function(form, callback) {
    var path = '/api/todo/update'
    ajax('POST', path, form, callback)
}

var todoTemplate = function(todo) {
// TODO DOM
    var t = `
        <div class="todo-cell">
            <button data-id=${todo.id} class="todo-delete">删除</button>
            <button data-id=${todo.id} class="todo-edit">编辑</button>
            <span class="todo-task">${todo.task}</span>
        </div>
    `
    return t
}

var todoUpdateTemplate = function(todoId) {
// TODO DOM
    var t = `
        <div class="todo-update-form">
            <input class="todo-update-input">
            <button data-id=${todoId} class="todo-update">更新</button>
        </div>
    `
    return t
}


var insertTodo = function(todo) {
    var todoCell = todoTemplate(todo)
    // 插入 todo-list
    var todoList = e('.todo-list')
    log('tdl', todoList)
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var insertUpdate = function(edit_button) {
    var todoId = edit_button.dataset.id
    var editCell = todoUpdateTemplate(todoId)
    edit_button.parentElement.insertAdjacentHTML('beforeend', editCell)
}

var loadTodos = function() {
    apiTodoAll(function(r) {
        console.log('load all', r)
        // 解析为 数组
        var todos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            insertTodo(todo)
        }
    })
}

var bindEventTodoAdd = function() {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-todo')
        var task = input.value
        log('click add', task)
        var form = {
            task: task,
        }
        apiTodoAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var todo = JSON.parse(r)
            insertTodo(todo)
        })
    })
}

var bindEventTodoDelete = function() {
    var todoList = e('.todo-list')
    todoList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('todo-delete')) {
            log('点到了 删除按钮，id 是', self.dataset.id )
            var todoId = self.dataset.id
            apiTodoDelete(todoId, function(r) {
                self.parentElement.remove()
            })
        } else {
            log('点击的不是删除按钮******')
        }
    })
}

var bindEventTodoEdit = function(){
    var todoList = e('.todo-list')
    todoList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('todo-edit')) {
            log('点到了 编辑按钮，id 是', self.dataset.id )
            insertUpdate(self)
        } else {
            log('点击的不是编辑按钮******')
        }
    })
}


var bindEventTodoUpdate = function(){
    var todoList = e('.todo-list')
    todoList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('todo-update')) {
            log('点到了 更新按钮，id 是', self.dataset.id )
            var todoCell = self.closest('.todo-cell')
            var input = todoCell.querySelector('.todo-update-input')
            var todoId = self.dataset.id
            var form = {
                id: todoId,
                task: input.value,
            }

            apiTodoUpdate(form, function(r){
                log('收到更新数据', r)
                var updateForm = todoCell.querySelector('.todo-update-form')
                updateForm.remove()
                var todo = JSON.parse(r)
                var todoTask = todoCell.querySelector('.todo-task')
                todoTask.innerText = todo.task
            })
        } else {
            log('点击的不是更新按钮******')
        }
    })
}

var bindEvents = function() {
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    bindEventTodoUpdate()
}

var __main = function() {
    bindEvents()
    loadTodos()
}

__main()
