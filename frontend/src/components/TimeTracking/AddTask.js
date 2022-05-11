import { useRef, useState } from "react";
import classes from "./AddTask.module.css";

const AddTask = ({ onAddTask }) => {
  const taskNameRef = useRef("");

  const [isTaskStarted, setIsTaskStarted] = useState(false);

  const submitHandler = (event) => {
    event.preventDefault();
    onAddTask(taskNameRef.current.value);
    isTaskStarted ? setIsTaskStarted(true) : setIsTaskStarted(false);
  };

  // TODO: add disabled state to the submit button
  return (
    <form onSubmit={submitHandler}>
      <div className={classes.control}>
        <label htmlFor="task-name">Task Name</label>
        <input type="text" id="task-name" ref={taskNameRef} />
      </div>
      <section>
        <button
          type="submit"
          className={classes.toggle}
        >
          {isTaskStarted ? "Finish Task" : "Add Task"}
        </button>
      </section>
    </form>
  );
};

export default AddTask;
