import classes from "./UserProfile.module.css";
import React, { useState, useCallback, useEffect } from "react";

const BACKEND_API = "http://127.0.0.1:4000";

const UserProfile = () => {
  const [tasks, setTasks] = useState([]);
  const [durations, setDurations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [durationError, setDurationError] = useState(null);

  const fetchTasksHandler = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      let token = localStorage.getItem("token");
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
        setTasks(data);
      }
    } catch (error) {
      setError(error.message);
    }
    setIsLoading(false);
  }, []);

  const fetchDurationHandler = useCallback(async (taskName) => {
    // setIsLoading(true);
    setDurationError(null);
    try {
      let token = localStorage.getItem("token");
      if (token) {
        const response = await fetch(
          `${BACKEND_API}/task/${taskName}/duration`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        if (!response.ok) {
          throw new Error("Cannot fetch task duration");
        }
        const durationData = await response.json();
        setDurations(durationData);
      }
    } catch (error) {
      setDurationError(error.message);
    }
    // setIsLoading(false);
  }, [durationError]);

  useEffect(() => {
    fetchTasksHandler();
  }, [fetchTasksHandler]);

  return (
    <React.Fragment>
      <section className={classes.profile}>
        <h2>Your User Profile</h2>
        <h3>Reports</h3>
        <section>
          <button onClick={fetchTasksHandler}>Fetch Task Details</button>
        </section>
        {isLoading ? <p>Loading...</p> : ""}
        {error ? <p className={classes.error}>{error}</p> : ""}
        <ul className={classes.data}>
          {tasks.task_detail && tasks.task_detail.length > 0 ? (
            tasks.task_detail.map((task) => (
              <li key={task.id}>
                <p>task name: {task.task_name}</p>
                <p>start time: {task.start_time}</p>
                {task.finish_time && <p>finish time: {task.finish_time}</p>}
                {task.finish_time ? (
                  <p className={classes.complete}>Completed</p>
                ) : (
                  <p className={classes.pending}>Not Completed</p>
                )}
                {task.finish_time && durations.duration && (
                  <p>duration: {fetchDurationHandler(task.task_name)}</p>
                )}
              </li>
            ))
          ) : (
            <p>Found no tasks</p>
          )}
        </ul>
      </section>
    </React.Fragment>
  );
};

export default UserProfile;
