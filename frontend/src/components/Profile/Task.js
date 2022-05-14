import classes from './Task.module.css';

const Task = (props) => {
  return (
    <li className={classes.task}>
      <p>{props.user_id}</p>
      <p>{props.task_name}</p>
      <p>{props.start_time}</p>
      <p>{props.finish_time}</p>
      <p>{props.duration}</p>
    </li>
  );
};

export default Task;
