import classes from "./TaskDetail.module.css";
import { useEffect, useState } from "react";
import { useParams, useHistory } from "react-router-dom";

const TaskDetail = () => {
  const [taskDetail, setTaskDetail] = useState([]);
  const BACKEND_API = "http://127.0.0.1:4000";
  const params = useParams();
  const taskName = params.taskName;
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
          // if (data[taskName][0].finish_time) {
          //   const current_duration = FetchDurationHandler(taskName);
          //   console.log(current_duration);
          // }
          // data[taskName][0].duration = current_duration.duration;
          setTaskDetail(data[taskName][0]);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, []);

  // const fetchTaskHandler = async () => {
  //   let current_duration = [];
  //   try {
  //     const token = localStorage.getItem("token");
  //     if (token) {
  //       const response = fetch(`${BACKEND_API}/task/${taskName}`, {
  //         headers: {
  //           Authorization: "Bearer " + token,
  //         },
  //       });
  //       if (!response.ok) {
  //         throw new Error(`Cannot fetch task detail of ${taskName}`);
  //       }
  //       const data = await response.json();
  //       if (data[taskName][0].finish_time) {
  //         current_duration = await FetchDurationHandler(taskName);
  //         console.log(current_duration);
  //       }
  //       data[taskName][0].duration = current_duration.duration;
  //       setTaskDetail(data[taskName][0]);
  //     }
  //   } catch (error) {
  //     console.log(error);
  //   }
  // };

  // const FetchDurationHandler = (task) => {
  //   const token = localStorage.getItem("token");
  //   if (token) {
  //     return fetch(`${BACKEND_API}/task/${task}/duration`, {
  //       headers: {
  //         Authorization: "Bearer " + token,
  //       },
  //     })
  //       .then((res) => {
  //         if (res.ok) {
  //           return res.json();
  //         } else {
  //           throw new Error("Cannot fetch task duration");
  //         }
  //       })
  //       .catch((err) => {
  //         console.log(err);
  //       });
  //   }
  // };

  // useEffect(() => {
  //   fetchTaskHandler();
  // }, []);

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
            return res.json();
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
            return res.json();
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
