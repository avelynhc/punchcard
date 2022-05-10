import { useRef, useState } from "react";
import classes from "./AddTask.module.css";

const AddTask = (props) => {
  const taskNameRef = useRef("");

  const [isTaskStarted, setIsTaskStarted] = useState(false);

  const switchTaskModelHandler = () => {
    console.log(isTaskStarted)
    setIsTaskStarted((prevState) => !prevState);
    console.log(isTaskStarted)
  };

  const submitHandler = (event) => {
    event.preventDefault();
    props.onAddTask(taskNameRef.current.value);
    setIsTaskStarted(true);
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
          className={classes.toggle}
        >
          {isTaskStarted ? "Finish Task" : "Add Task"}
        </button>
      </section>
    </form>
  );
};

export default AddTask;
