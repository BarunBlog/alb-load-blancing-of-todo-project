import React, { useState, useEffect } from "react";
import axios from "axios";

const TODO_LIST_URL = "http://127.0.0.1:8000/todo/task-list/";

function App() {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    const callAPI = async () => {
      try {
        const res = await axios.get(TODO_LIST_URL);
        setTodos(res.data.results);
      } catch (error) {
        console.log("Error fetching todos:", error);
      }
    };

    callAPI();
  }, []);

  return (
    <div className="App">
      <h1>Todo List</h1>

      <div>
        {todos.map((todo) => (
          <div key={todo.id} className="todo-card">
            <h2>{todo.title}</h2>
            <p>
              <b>status: </b>
              {todo.status}
            </p>
            <br />
            <p>{todo.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
