import classes from "./TaskDetail.module.css";
import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import SimpleDateTime  from 'react-simple-timestamp-to-date';

const TaskDetail = (props) => {
  const [taskDetail, setTaskDetail] = useState([null]);
  const [timer, setTimer] = useState({
    days: 0,
    hours: 0,
    mins: 0,
    secs: 0,
  });
  const [duration, setDuration] = useState({
    days: 0,
    hours: 0,
    mins: 0,
    secs: 0,
  });

  const BACKEND_API = "http://127.0.0.1:4000";
  const taskName = props.params;
  const history = useHistory();

  const getToken = () => {
    return localStorage.getItem("token");
  };

  const FetchDurationHandler = (taskName) => {
    const token = getToken();
    if (token) {
      return fetch(`${BACKEND_API}/task/${taskName}/duration`, {
        headers: {
          Authorization: "Bearer " + token,
        },
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            throw new Error("Cannot fetch task duration");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    }
  };

  const fetchTaskHandler = async () => {
    try {
      const token = getToken();
      if (token) {
        const response = await fetch(`${BACKEND_API}/task/${taskName}`, {
          headers: {
            Authorization: "Bearer " + token,
          },
        });
        if (!response.ok)
          throw new Error(`Cannot fetch task detail of ${taskName}`);
        const data = await response.json();
        if (
          data[taskName] &&
          data[taskName].length >= 1 &&
          data[taskName][0].finish_time
        ) {
          const current_duration = await FetchDurationHandler(taskName);
          data[taskName][0].duration = current_duration.duration;
        }
        setTaskDetail(data[taskName][0]);

        let durationDiff = data[taskName][0].duration;
        const secs_diff = durationDiff % 60;
        durationDiff = Math.floor(durationDiff / 60);
        const mins_diff = durationDiff % 60;
        durationDiff = Math.floor(durationDiff / 60);
        const hours_diff = durationDiff % 24;
        durationDiff = Math.floor(durationDiff / 24);
        const days_diff = durationDiff % 24;

        setDuration({
          days: days_diff,
          hours: hours_diff,
          mins: mins_diff,
          secs: secs_diff
        });
      }
    } catch (err) {
      console.log(err);
    }
  };

  const cancelHandler = (taskName) => {
    const token = getToken();
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
          alert(`Successfully cancel ${taskName}`);
          history.push("/tasks");
        } else {
          alert("Error while cancelling a task");
          throw new Error("Error while cancelling a task");
        }
      })
      .catch((err) => console.log(err));
    }
  };

  const deleteHandler = (taskName) => {
    const token = getToken();
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
          alert(`Successfully delete ${taskName}`);
          history.push("/tasks");
        } else {
          alert("Error while deleting a task");
          throw new Error("Error while deleting a task");
        }
      })
      .catch((err) => console.log(err));
    }
  };

  const finishTaskHandler = (ongoingTask) => {
    const token = getToken();
    if (token) {
      fetch(`${BACKEND_API}/task/${ongoingTask}/finish`, {
        method: "POST",
        body: JSON.stringify(ongoingTask),
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            throw new Error(`Failed to finish ${ongoingTask}`);
          }
        })
        .then(() => {
          history.push("/tasks");
        })
        .catch((err) => {
          console.log(err.message);
        });
    }
  };

  useEffect(() => {
    fetchTaskHandler();
    const interval = setInterval(() => {
      let timeDiff = new Date().getTime() - taskDetail.start_time * 1000;

      timeDiff = Math.floor(timeDiff / 1000);
      const secs_diff = timeDiff % 60;
      timeDiff = Math.floor(timeDiff / 60);
      const mins_diff = timeDiff % 60;
      timeDiff = Math.floor(timeDiff / 60);
      const hours_diff = timeDiff % 24;
      timeDiff = Math.floor(timeDiff / 24);
      const days_diff = timeDiff % 24;

      setTimer({
        days: days_diff,
        hours: hours_diff,
        mins: mins_diff,
        secs: secs_diff
      });
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, [taskName, taskDetail.start_time]);

  return (
    <>
      <h2>Task Detail Page</h2>
      <section className={classes.details}>
        {taskName && <p>task name: {taskName}</p>}
        {taskDetail.start_time && <p>start time: <SimpleDateTime dateFormat="DMY" dateSeparator="/"  timeSeparator=":">{taskDetail.start_time}</SimpleDateTime></p>}
        {taskDetail.finish_time && <p>finish time: <SimpleDateTime dateFormat="DMY" dateSeparator="/"  timeSeparator=":">{taskDetail.finish_time}</SimpleDateTime></p>}
        {taskDetail.finish_time && <p>duration: {`${duration.days}day(s) ${duration.hours}hour(s) ${duration.mins}min(s) ${duration.secs}sec(s)`}</p>}
        {!taskDetail.finish_time && (
          <button className={classes.timer}>
            Timer: {`${timer.days}day(s) ${timer.hours}hour(s) ${timer.mins}min(s) ${timer.secs}sec(s)`}
          </button>
        )}
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
        {!taskDetail.finish_time && (
          <button
            className={classes.finish}
            onClick={() => finishTaskHandler(`${taskDetail.task_name}`)}
          >
            Finish Current Task
          </button>
        )}
      </section>
    </>
  );
};

export default TaskDetail;
