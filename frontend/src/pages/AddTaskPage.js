import { useState } from "react";
import classes from "./AddTaskPage.module.css";

import AddTask from "../components/TimeTracking/AddTask";
import Timer from "../components/UI/Timer";

const BACKEND_API = "http://127.0.0.1:4000";
const StartingPageContent = () => {
  const [isAdded, setIsAdded] = useState(false);
  const [error, setError] = useState(null);

  const addTaskHandler = (newTask) => {
    const url = isAdded
      ? `${BACKEND_API}/task/${newTask}/finish`
      : `${BACKEND_API}/task/${newTask}`;

    const token = localStorage.getItem("token");
    // TODO: make the check for token happen in a single place
    fetch(url, {
      method: "POST",
      body: JSON.stringify(newTask),
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    })
      .then((res) => {
        if (res.ok) {
          setIsAdded(true);
          return res.json();
        } else {
          throw new Error("Failed to add a new task");
        }
      })
      .catch((err) => {
        console.log(err.message);
        setError(err.message);
      });
  };

  return (
    <>
      <section className={classes.starting}>
        <h1>Please enter a task you want to start</h1>
      </section>
      <section>
        <AddTask onAddTask={addTaskHandler} />
        {isAdded && <Timer />}
        {!isAdded && <p className={classes.warning}>{error}</p>}
      </section>
    </>
  );
};

export default StartingPageContent;
