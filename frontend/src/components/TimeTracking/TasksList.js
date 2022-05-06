import React from "react";
import classes from "./TasksList.module.css";

import Task from "./Task";

const TasksList = (props) => {
  return (
    <ul className={classes["tasks-list"]}>
      {props.tasks.map((task) => (
        <Task
          key={task.id}
          user_id={task.user_id}
          task_name={task.task_name}
          start_time={task.start_time}
          finish_time={task.finish_time}
        />
      ))}
    </ul>
  );
};

export default TasksList;
