import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import classes from "./UserProfile.module.css";

const BACKEND_API = "http://127.0.0.1:4000";

const UserProfile = () => {
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const getToken = () => {
    return localStorage.getItem("token");
  };

  const fetchTasksHandler = async () => {
    setIsLoading(true);
    try {
      const token = getToken();
      if (token) {
        const response = await fetch(`${BACKEND_API}/tasks`, {
          headers: {
            Authorization: "Bearer " + token,
          },
        });
        if (!response.ok) {
          throw new Error("Cannot fetch task detail");
        }
        const data = await response.json();
        for (let i = 0; i < data.task_detail.length; i++) {
          if (data.task_detail[i].finish_time) {
            const current_duration = await FetchDurationHandler(
              data.task_detail[i].task_name
            );
            data.task_detail[i].duration = current_duration.duration;
          }
        }
        setTasks(data.task_detail);
      }
    } catch (error) {
      console.log(error);
    }
    setIsLoading(false);
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

  useEffect(() => {
    fetchTasksHandler();
  }, []);

  return (
    <React.Fragment>
      <section className={classes.profile}>
        <h2>Your User Profile</h2>
        <h3>Task Reports</h3>
        {isLoading && <p>Loading...</p>}
        {tasks.length > 0 ? (
          <ul className={classes.data}>
            {tasks.map((task) => (
              <li key={task.id}>
                <Link to={`/tasks/${task.task_name}`}>
                  task name: {task.task_name}
                </Link>
                <p>start time: {task.start_time}</p>
                {task.finish_time > 0 && <p>finish time: {task.finish_time}</p>}
                {task.duration && <p>duration: {task.duration}</p>}
                {task.finish_time > 0 ? (
                  <p className={classes.complete}>Complete</p>
                ) : (
                  <p className={classes.pending}>In Progress</p>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p>Found no tasks</p>
        )}
      </section>
    </React.Fragment>
  );
};

export default UserProfile;
