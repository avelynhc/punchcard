import classes from './Task.module.css';

const Task = (props) => {
  return (
    <li className={classes.task}>
      <h2>{props.user_id}</h2>
      <h2>{props.task_name}</h2>
      <h2>{props.start_time}</h2>
      <h2>{props.finish_time}</h2>
      <h2>{props.duration}</h2>
    </li>
  );
};

export default Task;
