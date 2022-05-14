import classes from "./TaskDetail.module.css";
import { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";

const TaskDetail = (props) => {
  const [taskDetail, setTaskDetail] = useState([null]);
  const BACKEND_API = "http://127.0.0.1:4000";
  const taskName = props.params;
  const history = useHistory();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetch(`${BACKEND_API}/task/${taskName}`, {
        headers: {
          Authorization: "Bearer " + token,
        },
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            throw new Error(`Cannot fetch task detail of ${taskName}`);
          }
        })
        .then((data) => {
          setTaskDetail(data[taskName][0]);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [taskName]);

  const cancelHandler = (taskName) => {
    const token = localStorage.getItem("token");
    if (token) {
      fetch(`${BACKEND_API}/task/${taskName}/cancel`, {
        method: "POST",
        body: JSON.stringify({
          returnSecureToken: true,
        }),
        headers: {
          Authorization: "Bearer " + token,
        },
      })
        .then((res) => {
          if (res.ok) {
            setTaskDetail(null);
            alert(`Succesfully cancel ${taskName}`);
            history.push("/task");
          } else {
            alert("Error while deleting a task");
            throw new Error("Error while cancelling a task");
          }
        })
        .catch((err) => console.log(err));
    }
  };

  const deleteHandler = (taskName) => {
    const token = localStorage.getItem("token");
    if (token) {
      fetch(`${BACKEND_API}/task/${taskName}/delete`, {
        method: "POST",
        body: JSON.stringify({
          returnSecureToken: true,
        }),
        headers: {
          Authorization: "Bearer " + token,
        },
      })
        .then((res) => {
          if (res.ok) {
            setTaskDetail(null);
            alert(`Succesfully delete ${taskName}`);
            history.push("/task");
          } else {
            alert("Error while deleting a task");
            throw new Error("Error while deleting a task");
          }
        })
        .catch((err) => console.log(err));
    }
  };

  return (
    <>
      <h2>Welcome to task detail page!</h2>
      <section className={classes.details}>
        {taskName && <p>task name: {taskName}</p>}
        {taskDetail.start_time && <p>start time: {taskDetail.start_time}</p>}
        {taskDetail.finish_time && <p>finish time: {taskDetail.finish_time}</p>}
        {taskDetail.finish_time && <p>duration: {taskDetail.duration}</p>}
        {!taskDetail.finish_time ? (
          <button
            className={classes.cancel}
            type="button"
            onClick={() => cancelHandler(`${taskDetail.task_name}`)}
          >
            Cancel
          </button>
        ) : (
          <button
            className={classes.delete}
            type="button"
            onClick={() => deleteHandler(`${taskDetail.task_name}`)}
          >
            Delete
          </button>
        )}
      </section>
    </>
  );
};

export default TaskDetail;
