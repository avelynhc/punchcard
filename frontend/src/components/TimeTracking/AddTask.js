import { useRef, useState } from "react";
import classes from "./AddTask.module.css";

const AddTask = ({ onAddTask }) => {
  const taskNameRef = useRef("");
  const [isSubmitted, setSubmitted] = useState(false);

  const submitHandler = (event) => {
    event.preventDefault();
    onAddTask(taskNameRef.current.value);
    setSubmitted(true);
    console.log("add task button was clicked!")
  };

  return (
    <form onSubmit={submitHandler}>
      <div className={classes.control}>
        <label htmlFor="task-name">Task Name</label>
        <input type="text" id="task-name" ref={taskNameRef} />
      </div>
      <section>
        <button
          type="submit"
          disabled={isSubmitted}
        >
          Add Task
        </button>
      </section>
    </form>
  );
};

export default AddTask;
