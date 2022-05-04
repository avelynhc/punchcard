const Task = (props) => {
  return (
    <li>
      <h2>{props.task_name}</h2>
      <h2>{props.start_time}</h2>
      <h2>{props.finish_time}</h2>
    </li>
  );
};

export default Task;
